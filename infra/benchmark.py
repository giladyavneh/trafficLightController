from infra.infra import Lane, Intersection
from typing import Tuple, List, Callable
from infra.photo_picker import photo_picker_factory
from infra.visual_recognition import visual_recognition
from infra.logic_functions import round_robin_logic

CARS_FOR_LANE = 300

def run_simulation(traffic_rate_range: Tuple[int, int], odds_of_traffic: float, traffic_light_logic: Callable[[List[int], object], int]):
    lanes = [Lane(CARS_FOR_LANE, traffic_rate_range, odds_of_traffic) for _ in range(4)]
    intersection = Intersection(lanes, traffic_light_logic)
    photo_picker = photo_picker_factory("./kaggle_data/test")
    time = 0

    while any(lane.cars > 0 for lane in intersection.lanes) or \
          any(ind.current_cars > 0 for ind in intersection.traffic_indicators):
        
        current_photos = photo_picker.update_images([ind.current_cars for ind in intersection.traffic_indicators])
        current_counts = visual_recognition(current_photos)
        intersection.update(current_counts)
        time += 1
    
    return time

scenarios = [
    { "name": 'Low Traffic', "traffic_rate_range": (1, 7), "odds_of_traffic": 0.5 },
    { "name": 'Medium Traffic', "traffic_rate_range": (2, 9), "odds_of_traffic": 0.6 },
    { "name": 'High Traffic', "traffic_rate_range": (3, 11), "odds_of_traffic": 0.7 }
]

logic_functions = [
    {"name": "Round Robin", "func": round_robin_logic}
]

if __name__ == "__main__":
    results = []
    for scenario in scenarios:
        for logic in logic_functions:
            time = run_simulation(scenario["traffic_rate_range"], scenario["odds_of_traffic"], logic["func"])
            results.append((scenario['name'], logic['name'], time))

    print("\n" + "="*50)
    print(f"{'Scenario':<20} | {'Logic':<15} | {'Time':<10}")
    print("-" * 50)
    for res in results:
        print(f"{res[0]:<20} | {res[1]:<15} | {res[2]:<10}")
    print("="*50)