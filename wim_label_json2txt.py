import os
import json
import wim_labels as wim

#for new version wim labels
def convert(orig_path, new_path):
    """
        Purpose : convert wim label(json) to txt label(for YOLO training)
    
        NO REPLACEMENT BUT GENERATE NEW DATA
              
    """
    os.makedirs(new_path, exist_ok=True)
    for label_path in os.listdir(orig_path):
            if label_path.endswith('.json'):
                label_name = os.path.splitext(label_path)[0] # label_name = exclude '.json'
                with open(os.path.join(orig_path, label_path),'r') as file_read:
                    data = json.load(file_read)
                    with open(os.path.join(new_path, label_name) + ".txt", 'w') as file: # new_path(refined_dataset/trian) | label_path = filename
                        for i in range(len(data['annotations'])):
                            # bbox = data['regions'][i]["boundingBox"]
                            bbox = data['annotations'][i]["bbox"]
                            x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]
                            category_id = data['annotations'][i]['category_id']
                            # get class name
                            class_name = None
                            for i in range(len(data['categories'])):
                                if data['categories'][i]["id"] == category_id:
                                    class_name = data['categories'][i]["name"]
                                    break

                            
                            img_w, img_h = data["images"][0]["width"], data["images"][0]["height"]
                            #convert class_name as class number
                            reverse_labels = {v: k for k, v in wim.labels.items()}
                            class_idx = reverse_labels[class_name]
        
                            #get bbox  : x_center, y_center, width, height
                            width, height = x2 - x1, y2 - y1
                            x_center, y_center = (x1 + x2)/2 , (y1 + y2)/2
                            x_center, y_center, width, height = x_center/img_w, y_center/img_h, width/img_w, height/img_h #normalize
                            context = f"{class_idx} {x_center} {y_center} {width} {height}\n"
                            file.write(context)
    return f"The labels converted from {orig_path} to : {new_path}"


if __name__ == "__main__":
    orig_label_path = "new_dataset/orig_labels"
    new_label_path = "new_dataset/labels"
    convert(orig_label_path, new_label_path)