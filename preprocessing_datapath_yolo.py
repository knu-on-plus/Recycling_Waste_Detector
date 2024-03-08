from sklearn.model_selection import train_test_split
import shutil
import os

# Function to read and process YOLO label files
def read_yolo_labels(folder_path):
    label_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'r') as file:
                lines = file.readlines()
                # Process each line in the YOLO label file
                objects = [list(line.strip().split(" "))[0] for line in lines]
                label_data.append({'filename': filename, 'objects': objects})
    return label_data


def random_split(
        data_folder_path = 'new_dataset', 
        train_ratio = 12/20, 
        val_ratio = 3/20, 
        test_ratio = 5/20
    ):
    labels_folder_path = os.path.join(data_folder_path, 'labels')
    label_data = read_yolo_labels(labels_folder_path)
    class_labels = [img_data['objects'] for img_data in label_data]
    filenames = [img['filename'] for img in label_data]
    X_train, X_temp, y_train, y_temp = train_test_split(filenames, class_labels, test_size=(val_ratio + test_ratio), random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=(test_ratio / (val_ratio + test_ratio)), random_state=42)
    
    return X_train, y_train, X_val, y_val, X_test, y_test

def create_folders(base_folder, subfolders):
    for subfolder in subfolders:
        folder_path = os.path.join(base_folder, subfolder)
        os.makedirs(folder_path, exist_ok=True)
        
        # Create subfolders 'images' and 'labels' within each main subfolder
        for sub_subfolder in ['images', 'labels']:
            sub_subfolder_path = os.path.join(folder_path, sub_subfolder)
            os.makedirs(sub_subfolder_path, exist_ok=True)

def make_YOLO_dataset(
        X_train,
        X_val,
        X_test,
        source_directory = 'dataset',
        destination_folder = 'refined_dataset', 
        subfolders = ['train', 'val', 'test'],
    ):
    """
    Convert the original data to YOLO format
    
    Assumed data structure:

        - Original data(Before) :
            - dataset
                - images
                    - image1.jpg
                    - image2.jpg
                    - ...
                - labels
                    - image1.txt
                    - image2.txt
                    - ...

        - Refined data(After) :
            - refined_dataset
                - train
                    - images
                        - image1.jpg
                        - image2.jpg
                        - ...
                    - labels
                        - image1.txt
                        - image2.txt
                        - ...
                - val
                    - images
                        - image1.jpg
                        - image2.jpg
                        - ...
                    - labels
                        - image1.txt
                        - image2.txt
                        - ...
                - test
                    - images
                        - image1.jpg
                        - image2.jpg
                        - ...
                    - labels
                        - image1.txt
                        - image2.txt
                        - ...

    """
    create_folders(destination_folder, subfolders)
    # Iterate through each subfolder and copy files
    for subfolder, file_list in zip(subfolders, [X_train, X_val, X_test]):
        destination_directory = os.path.join(destination_folder, subfolder)
        # # Ensure the destination directory exists
        os.makedirs(destination_directory, exist_ok=True)

        # # Copy files from the source directory to the destination directory
        for file_name in file_list:
            file_name = '.'.join(file_name.split('.')[:-1])
            
            # copy images
            source_file_path = os.path.join(source_directory, 'images', file_name + '.jpg')
            # print(source_file_path)
            destination_file_path = os.path.join(destination_directory, 'images', file_name + '.jpg')
            shutil.copyfile(source_file_path, destination_file_path)
            
            # copy labels
            source_file_path = os.path.join(source_directory, 'labels', file_name + '.txt')
            # print(source_file_path)
            destination_file_path = os.path.join(destination_directory, 'labels', file_name + '.txt')
            shutil.copyfile(source_file_path, destination_file_path)
    print(f"all files are splited from {source_directory} to {destination_folder}")


if __name__ == "__main__":
    # split data in folder new_dataset
    X_train, y_train, X_val, y_val, X_test, y_test = random_split(        
        data_folder_path = 'new_dataset', 
        train_ratio = 12/20, 
        val_ratio = 3/20, 
        test_ratio = 5/20)

    print(
        f"""
        X_train : {len(X_train)}
        y_train : {len(y_train)}
        
        X_val : {len(X_val)}
        y_val : {len(y_val)}
        
        X_test : {len(X_test)}
        y_test : {len(y_test)}
        """
    )
    # make the data to yolo format
    make_YOLO_dataset( X_train, X_val,X_test)
    