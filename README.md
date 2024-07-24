# Recycling Waste Detector with YOLOv8
---
Worked by [Minse Ha](https://github.com/haminse)

Check the full project in [Here](https://github.com/knu-on-plus/Data-generation-solution-for-recycling-waste-classification)

### Problem & Solution

- Sorting recycling waste requires a lot of manpower and time.

- Emerging need for automated waste detection and classification solutions

### Task

- Implement trash detector with recycling waste data from vison AI & Robotics company [WIM](https://www.wimcorp.co.kr/)

<img width="1038" alt="image" src="https://github.com/knu-on-plus/Recycling_Waste_Detector/assets/68217111/7688e1bb-bdb0-491c-95c1-ba7acc28d19c">


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

| params     | value | Functions                      | Reasons                           |
|------------|-------|--------------------------------|-----------------------------------|
| epochs     | 100   | Number of epochs               | Baseline comparison               |
| patience   | 5 or 10 | Early stopping threshold     | Prevent overfitting, stop if no improvement after 5 or 10 epochs |
| shear      | 0.2   | Image shearing                 | Augment dataset with sheared images |
| degrees    | 0.3   | Image rotation                 | Augment dataset with rotated images |
| copy_paste | 0.5   | Randomly segment objects and insert them into other images | Helps model generalize better by creating composite images |
| flipud     | 0.5   | Vertical flipping              | Augment dataset with vertically flipped images |
| fliplr     | 0.5   | Horizontal flipping            | Augment dataset with horizontally flipped images |
| translate  | 0.2   | Image shifting                 | Augment dataset with shifted images |
| batch      | 64    | Batch size for image processing | Efficient use of memory, GPU acceleration, balance between speed and memory usage |
| hsv_v      | 0.6   | Brightness adjustment          | Augment dataset with brightness-varied images |
| hsv_s      | 0.9   | Saturation adjustment          | Augment dataset with saturation-varied images |


- Augmentation Results : Reduces overfitting and improves generalization performance
<img width="540" alt="image" src="https://github.com/knu-on-plus/Trash_Detector/assets/68217111/54ca3395-dd88-4d8f-89d7-3c1f36a22fc1">


### 3. Model Training
- Trained Yolov8 detection model pretrained by COCO dataset
- Conducted to train various size of yolo modes
- Visualized the confusion matrix & F1score

<img width="1017" alt="image" src="https://github.com/knu-on-plus/Trash_Detector/assets/68217111/9b777b08-7d4a-4b80-9055-fb693082260e">


### 4. Final Result

| Model    | F1 score | mAp     | mAp50   |
|----------|----------|---------|---------|
| YOLOv8l  | 0.546260 | 0.417540| 0.603613|
| YOLOv8m  | 0.594815 | 0.438444| 0.617753|
| YOLOv8n  | 0.568087 | 0.342928| 0.533377|
| YOLOv8s  | 0.515948 | 0.376841| 0.528821|
| **YOLOv8x**  | **0.637628** | **0.458198**| **0.620616**|

