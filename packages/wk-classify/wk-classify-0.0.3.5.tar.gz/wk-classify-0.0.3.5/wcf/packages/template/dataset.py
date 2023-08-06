
import os, shutil, glob, random
from PIL import Image
import torch
import math
import  numpy as np
IMG_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif', '.tiff', '.webp')
from torch.utils.data import DataLoader

def load_image_files(dir,recursive=False):
    fs=[]
    for ext in IMG_EXTENSIONS:
        if recursive:
            fs += glob.glob(dir + '/**/*' + ext,recursive=True)
        else:
            fs += glob.glob(dir + '/*' + ext)
    return fs
def load_image_folder(path):
    classes = os.listdir(path)
    files = {cls: [] for cls in classes}
    for cls in classes:
        cls_dir = os.path.join(path, cls)
        for ext in IMG_EXTENSIONS:
            files[cls] += glob.glob(cls_dir + '/*' + ext)
    return files

def adaptive_duplicate(class_files,nums=None,ratios=None):
    max_length = max([len(fs) for fs in class_files.values()])
    if not nums:
        if not ratios:
            nums=[max_length]*len(class_files)
        else:
            s=sum(ratios)
            ratios=[x/s for x in ratios]
            cls_file_nums=[]
            for i,cls in enumerate(sorted(class_files.keys())):
                cls_file_nums.append(len(class_files[cls]))
            actual_ratios=[x/sum(cls_file_nums) for x in cls_file_nums]
            needs_satisfied=[x1/x2 for x1,x2 in zip(actual_ratios,ratios)]
            index=np.argmax(needs_satisfied)
            ratios=np.array(ratios)
            ratios*=1/ratios[index]
            nums=[int(cls_file_nums[index]*ratios[i]) for i in range(len(class_files.keys()))]
    new_class_files = {}
    for i,cls in enumerate(sorted(class_files.keys())):
        fs=class_files[cls]
        new_class_files[cls] = fs + random.choices(fs, k=nums[i] - len(fs))
    return new_class_files


class ImageFolder:
    def __init__(self, path, balance_classes=False, transform=None):
        self.class_files = load_image_folder(path)
        if balance_classes:
            self.class_files = adaptive_duplicate(self.class_files,ratios=balance_classes if isinstance(balance_classes,(tuple,list)) else None)
        print('Data Info'.center(200,'*'))
        for k,v in self.class_files.items():
            print(k,len(v))
        self.classes = sorted(list(self.class_files.keys()))
        self.cls2idx = {cls: i for i, cls in enumerate(self.classes)}
        self.data = []
        for cls, fs in self.class_files.items():
            self.data += list(zip(fs, [self.cls2idx[cls]] * len(fs)))
        self.transform = transform

    def __getitem__(self, item):
        img_path, cls_idx = self.data[item]
        img = Image.open(img_path)
        if self.transform:
            img = self.transform(img)
        return img, cls_idx

    def __len__(self):
        return len(self.data)
class Dataset(DataLoader):
    def __init__(self, path=None, balance_classes=False, transform=None, data=None, batch_size=16,
                 shuffle=True,num_workers=4):
        data = data or ImageFolder(path, balance_classes, transform)
        super().__init__(data,batch_size=batch_size,shuffle=shuffle,num_workers=num_workers)
def demo():
    pass
