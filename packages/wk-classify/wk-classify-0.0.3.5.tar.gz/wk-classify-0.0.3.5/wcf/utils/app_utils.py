from wcf import train, TrainValConfigBase, val, t, EasyTransform, models_names
from wk import PointDict
from vtgui.app import make_app, SelectDir, SelectFile, VirtualField
from wcf import models_names
import sys


def make_trainval_config(
        cfg, data_cfg
):
    cfg=PointDict(**cfg)
    data_cfg=PointDict(**data_cfg)
    class Config(TrainValConfigBase):
        MODEL_TYPE = cfg.MODEL_TYPE
        GEN_CLASSES_FILE = cfg.GEN_CLASSES_FILE
        USE_tqdm_TRAIN = cfg.USE_tqdm_TRAIN
        INPUT_SIZE = (cfg.INPUT_W, cfg.INPUT_H)
        BATCH_SIZE = cfg.BATCH_SIZE
        MAX_EPOCHS = cfg.MAX_EPOCHS
        BALANCE_CLASSES = cfg.BALANCE_CLASSES
        BALANCE_CLASSES_VAL = cfg.BALANCE_CLASSES_VAL
        VAL_INTERVAL = cfg.VAL_INTERVAL
        WEIGHTS_SAVE_INTERVAL = cfg.WEIGHTS_SAVE_INTERVAL
        WEIGHTS_INIT = cfg.WEIGHTS_INIT
        TRAIN_DIR = cfg.TRAIN_DIR
        VAL_DIR = cfg.VAL_DIR
        INPUT_W = cfg.INPUT_W
        INPUT_H = cfg.INPUT_H
        USE_PRETRAINED = cfg.USE_PRETRAINED
        val_transform = EasyTransform([
            t.Resize(INPUT_SIZE[::-1]),
            t.SaveToDir(cfg.VISUALIZE_RESULT_DIR),
            t.ToTensor(),
        ])
        train_transform = EasyTransform(list(filter(lambda x:x is not None,[
            t.ColorJitter(brightness=data_cfg.BRIGHTNESS, contrast=data_cfg.CONTRAST, saturation=data_cfg.SATURATION, hue=data_cfg.HUE),
            t.RandomHorizontalFlip() if data_cfg.RandomHorizontalFlip else None,
            t.RandomVerticalFlip() if data_cfg.RandomVerticalFlip else None,
            t.RandomRotate(data_cfg.RandomRotate) if data_cfg.RandomRotate else None ,
            t.RandomShear(data_cfg.RandomShear,data_cfg.RandomShear) if data_cfg.RandomShear else None,
            t.RandomTranslate(data_cfg.RandomTranslate) if data_cfg.RandomTranslate else None,
            t.RandomBlur(p=data_cfg.RandomBlur, radius=1) if data_cfg.RandomBlur else None,
            t.RandomSPNoise(p=data_cfg.RandomSPNoise) if data_cfg.RandomSPNoise else None,
            *val_transform,
        ])))
    for k,v in cfg.items():
        setattr(Config,k,v)
    return Config




models = [
    models_names.resnet10,
    models_names.resnet18,
    models_names.resnet50,
    models_names.shufflenet_v2_x0_5,
    models_names.shufflenet_v2_x1_0,
]

def get_default_base_config(**kwargs):
    base_config = dict(
        MODEL_TYPE='resnet18',
        GEN_CLASSES_FILE=True,
        USE_tqdm_TRAIN=True,
        USE_PRETRAINED=True,
        BATCH_SIZE=64,
        MAX_EPOCHS=200,
        BALANCE_CLASSES=True,
        BALANCE_CLASSES_VAL=True,
        VAL_INTERVAL=1,
        WEIGHTS_SAVE_INTERVAL=1,
        WEIGHTS_INIT='weights/training/model_best.pkl',
        INPUT_W=224,
        INPUT_H=224,
        VISUALIZE_RESULT_DIR='data/visualize',
    )
    base_config.update(**kwargs)
    return base_config

def get_default_data_config(**kwargs):
    data_config = dict(
        BRIGHTNESS=0.1,
        CONTRAST=0.05,
        SATURATION=0.05,
        HUE=0.05,
        RandomHorizontalFlip=False,
        RandomVerticalFlip=False,
        RandomRotate=0,
        RandomShear=0,
        RandomTranslate=0,
        RandomBlur=0.3,
        RandomSPNoise=0.3,
    )
    data_config.update(**kwargs)
    return data_config

