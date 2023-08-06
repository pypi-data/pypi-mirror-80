import os,shutil,glob

def encrypt_model(src,dst=None,key=0xef):
    dst=dst or src+'.encrypted'
    with open(src ,'rb') as f:
        data=f.read()
    data2=bytearray(data)
    for i,B in enumerate(data):
        data2[i]=B^key
    data2=bytes(data2)
    with open(dst,'wb') as f:
        f.write(data2)
def decrypt_model(src,dst=None,key=0xef):
    dst=dst or src+'.decrypted'
    with open(src ,'rb') as f:
        data=f.read()
    data2=bytearray(data)
    for i,B in enumerate(data):
        data2[i]=B^key
    data2=bytes(data2)
    with open(dst,'wb') as f:
        f.write(data2)

if __name__ == '__main__':
    pass
    encrypt_model(
        src='/home/ars/sda6/work/play/wk-classify/local/capacitor_color1_face0/model_best_[capacitor][0918][resnet18][color1][face0][cropped][epoch=29&acc=0.9538].onnx'
    )