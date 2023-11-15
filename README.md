<<<<<<< HEAD
# yolov7-tasks
=======
# YOLOv7 Tasks
#### TASK1
- Dataset Cleaning and Formatting:
Simply run the datasetformatter.py inside Dataset_Cleaning_Formatting folder. 
This is a two step process:
--- Data Cleaning: 
    * Checking for valid image files and discarding from dataset if found.
    * Checking for unannotated files
    * Checking for annotations with category id > 79 (our class length is 80)
    * Checking for missing bbox coordinates in annotations
    
    --- Data Formatting: 
    * Normalizing the bounding box coordinates
    * Creating the COCO structure for dataset


- Training:
    - developed on top of https://github.com/WongKinYiu/yolov7/tree/main
    - created a custom.yaml for dataset configuration.
    - wandb has been utilized:
    https://api.wandb.ai/links/mashrukanim/9vxonddt

- Inferencing:

    - Customized the inference script to detect the largest and the smallest object by calculating bounding box areas.
    !(https://ibb.co/2hH5ckW)
    
    - Code to run the inference:
    ```python detect.py --weights runs/train/<path>/best.pt --conf 0.25 --img-size 640 --source <test_image>```

#### TASK2

Altered the __get_item__ function by adding cv2.imwrite statements in the dataloader to output our desired images. For the sake of simplicity, added an extra flag in the training script called --verbose <path_to_output_folder> for easy access to transformed images during training.

Simply run the training script along with the verbose flag and it should output all the intermediary images during training:
python train.py --workers 8 --device 0 --batch-size 32 --data data/custom.yaml --img 640 640 --cfg cfg/training/yolov7-custom.yaml --weights 'yolov7_training.pt' --name yolov7-custom --hyp data/hyp.scratch.custom.yaml --verbose <path_to_output_folder>

#### KEY FINDINGS
* could segmentation polygon coordinates and bbox coordinates can be used for training object detectors in Yolo
>>>>>>> f1d5be46fd06c0488efe5bfdc04e51b6d188324c
