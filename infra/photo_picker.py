import cv2
import random
from infra.utils import create_photos_dict

import os 

class PhotoPicker:
    def __init__(self, photos_dict: dict):
        self.photos_dict = photos_dict
        self.current_state = [{"img": None, "count": None, "path": None} for _ in range(4)]

    def update_images(self, cars_in_intersection: list[int]):
        """Syncs the photos with the current car counts in the intersection."""
        for i, cars_in_lane in enumerate(cars_in_intersection):
            
            # Only update if the count changed or we have no image
            if cars_in_lane != self.current_state[i]["count"] or self.current_state[i]["img"] is None:
                available = sorted(self.photos_dict.keys())
                # Find closest match in the dataset
                best_key = min(available, key=lambda x: abs(x - cars_in_lane))
                path = random.choice(self.photos_dict[best_key])
                
                new_img = cv2.imread(path)
                if new_img is not None:
                    # Apply the square zoom crop here so it's consistent for all components
                    h, w, _ = new_img.shape
                    dim = min(h, w)
                    zoom = 0.75
                    start_h = int((h - dim * zoom) / 2) + int(h * 0.08)
                    start_w = int((w - dim * zoom) / 2)
                    cropped = new_img[start_h:start_h+int(dim*zoom), 
                                      start_w:start_w+int(dim*zoom)]
                    
                    # Store everything
                    self.current_state[i] = {
                        "img": cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB),
                        "count": cars_in_lane,
                        "path": path # The recognition component might need the raw path
                    }
        return [state["img"] for state in self.current_state]
    
def photo_picker_factory(data_dir: str):
    images_path = os.path.join(data_dir, "images")
    labels_path = os.path.join(data_dir, "labels")
    my_photos_dict = create_photos_dict(images_path, labels_path)
    return PhotoPicker(my_photos_dict)