def get_base_config(train_dir='/home/ars/sda5/data/projects/烟分类/data/烟分类-train',val_dir='/home/ars/sda5/data/projects/烟分类/data/烟分类-val'):
    base_config = dict(
        MODEL_TYPE=VirtualField(title='模型', description='选择模型', default='resnet18', options=models),
        TRAIN_DIR=SelectDir(train_dir),
        VAL_DIR=SelectDir(val_dir),
        GEN_CLASSES_FILE=VirtualField(default=True, title='生成类别文件'),
        USE_tqdm_TRAIN=True,
        USE_PRETRAINED=True,
        BATCH_SIZE=64,
        MAX_EPOCHS=200,
        BALANCE_CLASSES=True,
        BALANCE_CLASSES_VAL=True,
        VAL_INTERVAL=1,
        WEIGHTS_SAVE_INTERVAL=1,
        WEIGHTS_INIT='weights/training/model_best.pkl',
        INPUT_W=224,
        INPUT_H=224,
        VISUALIZE_RESULT_DIR='data/visualize',
    )
    return base_config

def get_data_config():
    data_config = dict(
        BRIGHTNESS=0.1,
        CONTRAST=0.05,
        SATURATION=0.05,
        HUE=0.05,
        RandomHorizontalFlip=False,
        RandomVerticalFlip=False,
        RandomRotate=0,
        RandomShear=0,
        RandomTranslate=0,
        RandomBlur=0.3,
        RandomSPNoise=0.3,
    )
    return data_config


def training_callback(base_cfg, data_cfg={}):
    base_config = get_default_base_config(**base_cfg)
    data_config = get_default_data_config(**data_cfg)
    Config= make_trainval_config(base_config,data_config)
    cfg=Config()
    train(cfg)

def make_training_app(base_config,data_config,function=training_callback,columns=[4, 4],window_size=(1600,800)):
    app = make_app(function=function, args=(base_config, data_config), columns=columns,window_size=window_size)
    return app

def make_example_training_app(train_dir='',val_dir=''):
    base_config = get_base_config(train_dir=train_dir, val_dir=val_dir)
    data_config = get_data_config()
    return make_training_app(base_config,data_config)

def make_simple_training_app(train_dir='', val_dir='', default_base_config=None, default_data_config=None,train_func=None):
    if default_data_config is None:
        default_data_config = {}
    if default_base_config is None:
        default_base_config = {}
    base_config=dict(
        TRAIN_DIR=SelectDir(default=train_dir,title='训练集路径'),
        VAL_DIR=SelectDir(default=val_dir,title='验证集路径'),
    )
    def train(base_config):
        default_base_config.update(**base_config)
        training_callback(default_base_config,default_data_config)
    return make_app(train_func or train,args=(base_config,),columns=2,window_size=(1300,800))

def capacitor_app_demo(train_dir='',val_dir=''):
    default_data_config=dict(
        BRIGHTNESS=0.1,
        CONTRAST=0.05,
        SATURATION=0.05,
        HUE=0.1,
        RandomHorizontalFlip=False,
        RandomVerticalFlip=False,
        RandomRotate=360,
        RandomShear=0,
        RandomTranslate=50,
        RandomBlur=0.3,
        RandomSPNoise=0.3,
    )
    default_base_config=dict(
        MODEL_TYPE='resnet18',
        GEN_CLASSES_FILE=True,
        USE_tqdm_TRAIN=True,
        USE_PRETRAINED=False,
        BATCH_SIZE=64,
        MAX_EPOCHS=200,
        BALANCE_CLASSES=True,
        BALANCE_CLASSES_VAL=True,
        VAL_INTERVAL=1,
        WEIGHTS_SAVE_INTERVAL=1,
        WEIGHTS_INIT=None,
        INPUT_W=360,
        INPUT_H=270,
        LOG_INFO=False,
        VISUALIZE_RESULT_DIR='data/visualize',
    )
    def train(base_config):
        try:
            default_base_config.update(**base_config)
            training_callback(default_base_config, default_data_config)
        except:
            print('Error occurred !')
    return make_simple_training_app(train_dir=train_dir,val_dir=val_dir,default_base_config=default_base_config,default_data_config=default_data_config,train_func=train)
if __name__ == '__main__':
    # make_simple_training_app(
    #     train_dir='/home/ars/sda5/data/chaoyuan/datasets/classify_datasets/公章/train',
    #     val_dir='/home/ars/sda5/data/chaoyuan/datasets/classify_datasets/公章/train',
    # ).run()
    capacitor_app_demo(
        train_dir='/home/ars/sda5/data/projects/无锡和博电容/data2/color1/face2/标注中-train',
        val_dir='/home/ars/sda5/data/projects/无锡和博电容/data2/color1/face2/标注中-val',
    ).run()

