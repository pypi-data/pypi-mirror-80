from .dataset import Dataset
import os
import torch
from torch.nn import CrossEntropyLoss
import torch.optim
from torch import optim
import numpy as np
from .config import ConfigBase
from wcf.networks.utils import load_model
import logging
import json
import time

time_stamp = time.strftime('[%m%d]', time.localtime(time.time()))


def load_weights(model, weights_path=None, except_keys=[], strict=False):
    if weights_path:
        if os.path.exists(weights_path):
            try:
                state_dict = torch.load(weights_path)
                remove_keys = []
                for k in state_dict.keys():
                    for key in except_keys:
                        if k.startswith(key):
                            remove_keys.append(k)
                for k in remove_keys:
                    del state_dict[k]
                    print('ignore key:', k)
                model.load_state_dict(state_dict, strict=strict)
                print('Weights loaded from %s' % (weights_path))
            except:
                logging.warning('Cannot load pretrained model %s' % (weights_path))

        if not os.path.exists(weights_path):
            logging.warning('weights path %s does not exists.' % (weights_path))
    return model


class TrainValConfigBase(ConfigBase):
    MODEL_TYPE = 'resnet18'
    TIME_STAMP = time_stamp
    PROJECT_TAG = ''
    EXTRA_TAG = ''
    TAG = None
    NUM_CLASSES = None
    TRAIN_DIR = None
    VAL_DIR = None
    DATA_DIR = None
    INPUT_SIZE = (224, 224)
    BATCH_SIZE = 16
    BATCH_SIZE_TRAIN = None
    BATCH_SIZE_VAL = None
    MAX_EPOCHS = 100
    PATIENCE = 20
    LR_INIT = 1e-3
    LR_END = 1e-5
    USE_PRETRAINED = True
    WEIGHTS_INIT = None
    BALANCE_CLASSES = True
    BALANCE_CLASSES_VAL = False
    criterion = CrossEntropyLoss()
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    WEIGHTS_SAVE_INTERVAL = 1
    WEIGHTS_SAVE_DIR = 'weights/training'
    WEIGHTS_SAVE_BEST_NAME = 'model_best_{tag}[epoch={epoch}&acc={val_acc:.4f}].pkl'
    WEIGHTS_SAVE_NAME = 'model{tag}.pkl'
    VAL_INTERVAL = 1
    train_transform = None
    val_transform = None
    USE_tqdm_TRAIN = True
    USE_tqdm_VAL = False
    GEN_CLASSES_FILE = False
    CLASSES_FILE_PATH = 'classes.txt'
    LOG_INFO=True

    def get_TAG(self):
        return '%s%s%s%s' % (
        self.PROJECT_TAG or '', self.TIME_STAMP or '', '[%s]' % (self.MODEL_TYPE), self.EXTRA_TAG or '')

    def get_train_data(self):
        return Dataset(path=self.TRAIN_DIR, balance_classes=self.BALANCE_CLASSES, batch_size=self.BATCH_SIZE_TRAIN,
                        transform=self.train_transform)

    def get_val_data(self):
        return Dataset(path=self.VAL_DIR, balance_classes=self.BALANCE_CLASSES_VAL, batch_size=self.BATCH_SIZE_VAL,
                        transform=self.val_transform, shuffle=False)
    def get_classes(self):
        return sorted(os.listdir(self.TRAIN_DIR))
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.BATCH_SIZE_TRAIN = self.BATCH_SIZE_TRAIN or self.BATCH_SIZE
        self.BATCH_SIZE_VAL = self.BATCH_SIZE_VAL or self.BATCH_SIZE
        if self.TAG is None:
            self.TAG = self.get_TAG()
        self.train_data = self.get_train_data()
        self.val_data = self.get_val_data()
        if self.__class__.NUM_CLASSES is None:
            self.__class__.NUM_CLASSES = len(self.get_classes())
        self.model = self.get_model()
        self.model = load_weights(self.model, weights_path=self.WEIGHTS_INIT)
        self.model.to(self.DEVICE)
        if self.GEN_CLASSES_FILE:
            with open(self.CLASSES_FILE_PATH, 'w') as f:
                f.write('\n'.join(self.get_classes()))
        if self.LOG_INFO:
            self.log_info()
            # pass
    def log_info(self):
        print('CONFIG INFO'.center(200, '*'))
        dic = self.get_config_info_dict()
        max_length = 50
        for k, v in dic.items():
            # k=''
            print('%s\t:\t%s' % (k.rjust(max_length, '_'), v))
    def check_params(self):
        assert self.DATA_DIR or self.TRAIN_DIR

    def get_model(self, num_classes=None):
        num_classes = num_classes or self.NUM_CLASSES
        assert num_classes
        model = load_model(self.MODEL_TYPE, num_classes=num_classes, pretrained=self.USE_PRETRAINED)
        return model


