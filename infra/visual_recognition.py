from typing import List, Any
from ultralytics import RTDETR
from ultralytics import YOLO
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = RTDETR('rtdetr-l.pt') if device == 'cuda' else RTDETR('rtdetr-l.pt')

VALID_CLASSES_LIST = [1, 2, 3, 5]

@torch.inference_mode()
def visual_recognition(current_photos: List[Any]) -> List[int]:
    if not current_photos:
        return []

    results = model(current_photos, 
                    verbose=False, 
                    conf=0.4, 
                    classes=VALID_CLASSES_LIST,
                    half=(device == 'cuda'))

    counts = [len(result.boxes) for result in results]

    return counts