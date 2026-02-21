from typing import List, Any
from ultralytics import RTDETR
from ultralytics import YOLO
import torch


device = 'cuda' if torch.cuda.is_available() else 'cpu'
target_names = ['car', 'bus']

def get_model_and_classes(light: bool):
    if light:
        model = YOLO('yolov8n.pt')
    else:
        model = RTDETR('rtdetr-l.pt')
    valid_classes = [id for id, name in model.names.items() if name in target_names]
    return model, valid_classes

@torch.inference_mode()
def visual_recognition(current_photos: List[Any], light: bool = False) -> list:
    if not current_photos:
        return []

    model, valid_classes = get_model_and_classes(light)
    results = model(current_photos, 
                    verbose=False, 
                    conf=0.4, 
                    classes=valid_classes,
                    half=(device == 'cuda'))

    output = []
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy() if hasattr(result.boxes, 'xyxy') else []
        output.append({
            'boxes': boxes,
            'count': len(boxes)
        })
    return output