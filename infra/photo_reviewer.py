import os
import cv2
import matplotlib.pyplot as plt
from infra.visualizer import Visualizer


def get_all_test_images_and_true_counts(test_dir):
    images_dir = os.path.join(test_dir, 'images')
    labels_dir = os.path.join(test_dir, 'labels')
    all_images = []
    true_counts = []
    for root, _, files in os.walk(images_dir):
        for fname in files:
            if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(root, fname)
                label_name = os.path.splitext(fname)[0] + ".txt"
                label_path = os.path.join(labels_dir, label_name)
                count = 0
                if os.path.exists(label_path):
                    with open(label_path, 'r') as f:
                        for line in f:
                            parts = line.split()
                            if parts and int(parts[0]) in [1, 2]:
                                count += 1
                all_images.append(img_path)
                true_counts.append(count)
    # Sort images and true_counts together
    sorted_pairs = sorted(zip(all_images, true_counts), key=lambda x: x[0])
    sorted_images = [p[0] for p in sorted_pairs]
    sorted_counts = [p[1] for p in sorted_pairs]
    return sorted_images, sorted_counts


from infra.visual_recognition import visual_recognition

class SinglePhotoReviewer(Visualizer):
    def __init__(self):
        super().__init__()
        self.bad_files = []
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)
        self._next = False
        self._mark_bad = False

    def _on_key_press(self, event):
        if event.key == 'enter':
            self._next = True
        elif event.key == 'b':
            print("B PRESSED (marking as bad)")
            self._next = True
            self._mark_bad = True

    def review_photos(self, photo_list, true_counts):
        for idx, (img_path, true_count) in enumerate(zip(photo_list, true_counts)):
            img = cv2.imread(img_path)
            if img is None:
                print(f"Could not read {img_path}")
                continue
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self._next = False
            self._mark_bad = False
            # Run visual recognition
            detection_result = visual_recognition([img_rgb])[0]
            recognized_count = detection_result.get('count', 0)
            # Ensure true_count is int for display
            print(f"True count: {true_count}, Recognized count: {recognized_count}")
            at_light_count = true_count
            self.photo_picker_state = [{'path': img_path, 'true_count': at_light_count}]
            self.display(
                [img_rgb],
                cars_in_intersection=[at_light_count],
                cars_remaining=[0],
                green_light_idx=0,
                detections=[detection_result],
                photo_paths=[img_path],
                recognized_counts=[recognized_count]
            )
            while not self._next:
                plt.pause(0.05)
            if self._mark_bad:
                self.bad_files.append(img_path)
                print(f"Marked bad: {img_path}")
        print("\nBad files collected:")
        for path in self.bad_files:
            print(path)

if __name__ == "__main__":
    test_dir = "./kaggle_data/test"
    images, true_counts = get_all_test_images_and_true_counts(test_dir)
    reviewer = SinglePhotoReviewer()
    reviewer.review_photos(images, true_counts)
