import cv2
import os
from sys import argv
import re

dirpath = argv[1]

def get_callback(img, points: list[float]):
    def mouse_callback(event, x, y, flags, param):
        """Handles mouse events and stores up to 4 points."""
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(points) < 4:
                points.append((x, y))
                # Draw a small circle to mark the point on the image
                cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
                cv2.imshow("Image", img)
                print(f"Point {len(points)}: ({x}, {y})")

            if len(points) == 4:
                print("Four points collected:", points)
                
    return mouse_callback

def get_4_points_from_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Could not read image. Check the file path.")
        exit()

    points = []

    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", get_callback(img, points))

    print("Click on the image to select 4 points. Press 'q' to quit.")

    while True:
        cv2.imshow("Image", img)
        key = cv2.waitKey(1) & 0xFF

        # q break the loop
        if key == ord("q"):
            break
    cv2.destroyAllWindows()
    return points

def get_images_prefixs(folder_path: str):
    prefixes = set()
    for filename in os.listdir(folder_path):
        match = re.search(r"^[a-z_]+(?=-?\d)", filename)
        
        if match:
            prefixes.add(match.group())
            
    return list(prefixes)

prefixes = get_images_prefixs(dirpath + "/images")
result = {}
for string in prefixes:
    # find first match
    image_path = next((os.path.join(dirpath, "images", f) for f in os.listdir(os.path.join(dirpath, "images")) if f.startswith(string)), None)
    if image_path:
        points = get_4_points_from_image(image_path)
        print(f"Points for {string}: {points}")