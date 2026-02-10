import time
from time import sleep
import random

def naive(cars: list[list[int]]):
    print("This is a function in secondery.py")
    index = 0
    # while any list in cars is not empty
    while any(cars):
        activateLight(index, 20, cars)
        index += 1
        index = index % len(cars)

def avg(cars: list[list[int]]):
    print("This is a function in secondery.py")
    index = 0
    timeToshare = 20 * len(cars)
    # while any list in cars is not empty
    while any(cars):
        snapshot = [cars[i][0] if cars[i] else 0 for i in range(len(cars))]
        # calculate time to share for each lane based on the number of cars in the lane (relative to the total number of cars)
        times = [timeToshare * (snapshot[i] / sum(snapshot)) if snapshot[i] > 0 else 0 for i in range(len(cars))] 
        for seconds in times:
            activateLight(index, int(seconds), cars)
            index += 1


def realtime(cars: list[list[int]]):
    print("This is a function in secondery.py")
    index = 0
    # while any list in cars is not empty
    while any(cars):
        traffic = cars[index]
        if traffic:
            traffic.pop(0)
        sleep(1)
        index += 1
        index = index % len(cars)

def activateLight(index: int, seconds: int, cars: list[list[int]]):
    counter = 0
    rand = random.randint(1, 10)
    for i in range(seconds):
        traffic = cars[index]
        if (traffic[0] or 0) != 0 or counter >= rand:
            len(traffic) and traffic.pop(0)
            counter = 0
            rand = random.randint(1, 10)
        else:
            counter += 1
        sleep(1)