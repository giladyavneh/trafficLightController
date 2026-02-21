from infra.infra import Lane, Intersection
from infra.logic_functions import round_robin_logic
from infra.photo_picker import photo_picker_factory
from infra.visualizer import Visualizer
from infra.visual_recognition import visual_recognition

lanes = [Lane(100, (1, 8), 0.6) for _ in range(4)]
intersection = Intersection(lanes, round_robin_logic)
photo_picker = photo_picker_factory("./kaggle_data/test")
visualizer = Visualizer()


visualizer.setup_bad_file_collector()

while any(lane.cars > 0 for lane in intersection.lanes) or \
    any(ind.current_cars > 0 for ind in intersection.traffic_indicators):

    current_photos = photo_picker.update_images([ind.current_cars for ind in intersection.traffic_indicators])
    detection_results = visual_recognition(current_photos)
    photo_paths = [state["path"] for state in photo_picker.current_state]
    recognized_counts = [det['count'] for det in detection_results]
    visualizer.photo_picker_state = photo_picker.current_state
    visualizer.display(
        current_photos,
        cars_in_intersection=[indicator.current_cars for indicator in intersection.traffic_indicators],
        cars_remaining=[lane.cars for lane in intersection.lanes],
        green_light_idx=intersection.green_light_index,
        detections=detection_results,
        photo_paths=photo_paths,
        recognized_counts=recognized_counts
    )
    intersection.update(recognized_counts)
    
    total_waiting = sum(ind.current_cars for ind in intersection.traffic_indicators)
    remaining_in_reservoir = sum(lane.cars for lane in intersection.lanes)    

# After simulation, print bad files
visualizer.print_bad_files()