class AccuracyMetric:
    def __init__(self):
        self.label_counts = 0
        self.pred_counts = 0
        self.correct_counts = 0
        self.sample_counts = 0

    def analyze(self):
        def non_zero(t):
            '''to prevent some arrays from being divided by zeros'''
            mask = t == 0
            epsilon = 1e-7
            tmp = np.zeros_like(mask)
            tmp.fill(epsilon)
            t = t + tmp * mask
            return t

        if self.sample_counts == 0:
            raise Exception('No samples for training?')
        else:
            recalls = self.correct_counts / non_zero(self.label_counts)
            precisions = self.correct_counts / non_zero(self.pred_counts)
            accuracy = sum(self.correct_counts) / non_zero(self.sample_counts)
        res = dict(
            recalls=recalls,
            precisions=precisions,
            accuracy=accuracy,
        )
        return res

    def batch_step(self, preds, labels):
        preds, labels = preds.cpu(), labels.cpu()
        batch_size, num_classes = preds.shape
        _, preds = torch.max(preds, 1)
        labels = torch.zeros((batch_size, num_classes)).scatter_(-1, torch.unsqueeze(labels, -1), 1)
        preds = torch.zeros((batch_size, num_classes)).scatter_(-1, torch.unsqueeze(preds, -1), 1)
        l=torch.sum(labels, 0).numpy()
        p=torch.sum(preds, 0).numpy()
        c=torch.sum(labels * preds, 0).numpy()
        s=len(labels)
        self.label_counts += l
        self.pred_counts += p
        self.correct_counts += c
        self.sample_counts += s
        # print(self.label_counts,self.pred_counts,self.correct_counts,self.sample_counts)


class MonitoredList:
    def __init__(self, whats_best=None, name=None):
        self.data = []
        self.best = None
        self.best_idx = None
        self.name = name
        if (not whats_best) and name:
            assert isinstance(name, str)
            if 'loss' in name.lower():
                whats_best = 'min'
            elif ('acc' in name.lower()) or ('accuracy' in name.lower()):
                whats_best = 'max'
        self.whats_best = whats_best

    def better(self, a, b):
        assert self.whats_best in ['max', 'min']
        if self.whats_best == 'max':
            return a > b
        else:
            assert self.whats_best == 'min'
            return a < b

    def push(self, data):
        self.data.append(data)
        if len(self.data) == 1:
            self.best = data
            self.best_idx = 0
        elif self.whats_best and self.better(data, self.best):
            self.best = data
            self.best_idx = len(self.data) - 1

    def last_is_best(self):
        assert len(self.data)
        assert self.whats_best
        return self.best_idx == len(self.data) - 1

    def mean(self):
        return np.array(self.data).mean()

    def max(self):
        return np.array(self.data).min(axis=0)

    def min(self):
        return np.array(self.data).max(axis=0)


class HistoryMonitor:
    def __init__(self):
        self.data = dict()

    def push(self, data):
        for k, v in data.items():
            if k not in self.data.keys():
                self.data[k] = MonitoredList(name=k)
            self.data[k].push(v)

    def get(self, k):
        return self.data[k]


def val(cfg):
    assert isinstance(cfg, TrainValConfigBase)
    model = cfg.model
    model.eval()
    losses = []
    val_acc_metric = AccuracyMetric()
    val_data = cfg.val_data
    if cfg.USE_tqdm_VAL:
        import tqdm
        val_data = tqdm.tqdm(val_data)
    for step, (inputs, labels) in enumerate(val_data):
        inputs = inputs.to(cfg.DEVICE)
        labels = labels.to(cfg.DEVICE)
        outputs = model(inputs)
        loss = cfg.criterion(outputs, labels)
        losses.append(loss.item())
        val_acc_metric.batch_step(outputs, labels)
    res = val_acc_metric.analyze()
    res['loss'] = np.mean(losses)
    return res


