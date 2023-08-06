# wk-classify
A package of tools for building deep-learning classification programs. Easy to use, light and powerful.

# Install
```shell script
pip3 install wk-classify
```

# Usage

### Quick start
```python
from wcf import train,  TrainValConfigBase
class Config(TrainValConfigBase):
    TRAIN_DIR = 'path for train set'
    VAL_DIR = 'path for val set'
cfg=Config()
train(cfg)
```
### A real example
```python
from wcf import train, TrainValConfigBase, val,t,EasyTransform,models_names
class Config(TrainValConfigBase):
    MODEL_TYPE = models_names.shufflenet_v2_x0_5
    TAG = '[%s]'%(MODEL_TYPE)
    GEN_CLASSES_FILE = True
    USE_tqdm_TRAIN = True
    INPUT_SIZE = (252,196) #(w,h)
    BATCH_SIZE = 64
    MAX_EPOCHS = 200
    BALANCE_CLASSES = True
    VAL_INTERVAL = 1
    WEIGHTS_SAVE_INTERVAL = 1
    WEIGHTS_INIT = 'weights/training/model_best.pkl'
    TRAIN_DIR = '/home/ars/sda5/data/projects/烟盒/data/现场采集好坏烟照片/相机1-train'
    VAL_DIR = '/home/ars/sda5/data/projects/烟盒/data/现场采集好坏烟照片/相机1-val'
    val_transform = EasyTransform([
        t.Resize(INPUT_SIZE[::-1]),
        t.SaveToDir('data/test'),
        t.ToTensor(),
    ])
    train_transform = EasyTransform([
        t.ColorJitter(brightness=0.2, contrast=0, saturation=0, hue=0),
        # t.RandomHorizontalFlip(),
        # t.RandomVerticalFlip(),
        # t.RandomRotate(360),
        t.RandomTranslate(30),
        t.RandomBlur(p=0.3, radius=1),
        t.RandomSPNoise(p=0.3),
        *val_transform,
    ])
    # def get_model(self, num_classes=None):
        # model=YourModel(...)
        # return model


if __name__ == '__main__':
    cfg = Config()
    train(cfg)
    # res=val(cfg)
    # print(res)

```

### all options
see the `TrainValConfigBase` class for all options

### how to predict?
see `demo_predict.py`

## more

see `demo_train.py` and  `demo_predict.py`



