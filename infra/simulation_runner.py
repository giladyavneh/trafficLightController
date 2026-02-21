from typing import NamedTuple, Tuple, List, Callable
from infra.infra import Lane, Intersection
from infra.photo_picker import photo_picker_factory
from infra.visual_recognition import visual_recognition

CARS_FOR_LANE = 300

class SimulationArgs(NamedTuple):
    scenario_name: str
    traffic_rate_range: Tuple[int, int]
    odds_of_traffic: float
    logic_name: str
    traffic_light_logic: Callable[[List[int], object], int]

def run_simulation(args: SimulationArgs, light=True):
    scenario_name, traffic_rate_range, odds_of_traffic, logic_name, traffic_light_logic = args

    lanes = [Lane(CARS_FOR_LANE, traffic_rate_range, odds_of_traffic) for _ in range(4)]
    intersection = Intersection(lanes, traffic_light_logic)
    photo_picker = photo_picker_factory("./kaggle_data/test")

    tick = 0

    while any(lane.cars > 0 for lane in intersection.lanes) or \
          any(ind.current_cars > 0 for ind in intersection.traffic_indicators):

        current_photos = photo_picker.update_images(
            [ind.current_cars for ind in intersection.traffic_indicators]
        )

        detection_results = visual_recognition(current_photos, light=light)
        current_counts = [det['count'] for det in detection_results]
        intersection.update(current_counts)
        tick += 1

    return (scenario_name, logic_name, tick)