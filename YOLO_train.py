import os
import torch
from ultralytics import YOLO

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]= "0"  # Set the GPU 0 to use
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def train_all_yolo_aug(model_list, data_path, params):
    results = {}
    yaml_path = os.path.join(data_path, "data.yaml") 
    for model_name in model_list:
        model = YOLO(model_name)
        results[model_name] = model.train(
            data=yaml_path, 
            epochs=params['epochs'], 
            patience= params['patience'], #for overfitting
            mixup = params['shear'], # distort imgs
            degrees = params['degrees'], # rotate
            copy_paste = params['copy_paste'], # copy and paste with segment
            flipud = params['flipud'], # vertical flip
            fliplr = params['fliplr'], # horizon filp
            translate = params['translate'], # shifting img
            batch = params['batch'], # bigger batch  
            hsv_v = params['hsv_v'],  # brightness
            hsv_s = params['hsv_s'],  # saturation
            
            )
    
    return results

if __name__ == '__main__':
    
    # data_path = "final_yolo_dataset" #original
    data_path = "Dataset_bind_16_17_21_24_25_26_27_29_31_32_7_20_28_deleted" # dataset path
    
    model_list = ["yolov8x.pt"] # You can add all the models in once ex : ["yolov8x.pt", "yolov8s", "yolov8l"]
    
    default_params = { # Default params
        'epochs' : 100, #same as base
        'patience' : 10, # prevent overfitting
        'shear' : 0.0, # distort imgs (default = 0.0)
        'degrees' : 0.0, # rotation (default = 0.0)
        'copy_paste' : 0.0, # RANDOM copy and paste 50% (default = 0.0)
        'flipud' : 0.5, # horizon flip (default = 0.5)
        'fliplr' : 0.0, # vertical flip (default = 0.0)
        'translate' : 0.1, # shifting (default = 0.1)
        'batch' : 64, # (default = 16)
        'hsv_v' : 0.4, # brightness (default = 0.4)
        'hsv_s' : 0.7, # saturation (default = 0.7)
    }
    
    params = { # For augmentation 
        'epochs' : 100, #same as base
        'patience' : 5, # prevent overfitting
        'shear' : 0.2, # distort imgs (default = 0.0)
        'degrees' : 0.3, # rotation (default = 0.0)
        'copy_paste' : 0.5, # RANDOM copy and paste 50% (default = 0.0)
        'flipud' : 0.5, # horizon flip (default = 0.5)
        'fliplr' : 0.5, # vertical flip (default = 0.0)
        'translate' : 0.2, # shifting (default = 0.1)
        'batch' : 64, # (default = 16)
        'hsv_v' : 0.6, # brightness (default = 0.4)
        'hsv_s' : 0.9, # saturation (default = 0.7)
    }

    results = train_all_yolo_aug(model_list, data_path, params = params)
    print(results)
    print(f"Models {model_list} train completed. the result saved in runs/detect")
    