def train(cfg):
    assert isinstance(cfg, TrainValConfigBase)
    train_data = cfg.train_data
    model = cfg.model
    # optimizer = torch.optim.Adam(model.parameters(), lr=cfg.LR_INIT)
    optimizer = optim.SGD(model.parameters(), lr=cfg.LR_INIT, momentum=0.9)
    lr_scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, cfg.MAX_EPOCHS, cfg.LR_END)

    global_step = -1
    saving_interval = int(cfg.WEIGHTS_SAVE_INTERVAL * len(train_data))
    val_interval = int(cfg.VAL_INTERVAL * len(train_data))
    if not os.path.exists(cfg.WEIGHTS_SAVE_DIR):
        os.makedirs(cfg.WEIGHTS_SAVE_DIR)
    train_history = HistoryMonitor()
    val_history = HistoryMonitor()
    for epoch in range(cfg.MAX_EPOCHS):
        model.train()
        losses = []
        train_acc_metric = AccuracyMetric()
        if cfg.USE_tqdm_TRAIN:
            import tqdm
            train_data = tqdm.tqdm(train_data)
        log = '\n' + ('Epoch %s' % (epoch)).center(200, '*')
        print(log)
        for step, (inputs, labels) in enumerate(train_data):
            inputs=inputs.to(cfg.DEVICE)
            labels=labels.to(cfg.DEVICE)
            global_step += 1
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = cfg.criterion(outputs, labels)
            loss.backward()
            losses.append(loss.item())
            optimizer.step()
            train_acc_metric.batch_step(outputs, labels)
            if global_step % saving_interval == 0 and global_step != 0:
                torch.save(model.state_dict(), cfg.WEIGHTS_SAVE_DIR + '/model.pkl')
                context = dict(
                    tag=cfg.TAG,
                    epoch=epoch,
                    step=global_step,
                )
                torch.save(model.state_dict(),
                           os.path.join(cfg.WEIGHTS_SAVE_DIR, cfg.WEIGHTS_SAVE_NAME.format(**context)))
            if global_step % val_interval == 0 and global_step != 0:
                val_res = val(cfg)
                val_history.push(val_res)
                log = '''\nStep:{global_step}\tValLoss:{val_loss:.4f}\tValAccuracy:{val_acc:.4f}\tValRecalls:{val_recalls}\tValPrecisions:{val_precisions}'''.format(
                    epoch=epoch, global_step=global_step, val_loss=val_res['loss'], val_acc=val_res['accuracy'],
                    val_recalls=val_res['recalls'], val_precisions=val_res['precisions']
                )
                print(log)
                context = dict(
                    tag=cfg.TAG,
                    epoch=epoch,
                    step=global_step,
                    val_acc=val_res['accuracy'],
                    val_loss=val_res['loss'],
                )

                if val_history.get('accuracy').last_is_best():
                    torch.save(model.state_dict(),
                               os.path.join(cfg.WEIGHTS_SAVE_DIR, cfg.WEIGHTS_SAVE_BEST_NAME.format(**context)))
                    torch.save(model.state_dict(), cfg.WEIGHTS_SAVE_DIR + f'''/model_best.pkl''')
                    print('New best accuracy: %.4f, model saved.' % (val_res['accuracy']))
                model.train()
        lr_scheduler.step()
        train_res = train_acc_metric.analyze()
        train_res['loss'] = np.mean(losses)
        train_history.push(train_res)
        lr = optimizer.state_dict()['param_groups'][0]['lr']
        log = '''\nTrainLoss:{train_loss:.4f}\tTrainAccuracy:{train_acc:.4f}\tTrainRecalls:{train_recalls}\tTrainPrecisions:{train_precisions}\tLearningRate:{lr:.6f}'''.format(
            epoch=epoch, lr=lr, train_loss=train_res['loss'], train_acc=train_res['accuracy'],
            train_recalls=train_res['recalls'], train_precisions=train_res['precisions']
        )
        print(log)
        torch.save(model.state_dict(), os.path.join(cfg.WEIGHTS_SAVE_DIR, 'model.pkl'))
