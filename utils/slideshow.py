import cv2
import os
import time


# Supported image extensions
EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp")





cv2.destroyAllWindows()

def show_images_in_dir(dirname: str, delay: int = 150):
    images = [
        f for f in os.listdir(dirname)
        if f.lower().endswith(EXTENSIONS)
    ]

    for i, img_name in enumerate(images):
        img_path = os.path.join(dirname, img_name)
        img = cv2.imread(img_path)

        if img is None:
            continue

        # attach filename to the image
        cv2.putText(img, dirname + str(i), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Dataset Viewer", img)
        
        # 0.3 seconds = 300 ms
        if cv2.waitKey(delay) & 0xFF == 27:  # ESC to exit early
            break
        
show_images_in_dir("../kaggle_data/test/images", 100)
show_images_in_dir("../kaggle_data/train/images", 100)
show_images_in_dir("../kaggle_data/valid/images", 100)