import os
import glob
import numpy as np
import json
import cv2
import shutil
from ruamel import yaml
from tqdm import tqdm

def convert(size, box): # size:(原图height,原图width) , box:(xmin,ymin,width,height)
    dh = 1./size[0] 
    dw = 1./size[1]    
    x = (box[0]+box[2]/2.0)*dw   
    y = (box[1]+box[3]/2.0)*dh   
    w = box[2]*dw         
    h = box[3]*dh

    return (x, y, w, h)    # 返回相对于原图的物体中心点的x坐标比,y坐标比,宽度比,高度比,取值范围[0-1]

def makedir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def copy_image(ori_path,path):
    images=[]
    with open(ori_path,'r',encoding='UTF-8',errors='ignore') as f:
        for line in f:
            images.append(line.strip())  

    for i in tqdm(range(len(images)),desc='Copy images'):
        video_file=images[i][images[i].rfind('/',0,images[i].rfind('/')-1)+1:images[i].rfind('/')]
        new_image=str(video_file)+'_'+images[i].split('/')[-1]
        shutil.copy(images[i],f'{path}/{new_image}')

def convert_label(path_txt,path):
    images=[]
    with open(path_txt,'r',encoding='UTF-8',errors='ignore') as f:
        for line in f:
            images.append(line.strip())

    for i in tqdm(range(len(images)),desc='Create label'):
        image=images[i]
        label_json=image[:image.rfind('/')]

        with open(glob.glob(fr"{label_json}/*.json")[0],'r',encoding='utf8')as f:
            json_data = json.load(f)
            if_label=json_data['exist']
            label=json_data['gt_rect']

        size=cv2.imread(image).shape[:2]
        image_id=image.split('/')[-1].split('.')[0]
        video_file=image[image.rfind('/',0,image.rfind('/')-1)+1:image.rfind('/')]
        index=int(image_id)
        image_label_txt=os.path.join(path,f'{video_file}_{image_id}.txt')
        if if_label[index-1]:
            image_label=convert(size,label[index-1])
            with open(image_label_txt,'w',encoding='utf8')as f:
                f.write('0'+' '+str(image_label[0])+' '+str(image_label[1])+' '+str(image_label[2])+' '+str(image_label[3])+'\n')
        else:
            with open(image_label_txt,'w',encoding='utf8')as f:
                f.write('\n')

def copy_json(ori_path,path):
    labels=[]
    with open(ori_path,'r',encoding='UTF-8',errors='ignore') as f:
        for line in f:
            labels.append(line.strip())

    for i in tqdm(range(len(labels)),desc='Copy jsons'):
        label=labels[i]
        video_file=label[label.rfind('/',0,label.rfind('/')-1)+1:label.rfind('/')]
        shutil.copy(label,f'{path}/{video_file}.json')



#读取原数据集，存储路径信息
path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'datasets/orignal_data')
path_txt=os.path.join(os.path.dirname(os.path.dirname(__file__)),'datasets')

path_train=os.path.join(path,'train')
path_test=os.path.join(path,'test')

train_files=[]
test_files=[]
train_images=[]
test_images=[]
train_labels=[]
test_labels=[]

for train_file in os.listdir(path_train):
    train_files.append(os.path.join(path_train,train_file))

for test_file in os.listdir(path_test):
    test_files.append(os.path.join(path_test,test_file))

for file_path in train_files:
    train_images.extend(glob.glob(fr"{file_path}/*.jpg"))
    train_labels.extend(glob.glob(fr"{file_path}/*.json"))

for file_path in test_files:
    test_images.extend(glob.glob(fr"{file_path}/*.jpg"))
    test_labels.extend(glob.glob(fr"{file_path}/*.json"))


path_train_image=os.path.join(path_txt,'train_image.txt')
path_val_image=os.path.join(path_txt,'val_image.txt')
path_test_image=os.path.join(path_txt,'test_image.txt')
path_label=os.path.join(path_txt,'label.txt')


#按4：1分训练集和验证集
np.random.seed(42)
p=0.8
train_index=np.arange(len(train_images))
np.random.shuffle(train_index)
val_index=train_index[int(p*len(train_images)):]
train_index=train_index[:int(p*len(train_images))]


with open(path_train_image,'w',encoding='UTF-8',errors='ignore') as f:
    for image_index in train_index:
        f.write(train_images[image_index]+'\n')

with open(path_val_image,'w',encoding='UTF-8',errors='ignore') as f:
    for image_index in val_index:
        f.write(train_images[image_index]+'\n')

with open(path_test_image,'w',encoding='UTF-8',errors='ignore') as f:
    for image in test_images:
        f.write(image+'\n')  

with open(path_label,'w',encoding='UTF-8',errors='ignore') as f:
    for label in test_labels:
        f.write(label+'\n')  



#得到新数据集目录
path_images=os.path.join(path_txt,'data/images')
path_labels=os.path.join(path_txt,'data/labels')

path_images_train=os.path.join(path_images,'train')
path_images_val=os.path.join(path_images,'val')
path_images_test=os.path.join(path_images,'test')
path_labels_train=os.path.join(path_labels,'train')
path_labels_val=os.path.join(path_labels,'val')
path_labels_test=os.path.join(path_labels,'test')
result_p=os.path.join(os.path.dirname(os.path.dirname(__file__)),'result')

makedir(path_images)
makedir(path_labels)
makedir(path_images_train)
makedir(path_images_val)
makedir(path_images_test)
makedir(path_labels_train)
makedir(path_labels_val)
makedir(path_labels_test)
makedir(result_p)

copy_image(path_train_image,path_images_train)
copy_image(path_val_image,path_images_val)
copy_image(path_test_image,path_images_test)


convert_label(path_train_image,path_labels_train)
convert_label(path_val_image,path_labels_val)

copy_json(path_label,path_labels_test)
copy_json(path_label,result_p)

#生成yaml文件

config={
   "train": path_images_train,
   "val": path_images_val,
   "test": path_images_test,

    # number of classes
   "nc": 1,

    # class names
   "names":['drone']
   
}

with open(os.path.join(path_txt,'config.yaml'), 'w', encoding='utf-8') as f:
   yaml.dump(config, f, Dumper=yaml.RoundTripDumper)


#删除原数据集和中间文件
shutil.rmtree(path)
os.remove(path_train_image)
os.remove(path_val_image)
os.remove(path_test_image)
os.remove(path_label)