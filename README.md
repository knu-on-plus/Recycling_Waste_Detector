# Recycling Waste Detector with YOLOv8
---
Worked by [Minse Ha](https://github.com/haminse)

### Problem & Solution

- Sorting recycling waste requires a lot of manpower and time.

- Emerging need for automated waste detection and classification solutions

### Task

- Implement trash detector with recycling waste data from vison AI & Robotics company [WIM](https://www.wimcorp.co.kr/)


### Object information

- Recycling waste objects on a conveyer belt with 30+ classes


---
## About Project

### 1. Exploratory Data Analysis(EDA)
![image](https://github.com/knu-on-plus/Trash_Detector/assets/68217111/ff65c5ca-317e-4e7e-9413-ee01c2d2750d)
- All the class names are encoded by class index due to the privacy concerns
- Huge Data imbalance problem between classes (min = 41, max = 2635)

### 2. Data Preprocessing

#### 2-1. Data Converting
<img width="920" alt="image" src="https://github.com/knu-on-plus/Trash_Detector/assets/68217111/2b6a5e6a-a0e6-40fa-b2f1-347467d95505">

- Convert json labels with YOLO txt file format

- Split data with Train/validation/test set

#### 2-2. Data Augmentation

- Augmentation parameters in yolov8

| Params   | values   | Functions | Reasons |
| ---------| ---------| ----------| --------|
| Cell 1   | Cell 2   |           |         |
| Cell 3   | Cell 4   |           |         |

- Augmentation Results : Reduces overfitting and improves generalization performance
<img width="540" alt="image" src="https://github.com/knu-on-plus/Trash_Detector/assets/68217111/54ca3395-dd88-4d8f-89d7-3c1f36a22fc1">


### 3. Model Training
- Trained Yolov8 detection model pretrained by COCO dataset
- Conducted to train various size of yolo modes
- Visualized the confusion matrix & F1score

<img width="1017" alt="image" src="https://github.com/knu-on-plus/Trash_Detector/assets/68217111/9b777b08-7d4a-4b80-9055-fb693082260e">


### 4. Final Result

| Model   | F1score   | mAP | mAP50 |
| ---------| ---------| ----------| --------|
| Cell 1   | Cell 2   |           |         |
| Cell 3   | Cell 4   |           |         |
