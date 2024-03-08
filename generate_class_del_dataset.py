import os
import shutil

def del_class_and_copy_folder(source_folder, destination_folder, del_class_list):
    os.makedirs(destination_folder, exist_ok=True)

    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)
        destination_path = os.path.join(destination_folder, filename)

        if filename.endswith('.txt'):
            with open(source_path, 'r') as source_file:
                lines_to_copy = [line.strip() for line in source_file.readlines() if not line.strip().split()[0] in map(str, del_class_list)]

            with open(destination_path, 'w') as destination_file:
                destination_file.write('\n'.join(lines_to_copy))

            print(f"Processed text file: {filename}")

        elif filename.endswith('.jpg'):
            shutil.copy(source_path, destination_path)
            print(f"Copied image file: {filename}")

        elif os.path.isdir(source_path):
            del_class_and_copy_folder(source_path, os.path.join(destination_folder, filename), del_class_list)


if __name__ == "__main__":
    source_folder = 'Dataset_bind_16_17_21_24_25_26_27_29_31_32_deleted' # dataset path
    del_classes = [7,20,28]  # the class num to be deleted   
    destination_folder = f'Dataset_{"_".join(map(str, del_classes))}_deleted' 

    del_class_and_copy_folder(source_folder, destination_folder, del_class_list=del_classes)
    # Once you have created the data folder, put only the yaml file in the root of the folder! (Modify only the path at the top of the yaml file)