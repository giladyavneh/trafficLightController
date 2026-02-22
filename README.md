# Traffic Flow Simulation - Final Project

## Usage

To install dependencies:
```bash
pip install -r requirements.txt
```


To run the main display simulation:
```bash
python -m infra.display
```

To run the benchmark (CPU or GPU auto-detected):
```bash
python -m infra.benchmark
```

## Project Overview

### Simulation Environment
The simulation models a four-lane intersection. Each lane starts with a fixed volume of vehicles, released into the intersection at random intervals and rates. The simulation measures how many steps are required to clear all traffic.

### Components
- **Lane:** Each lane (N, E, S, W) has a reservoir of vehicles. Cars enter the intersection based on some probability and a random rate per step. In the diplay, the number above each photo indicates how many cars have yet yo enter the intersection.
- **Traffic Indicator:** Controls the release of cars from the intersection. Green lights discharge cars at a rate that increases as the light stays green, simulating real traffic flow. In the display, the orange dots beside each photo represent the number of cars standing in the intersection.
- **Photo Picker:** Selects labeled photos matching the current car count for each lane, bridging the simulation and visual recognition.
- **Visual Recognition:** Processes intersection photos to estimate car counts, using deep learning models. The best-performing model was a transformer-based detector (`rtdetr-l.pt`).
- **Traffic Light Logic:** Receives car counts and decides which lane gets the green light. Multiple logic functions are implemented and compared.

### Traffic Light Logic Functions
1. **Round Robin:** Cycles through lanes in fixed order, each gets equal green time.
2. **Most Cars (no max):** Always gives green to the busiest lane, can starve others.
3. **Most Cars (with max):** Adds a cap to green time, forces switches.
4. **Adaptive Timer:** Green duration proportional to traffic share.
5. **Starvation Aware:** Prioritizes lanes waiting too long.
6. **Proportional Share:** Allocates green ticks proportionally, guarantees minimum for each lane.

### Model Comparison & Results
We compared four models; the transformer-based model (`rtdetr-l.pt`) had the best accuracy and reasonable speed (<2s per image). The optimal confidence threshold was 0.4, yielding an F1 score of 0.57 and nearly perfect count ratio.

#### Example Results (Strong Model)
| Scenario      | Logic                        | Time |
|-------------- |----------------------------- |------|
| Low Traffic   | Round Robin                  | 170  |
| Low Traffic   | Most Cars w/ Max Green Time  | 161  |
| Low Traffic   | Starvation Aware             | 162  |
| Medium Traffic| Adaptive Timer               | 122  |
| High Traffic  | Adaptive Timer               | 119  |

#### Example Results (Weak Model)
| Scenario      | Logic                        | Time |
|-------------- |----------------------------- |------|
| Low Traffic   | Round Robin                  | 207  |
| Low Traffic   | Most Cars w/ Max Green Time  | 600  |
| Medium Traffic| Round Robin                  | 138  |
| High Traffic  | Most Cars w/ Max Green Time  | 600  |

## Structure

- `infra/`: Core simulation, logic, visualization, and benchmarking modules.
- `kaggle_data/`: Test images and labels for visual recognition.
- `model_research/`: Notebooks and CSVs for model comparison and tuning.
