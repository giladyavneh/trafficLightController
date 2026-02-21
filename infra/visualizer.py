from matplotlib import pyplot as plt

class Visualizer:
    def setup_bad_file_collector(self):
        self.bad_files = []
        self._key_direction_map = {
            'up': 0,    # North
            'right': 1, # East
            'down': 2,  # South
            'left': 3   # West
        }
        self._last_photo_paths = None
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _on_key_press(self, event):
        if not hasattr(self, '_key_direction_map') or self._last_photo_paths is None:
            return
        direction = self._key_direction_map.get(event.key)
        if direction is not None:
            print(f"{event.key.upper()} PRESSED")
        if direction is not None and self._last_photo_paths and direction < len(self._last_photo_paths):
            path = self._last_photo_paths[direction]
            if path:
                self.bad_files.append(path)
                print(f"Added bad file: {path}")
    def __init__(self):
        # 's' = Photo size. 'm' = Margin from center cluster.
        s = 0.22  
        m = 0.08  
        
        self.img_rects = {
        0: [0.5 - s/2, 0.5 + m,   s, s], # Index 0: North
        1: [0.5 + m,   0.5 - s/2, s, s], # Index 1: East
        2: [0.5 - s/2, 0.5 - m - s, s, s], # Index 2: South (Swapped with 3)
        3: [0.5 - m - s, 0.5 - s/2, s, s]  # Index 3: West (Swapped with 2)
    }
    
        # Update labels to match the index of your input arrays [N, E, S, W]
        self.labels = ["North", "East", "South", "West"]
        
        plt.ion()
        self.fig = plt.figure(figsize=(10, 10))
        self.fig.patch.set_facecolor('#121212') # Dark dashboard theme

    def display(self, images, cars_in_intersection: list[int], cars_remaining: list[int], green_light_idx: int, detections=None, photo_paths=None, recognized_counts=None):
        # Store the latest photo paths for key event handling
        self._last_photo_paths = photo_paths
        if not plt.fignum_exists(self.fig.number):
            return

        self.fig.clf() 
        
        for i in range(len(cars_in_intersection)):
            at_light_count = cars_in_intersection[i]
            reservoir_count = cars_remaining[i]
            rect = self.img_rects[i]
            ax = self.fig.add_axes(rect)
            img = images[i]
            if img is not None:
                ax.imshow(img, aspect='equal')
                # Draw bounding boxes if detections are provided
                if detections is not None and i < len(detections):
                    det = detections[i]
                    boxes = det.get('boxes', [])
                    for j, box in enumerate(boxes):
                        x1, y1, x2, y2 = box
                        width = x2 - x1
                        height = y2 - y1
                        # Draw rectangle
                        rect_patch = plt.Rectangle((x1, y1), width, height, linewidth=2, edgecolor='yellow', facecolor='none', zorder=20)
                        ax.add_patch(rect_patch)
            # Compose debug info
            import os
            fname = os.path.basename(photo_paths[i]) if photo_paths and i < len(photo_paths) and photo_paths[i] else ""
            # Use the count from photo_picker.current_state if available
            vehicles_in_photo = "?"
            if photo_paths and i < len(photo_paths) and photo_paths[i] and hasattr(self, 'photo_picker_state') and self.photo_picker_state:
                # Try to match the photo path to the state
                for state in self.photo_picker_state:
                    if state and 'path' in state and state['path'] == photo_paths[i]:
                        vehicles_in_photo = state.get('true_count', '?')
                        break
            vehicles_recognized = recognized_counts[i] if recognized_counts and i < len(recognized_counts) else "?"
            debug_title = f"{fname}\nvehicles in photo: {vehicles_in_photo}\nvehicles recognized: {vehicles_recognized}"
            # Traffic Light
            light_color = 'lime' if green_light_idx == i else 'red'
            circle = plt.Circle((0.1, 0.9), 0.07, color=light_color, 
                                transform=ax.transAxes, zorder=10)
            ax.add_patch(circle)
            # Show all info at top
            ax.set_title(debug_title, color='yellow', fontsize=9, weight='bold', pad=10)
            ax.axis('off')

            dots_to_draw = min(at_light_count, 144)
            if dots_to_draw > 0:
                l, b, w, h = rect
                q_width = 0.07 
                gap = 0.005
                
                # Logic: [N:0, E:1, S:2, W:3]
                # North (0) and West (3) -> Place queue on the LEFT
                # East (1) and South (2) -> Place queue on the RIGHT
                if i in [0, 3]: 
                    d_rect = [l - q_width - gap, b, q_width, h]
                else:           
                    d_rect = [l + w + gap, b, q_width, h]
                
                dot_ax = self.fig.add_axes(d_rect)
                
                grid_dim = 12
                x_dots = [d // grid_dim for d in range(dots_to_draw)]
                y_dots = [d % grid_dim for d in range(dots_to_draw)]
                
                # If on the left side (N or W), reverse X so they stack "outwards" to the left
                if i in [0, 3]: 
                    x_dots = [grid_dim - x for x in x_dots]

                dot_ax.scatter(x_dots, y_dots, c='orange', s=8, 
                               edgecolors='black', linewidth=0.2)
                
                dot_ax.set_xlim(-1, grid_dim + 1)
                dot_ax.set_ylim(-1, grid_dim + 1)
                dot_ax.axis('off')

        plt.draw()
        plt.pause(0.1)

    def print_bad_files(self):
        print("\nBad files collected:")
        for path in self.bad_files:
            print(path)