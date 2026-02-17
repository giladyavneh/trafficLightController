from typing import List, Any
from ultralytics import RTDETR

model = RTDETR('rtdetr-l.pt')

# 1: bicycle, 2: car, 3: motorcycle, 5: bus
VALID_CLASSES = {1, 2, 3, 5}

def visual_recognition(current_photos: List[Any]) -> List[int]:
    if not current_photos:
        return []

    counts = []
    for photo in current_photos:
        results = model(photo, verbose=False, conf=0.4)
        count = 0
        for result in results:
            for box in result.boxes:
                if int(box.cls[0]) in VALID_CLASSES:
                    count += 1
        counts.append(count)

    return counts
