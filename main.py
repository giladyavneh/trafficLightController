from time import sleep

def carsdetection(num_lights: int) -> list[int]:
    """Blackbox stub returning zeros (placeholder)."""
    return [0] * num_lights

def trafficLightLogic(previousLights: list[int], detectedCars: list[int]) -> list[int]:
    """Legacy placeholder kept for compatibility."""
    return previousLights


class TrafficLightController:
    # t junctun - 6 lights, 4 way junction - 8 lights, crossway - 1 light
    def __init__(self, junction_type: str):
        self.junction_type = junction_type
        if junction_type == "t_junction":
            self.num_lights = 6
        elif junction_type == "4_way_junction":
            self.num_lights = 8
        elif junction_type == "crossway":
            self.num_lights = 1
        else:
            raise ValueError("Invalid junction type")
        self.lightList = [False] * self.num_lights  # False for red, True for green
        self.lightList[0] = True  # Initial state: first light is green

    
    def trafficLightLogic(self, detectedCars: list[int]) -> list[bool]:
        """Decide next lights. Subclasses should implement this."""
        raise NotImplementedError


class Tjunction(TrafficLightController):
    def __init__(self):
        super().__init__("t_junction")
    
    def trafficLightLogic(self, detectedCars: list[int]) -> list[bool]:  # [counts at each light]
        # simple placeholder rule: if many cars detected at index 4, switch that light
        if len(detectedCars) >= 5 and not self.lightList[4] and detectedCars[4] > 10:
            self.lightList[4] = True
            self.lightList[5] = False
        return self.lightList
    
class FourWayJunction(TrafficLightController):
    def __init__(self):
        super().__init__("4_way_junction")
    
    def trafficLightLogic(self, detectedCars: list[int]) -> list[bool]:
        # placeholder conditions (no-op)
        if self.lightList[0] and self.lightList[4]:
            pass
        if self.lightList[2] and self.lightList[6]:
            pass
        if self.lightList[1] and self.lightList[5]:
            pass
        if self.lightList[3] and self.lightList[7]:
            pass
        return self.lightList
    
class Crossway(TrafficLightController):
    def __init__(self):
        super().__init__("crossway")
    
    def trafficLightLogic(self, detectedCars: list[int]) -> list[bool]:
        # placeholder
        return self.lightList

if __name__ == "__main__":
    # example usage: instantiate one junction and run the loop
    junction = FourWayJunction()
    while True:
        detectedCars = carsdetection(junction.num_lights)
        junction.trafficLightLogic(detectedCars)
        sleep(5)