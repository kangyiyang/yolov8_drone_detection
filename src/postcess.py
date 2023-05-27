import os
import json
import cv2
from tqdm import tqdm

path_labels=os.path.join(os.path.dirname(os.path.dirname(__file__)),'runs/detect/predict/labels')
result_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'datasets/data/labels/test')
path_image=os.path.join(os.path.dirname(os.path.dirname(__file__)),'datasets/data/images/test')
result_p=os.path.join(os.path.dirname(os.path.dirname(__file__)),'result')


def convert(x,y,w,h,size):
    x,y,w,h=eval(x),eval(y),eval(w),eval(h)
    xmin=int(x*size[0]-w*size[0]/2)
    ymin=int(y*size[1]-h*size[1]/2)
    w=int(w*size[0])
    h=int(h*size[1])
    return [xmin,ymin,w,h]

def convert_json(json_file):
    video_index=json_file[:json_file.rfind('.')]
    result_json=[]
    result_json_index=[]
    for label in os.listdir(path_labels):
        file_index=label[:label.split('.')[0].rfind('_')]
        if video_index==file_index:
            image_path=label.split('.')[0]+'.jpg'
            result_index=label.split('.')[0][label.rfind('_')+1:].lstrip('0')
            with open(os.path.join(path_labels,label),'r',encoding='UTF-8',errors='ignore') as f:
                for line in f:
                    cls,x,y,w,h=(line.strip()).split(' ')
                    size=cv2.imread(os.path.join(path_image,image_path)).shape[:2]
                    result=convert(x,y,w,h,size)
                    result_json.append(result)
                    result_json_index.append(eval(result_index)-1)
    
    with open(os.path.join(result_path,json_file),'r',encoding='utf8')as f:
        json_data = json.load(f)
        res=json_data['res']
        for i in range(1,len(result_json_index)):
            try:
                res.append(result_json[result_json_index.index(i)])
            except:
                res.append([])
        json_data['res']=res
    
    with open(os.path.join(result_p,f'{video_index}.txt'),'w',encoding='utf8')as f:
        f.write(json.dumps(json_data))
                    


json_files=[]
for json_file in os.listdir(result_path):
    json_files.append(json_file)

for i in tqdm(range(len(json_files)),desc='Pred json'):
    convert_json(json_files[i])


