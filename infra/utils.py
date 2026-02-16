import os
from collections import defaultdict

def create_photos_dict(images_dir, labels_dir):
    """
    Parses YOLO labels to count cars (class 2) per image.
    Returns: {count: [list_of_image_paths]}
    """
    photos_dict = defaultdict(list)
    
    # 1. Get all image filenames
    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    
    for img_name in image_files:
        # 2. Construct the corresponding label filename
        label_name = os.path.splitext(img_name)[0] + ".txt"
        label_path = os.path.join(labels_dir, label_name)
        
        car_count = 0
        
        # 3. Check if label exists and count class '2' (cars)
        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                for line in f:
                    # YOLO format: <class_id> <x_center> <y_center> <width> <height>
                    parts = line.split()
                    if parts and parts[0] == '2':  # Class 2 is 'car' per your yaml
                        car_count += 1
        
        # 4. Store the path in our dictionary
        full_img_path = os.path.join(images_dir, img_name)
        photos_dict[car_count].append(full_img_path)
            
    return dict(photos_dict)

if __name__ == "__main__":
    # Note: avoid naming your variable 'dict' as it's a built-in Python keyword
    images_path = "../kaggle_data/test/images"
    labels_path = "../kaggle_data/test/labels"
    
    results = create_photos_dict(images_path, labels_path)
        
    for car_count in sorted(results.keys()):
        image_list = results[car_count]
        print(f"{car_count:<3} | {len(image_list)}")

