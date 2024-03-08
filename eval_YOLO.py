from ultralytics import YOLO
import pandas as pd
import os
import torch
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import wim_labels as wim
from pathlib import Path

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]= "3"  # Set the GPU 2 to use
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print('Device:', device)
print('Current cuda device:', torch.cuda.current_device()) 
print('Count of using GPUs:', torch.cuda.device_count()) 

def yolo_valid(model_path):
    model = YOLO(model_path)
    # Validate the model
    metrics = model.val(split = 'test')  # no arguments needed, dataset and settings remembered
    map = metrics.box.map    # map50-95
    map50 = metrics.box.map50  # map50
    map75 = metrics.box.map75  # map75
    maps = metrics.box.maps   # a list contains map50-95 of each category
    precision = metrics.box.mp
    recall = metrics.box.mr
    f1_score = 2 * (precision * recall) / (precision + recall)
    matrix = metrics.confusion_matrix.matrix
    return [f1_score, map, map50], matrix


# Plot custom confusion matrix after feature engineering(del or bine classes)
def plot_norm_conf_matrix(matrix, 
                          del_class, 
                          save_dir = "norm_conf_matrix",
                          annot = "input_descriptions" # the name of the confusion matrix jpg file
                          ):
    del_class_name = [wim.labels[idx] for idx in del_class]
    mat = pd.DataFrame(matrix)
    # Exclude specified classes
    mat = mat.drop(del_class, axis=0)  # Drop rows
    mat = mat.drop(del_class, axis=1)  # Drop columns

    mat = mat.to_numpy()
    array = mat / ((mat.sum(0).reshape(1, -1) + 1E-9))  # normalize columns
    array[array < 0.007] = np.nan
    # nc = 34 #17
    fig, ax = plt.subplots(1, 1, figsize=(12, 9), tight_layout=True)
    ticklabels = []
    for idx in (list(wim.labels.values()) + ['background']):
        if idx not in del_class_name:
            ticklabels.append(idx)
    # ticklabels = (list(wim.labels.values()) + ['background']) 
    # ticklabels = [label for i, label in enumerate(list(wim.labels.values()) + ['background']) if i not in del_class_name]
    sns.heatmap(array,
                    ax=ax,
                    # annot=nc < 30,
                    annot_kws={
                        'size': 8},
                    cmap='Blues',
                    fmt='.2f',
                    square=True,
                    vmin=0.0,
                    xticklabels=ticklabels,
                    yticklabels=ticklabels).set_facecolor((1, 1, 1))

    title = 'Confusion Matrix Normalized'
    ax.set_xlabel('True')
    ax.set_ylabel('Predicted')
    ax.set_title(title)
    plot_fname = Path(save_dir) / f'{title.lower().replace(" ", "_")}_{annot}.png'
    fig.savefig(plot_fname, dpi=250)
    plt.close(fig)
    return plot_fname

if __name__ == "__main__":
    #evaluate models
    model_list = ["runs/detect/train32/weights/best.pt"] # model path
    annot = "minse_train28_eval_new" # annotation for confusion matrix file name
    results = []
    for i in model_list:
        # val() model with .pt
        rst, matrix = yolo_valid(i)
        results.append(rst)
        
        #Plot Confusion matrix
        del_class = [4, 7, 8, 9, 15, 16, 17, 19, 20, 21, 24, 25, 26, 27, 28, 29, 31, 32] # class index to exclude plotting
        plot_fname = plot_norm_conf_matrix(matrix, del_class = del_class, annot = annot)
        print(f"Confusion Matrix saved in {plot_fname}")
        
    # df = pd.DataFrame(results, columns=['f1score', 'map', 'map50'], index=['l', 'm', 'n', 's', 'x'])
    df = pd.DataFrame(results, columns=['f1score', 'map', 'map50'], index=['x'])    
    print(df)
    df.to_csv("YOLO_test_results", index=False) # save the results
    