
# STCrowd

 This repository is for STCrowd dataset and official implement for **STCrowd: A Multimodal Dataset for Pedestrian Perception in Crowded Scenes**.

## Dataset 
Our website can be download from the [Homepage](https://4dvlab.github.io).

Also the dataset can be directly download from [STCrowd DATA](https://drive.google.com/file/d/1cw8Ats2jYSkUK-g-5lumF2pY_NKSehKS/view?usp=sharing) .

To achieve good cross-modal data alignment between different sensors, the timestamp of the LiDAR is the time when the full rotation of current frame is achieved and the correspond of timestamps for different devices is achieved by special posture when recording data. We keep the common frequency as 5 Hz and annotate the frames per 0.4 second.(The raw data extracted the timestamp information directly from ros, so the image timestamp and liDAR would be different in name due to ROS delay, but we took this delay into account in synchronization to complete the corresponding (corresponding in JSON file).)

The original annotation result is saved in 'SEQUENCE_NUM.json' for each continuous sequence,

We provide high-quality manually labeled ground truth for both LiDAR point clouds and images. For annotations in point clouds, we labeled each pedestrian using a 3D bounding box , where  denotes the center coordinates and  are the length, width, and height along the x-axis,y-axis and z-axis, respectively. Pedestrians with fewer than 15 points in the LiDAR point cloud are not annotated. For annotations of images, besides 3D bounding box, we also label the 2D bounding box with  for general 2D detection and tracking. For the objects captured by both the camera and LiDAR, we annotate the joint ID in sequences, which facilitates tracking and sensor-fusion tasks. The frequency of our annotation is 2.5HZ. We also provide annotations for the level of density and occlusion(more details in paper). Since the 3D bounding boxes in images are not directly derived from LiDAR point cloud, all objects have their own annotations but may lack corresponding information in point cloud/images. For tracking task, each sequence group has a variable number of continuously recorded frames with the group id, ranging from 50 to 800 (which is from 20s to 320s), the same object appear in continuous frame has consistent.

Humans with fewer than 15 points are not annotated and the point cloud annotation is conducted within the range of 35 meters. With the straight front of the camera as the reference direction, only the left and right 90° are labeled, result in the point cloud data within the range of 180° are labeled.

For more details, we include in sample.json.


## Installation

### Requirements
- PyTorch
- yaml
- mmcv
- mmdet
- mmdet3d
- mmpycocotools

## Data Preparation
The original annotation result is saved in **SEQUENCE_NUM.json** for each continuous sequence, for more details, we include in **anno/sample.json**.

Please prepare the dataset as following folder struction:

```
./
└── Path_To_STCrowd/
    ├──split.json
    ├──anno
        ├── 1.json
        ├── 2.json
        └── ...
    ├── left        
        ├── 1	
        |   ├── XXX.jpg
        |   ├── XXX.jpg
        │   └── ...
        ├── 2 
        ├── ...
    ├── right    
        ├── 1	
        |   ├── XXX.jpg
        |   ├── XXX.jpg
        │   └── ...
        ├── 2 
        ├── ...
    ├── pcd        
        ├── 1	
        |   ├── XXX.bin
        |   ├── XXX.bin
        │   └── ...
        ├── 2 
            ├── XXX.bin
            ├── XXX.bin
            └── ...
```
## Dataset convert
We provide the convert code for data converting.
eg. convert for **STCrowd_infos_train.pkl**.
```
python STCrowd_conver.py --path  Path_To_STCrowd --split 'train'
```

##  License:
All datasets are published under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 License.
This means that you must attribute the work in the manner specified by the authors, you may not use this work for commercial purposes and if you alter, transform, or build upon this work, you may distribute the resulting work only under the same license. 
