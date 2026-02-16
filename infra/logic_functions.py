

class TrafficLightState:
    def __init__(self):
        self.timer = 0
        self.current_green = 0

def round_robin_logic(counts: list[int], state: TrafficLightState):
    state.timer += 1

    if state.timer > 5:
        state.current_green = (state.current_green + 1) % len(counts)
        state.timer = 0

    return state.current_green