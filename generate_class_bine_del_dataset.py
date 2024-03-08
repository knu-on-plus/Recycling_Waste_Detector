import os
import shutil

def bdel_class_and_copy_folder(source_folder, destination_folder, del_class_list, class_change_map):
    os.makedirs(destination_folder, exist_ok=True)

    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)
        destination_path = os.path.join(destination_folder, filename)

        if filename.endswith('.txt'):
            with open(source_path, 'r') as source_file:
                lines_to_copy = []
                for line in source_file.readlines():
                    line = line.strip()
                    first_word = line.split()[0] if line.split() else None

                    # Check if the line belongs to a class to be changed
                    if first_word in map(str, class_change_map):
                        # Change the class of the line
                        line = line.replace(first_word, class_change_map[first_word])

                    # Check if the line belongs to a class to be deleted
                    if first_word not in map(str, del_class_list):
                        lines_to_copy.append(line)
                                                
            with open(destination_path, 'w') as destination_file:
                destination_file.write('\n'.join(lines_to_copy))

            print(f"Processed text file: {filename}")

        elif filename.endswith('.jpg'):
            shutil.copy(source_path, destination_path)
            print(f"Copied image file: {filename}")

        elif os.path.isdir(source_path):
            bdel_class_and_copy_folder(source_path, os.path.join(destination_folder, filename), del_class_list, class_change_map)


if __name__ == "__main__":
    source_folder = 'final_yolo_dataset'
    del_classes = [16, 17, 21, 24, 25, 26, 27, 29, 31, 32, 7, 20, 28]  #  
    destination_folder = f'Dataset_bind_{"_".join(map(str, del_classes))}_deleted' 
    class_change = {'8':'14', '15':'14', '19':'18', '4':'3', '9' : '12'} # Original class : New class
    bdel_class_and_copy_folder(source_folder, destination_folder, del_class_list=del_classes, class_change_map=class_change)
    # Once you have created the data folder, put only the yaml file in the root of the folder! (Modify only the path at the top of the yaml file)
    
    