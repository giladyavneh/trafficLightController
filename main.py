from time import sleep, time
import cv2
import os

def load_images_from_folder(folder_path: str, max_images: int):
    images = []
    for filename in sorted(os.listdir(folder_path))[:max_images]:
        path = os.path.join(folder_path, filename)
        img = cv2.imread(path)
        if img is not None:
            images.append(img)
    return images

def carsdetection(num_lights: int, images: list): #BLACK BOX
    return [0] * num_lights



class TrafficLightController:
    def __init__(self, junction_type: str):
        self.junction_type = junction_type

        if junction_type == "t_junction":
            self.num_lights = 6
        elif junction_type == "4_way_junction":
            self.num_lights = 8
        else:
            raise ValueError("Invalid junction type")

        self.lightList = [False] * self.num_lights

    def trafficLightLogic(self, detectedCars: list[int]) -> list[bool]:
        raise NotImplementedError


class Tjunction(TrafficLightController):
    SWITCH_INTERVAL = 5

    def __init__(self):
        super().__init__("t_junction")

        self.states = [
            [3, 5, 0],
            [0, 5, 1],
            [5, 4, 3],
            [2, 0, 3]
        ]

        self.current_state = 0
        self.last_switch_time = time()
        self.set_state(0)

    def choose_state(self, detectedCars):
        loads = [sum(detectedCars[i] for i in state) for state in self.states]
        return loads.index(max(loads))

    def set_state(self, state_index):
        self.lightList = [False] * self.num_lights
        for i in self.states[state_index]:
            self.lightList[i] = True
        self.current_state = state_index
        self.last_switch_time = time()

    def trafficLightLogic(self, detectedCars: list[int]) -> list[bool]:
        if time() - self.last_switch_time >= self.SWITCH_INTERVAL:
            next_state = self.choose_state(detectedCars)
            if next_state != self.current_state:
                self.set_state(next_state)
        return self.lightList


class FourWayJunction(TrafficLightController):
    SWITCH_INTERVAL = 5

    def __init__(self):
        super().__init__("4_way_junction")

        self.states = [
            [0, 3,5,7],
            [2, 3,0],
            [1, 0,7],
            [6,7 ,5]
           ,[3,4 ,5]
        ]

        self.current_state = 0
        self.last_switch_time = time()
        self.set_state(0)

    def choose_state(self, detectedCars):
        loads = [sum(detectedCars[i] for i in state) for state in self.states]
        return loads.index(max(loads))

    def set_state(self, state_index):
        self.lightList = [False] * self.num_lights
        for i in self.states[state_index]:
            self.lightList[i] = True
        self.current_state = state_index
        self.last_switch_time = time()

    def trafficLightLogic(self, detectedCars: list[int]) -> list[bool]:
        if time() - self.last_switch_time >= self.SWITCH_INTERVAL:
            next_state = self.choose_state(detectedCars)
            if next_state != self.current_state:
                self.set_state(next_state)
        return self.lightList


if __name__ == "__main__":
    choice = input("Enter junction type (t / 4): ").strip()
    if choice == "t":
        junction = Tjunction()
    elif choice == "4":
        junction = FourWayJunction()
    else:
        raise ValueError("Invalid junction type")
    image_folder = "images"  
    while True:
        images = load_images_from_folder(image_folder, junction.num_lights)
        detectedCars = carsdetection(
            junction.num_lights,
            images
        )
        junction.trafficLightLogic(detectedCars)
        sleep(1)

     
