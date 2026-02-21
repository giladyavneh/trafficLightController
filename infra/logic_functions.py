

class TrafficLightState:
    def __init__(self):
        self.timer = 0
        self.current_green = 0


def round_robin_logic(counts: list[int], state: TrafficLightState):
    """Cycles through lanes every 6 ticks, ignoring car counts entirely."""
    state.timer += 1

    if state.timer > 5:
        state.current_green = (state.current_green + 1) % len(counts)
        state.timer = 0

    return state.current_green


def most_cars_logic(counts: list[int], state: TrafficLightState):
    """Always gives green to the lane with the most cars waiting.

    Keeps the current lane green for a minimum of 3 ticks to avoid
    rapid switching that wastes the green-light release rate ramp-up.
    """
    state.timer += 1

    if state.timer >= 3:
        busiest = max(range(len(counts)), key=lambda i: counts[i])
        if busiest != state.current_green:
            state.current_green = busiest
            state.timer = 0

    return state.current_green


def adaptive_timer_logic(counts: list[int], state: TrafficLightState):
    """Round-robin but with a green duration proportional to traffic load.

    Each lane gets a green phase whose length scales with the fraction of
    total traffic it holds.  Minimum phase is 3 ticks, maximum is 12.
    """
    MIN_GREEN = 3
    MAX_GREEN = 12

    if not hasattr(state, 'phase_duration'):
        state.phase_duration = MIN_GREEN

    state.timer += 1

    if state.timer >= state.phase_duration:
        # Move to the next lane
        state.current_green = (state.current_green + 1) % len(counts)
        state.timer = 0

        # Calculate how long the new lane should stay green
        total = sum(counts)
        if total > 0:
            ratio = counts[state.current_green] / total
            state.phase_duration = max(MIN_GREEN, min(MAX_GREEN, round(ratio * MAX_GREEN * len(counts))))
        else:
            state.phase_duration = MIN_GREEN

    return state.current_green


def starvation_aware_logic(counts: list[int], state: TrafficLightState):
    """Greedy approach that picks the busiest lane but prevents starvation.

    Tracks how long each lane has been waiting (red). If any lane has been
    red for more than `MAX_WAIT` ticks, it gets priority regardless of
    its car count. Otherwise the busiest lane wins, with a minimum green
    phase of 3 ticks.
    """
    MAX_WAIT = 15
    MIN_GREEN = 3

    if not hasattr(state, 'wait_times'):
        state.wait_times = [0] * len(counts)

    state.timer += 1

    # Update wait times for all red lanes
    for i in range(len(counts)):
        if i == state.current_green:
            state.wait_times[i] = 0
        else:
            state.wait_times[i] += 1

    if state.timer >= MIN_GREEN:
        # Check for starving lanes first
        starving = [i for i in range(len(counts))
                    if state.wait_times[i] >= MAX_WAIT and counts[i] > 0]

        if starving:
            # Pick the starving lane that has waited the longest
            chosen = max(starving, key=lambda i: state.wait_times[i])
        else:
            # Pick the busiest lane
            chosen = max(range(len(counts)), key=lambda i: counts[i])

        if chosen != state.current_green:
            state.current_green = chosen
            state.timer = 0

    return state.current_green


def proportional_share_logic(counts: list[int], state: TrafficLightState):
    """Allocates green time in proportion to each lane's share of traffic.

    Works in cycles: at the start of each cycle it looks at current counts
    and assigns each lane a number of ticks proportional to its traffic.
    Then it runs through the schedule, giving each non-empty lane its
    allotted time before starting a new cycle.
    """
    MIN_GREEN = 2
    CYCLE_BUDGET = 20

    if not hasattr(state, 'schedule'):
        state.schedule = []
        state.schedule_idx = 0

    state.timer += 1

    # If current schedule is exhausted, build a new one
    if not state.schedule or state.timer >= state.schedule[state.schedule_idx][1]:
        if state.schedule and state.schedule_idx < len(state.schedule) - 1:
            # Move to next lane in the current schedule
            state.schedule_idx += 1
            state.timer = 0
            state.current_green = state.schedule[state.schedule_idx][0]
        else:
            # Build a new schedule based on current counts
            total = sum(counts)
            if total == 0:
                state.schedule = [(state.current_green, MIN_GREEN)]
            else:
                state.schedule = []
                for i in range(len(counts)):
                    if counts[i] > 0:
                        ticks = max(MIN_GREEN, round((counts[i] / total) * CYCLE_BUDGET))
                        state.schedule.append((i, ticks))

                if not state.schedule:
                    state.schedule = [(state.current_green, MIN_GREEN)]

            state.schedule_idx = 0
            state.timer = 0
            state.current_green = state.schedule[0][0]

    return state.current_green