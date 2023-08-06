import numpy as np
from .predict import Predictor,PredictConfigBase
from .dataset import load_image_files
import wk
import cv2


class TestConfigBase:
    TEST_DIR=None
    TEST_OUTPUT_DIR=None
    PREDICT_CONFIG=None
    SPLIT_BY_PROB=False
    predictor=None
    def __init__(self):
        if not self.TEST_OUTPUT_DIR:
            self.TEST_OUTPUT_DIR=self.TEST_DIR+'_test_out'
        wk.remake(self.TEST_OUTPUT_DIR)
        assert self.PREDICT_CONFIG or self.predictor
    def get_predictor(self):
        return self.predictor or Predictor(self.PREDICT_CONFIG)

def test(cfg):
    assert isinstance(cfg,TestConfigBase)
    fs=load_image_files(cfg.TEST_DIR,recursive=True)
    predictor=cfg.get_predictor()
    outFolder=wk.Folder(cfg.TEST_OUTPUT_DIR)
    res={}
    files={}
    probs=[]
    print('Num images: %s'%(len(fs)))
    for i,f in enumerate(fs):
        img=cv2.imread(f)
        if img is None:
            print('Failed to load %s'%(f))
            continue
        cls,prob=predictor.predict(img)
        probs.append(predictor.cache['probs'])

        if cfg.SPLIT_BY_PROB:
            outFolder.openFolder(cls).openFolder('%.1f'%(prob)).eat(f)
        else:
            outFolder.openFolder(cls).eat(f)
        print(i,f,cls)
        files[f]=[cls,prob]

    res['files']=files
    res['probs']=probs
    return res
def plot_result(res,cls=0,xlabel='',ylabel=''):
    res=res['probs']
    res=[res[i][cls] for i in range(len(res))]
    res.sort()
    xs = []
    ys = []
    for i in range(len(res)):
        xs.append(res[i])
        ys.append(i / len(res))
    from matplotlib import pyplot as plt
    plt.plot(xs,ys)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

if __name__ == '__main__':
    test(TestConfigBase())