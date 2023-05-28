### YOLOv8无人机检测与追踪

#### 环境
1. python:3.7  
2. torch:1.8.1+cu101

#### 运行步骤
1. 环境部署  
git clone https://github.com/kangyiyang/yolov8_drone_detection.git  
2. 下载数据集到datasets文件夹下，使用如下命令解压数据集，然后将无人机检测与追踪文件夹下的内容复制到orignal_data下并删除无人机检测与追踪文件夹  
7z x 无人机检测与追踪.7z
3. 执行数据预处理，打开src下process.py文件，点击运行
4. 使用yolo命令训练数据  
单卡：yolo task=detect mode=train model=yolov8n.pt data=datasets/config.yaml batch=32 epochs=20 imgsz=640 workers=16 device=0  
多卡：yolo task=detect mode=train model=yolov8n.pt data=datasets/config.yaml batch=32 epochs=20 imgsz=640 workers=16 device=\'0,1\'
5. 使用yolo命令验证数据  
yolo task=detect mode=val model=runs/detect/train/weights/best.pt data=datasets/config.yaml device=0  
6. 使用yolo命令预测数据  
yolo task=detect mode=predict model=runs/detect/train/weights/best.pt source=datasets/data/images/test device=0 save_txt=True
7. 执行数据后处理，打开src下的postcess.py文件，点击运行
