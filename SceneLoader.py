import numpy as np
from tkinter import filedialog
from Sphere import Sphere
from Light import Light
from Portal import Portal

class SceneLoader:
    def __init__(self, scene, canvas, canvas_width, canvas_height):
        self.scene = scene
        self.canvas = canvas
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

    def load_scene_from_file(self):
        """Wczytuje scenę z pliku tekstowego."""
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return
        
        try:
            with open(file_path, "r") as file:
                self.canvas.delete("all")
                for line in file:
                    parts = line.strip().split()
                    if not parts:
                        continue

                    obj_type = parts[0].lower()

                    if obj_type == "sphere":
                        self._load_sphere(parts)
                    elif obj_type == "light":
                        self._load_light(parts)
                    elif obj_type == "portal":
                        self._load_portal(parts)

                self.scene.render_simplified(self.canvas, self.canvas_width, self.canvas_height)
                self.draw_axes()
                print("Loaded scene successfully!")
                return self.scene
        except Exception as e:
            print(f"Error loading scene: {e}")

    def draw_axes(self):
        scale = 30
        margin = 50
        origin_x = self.canvas_width - margin
        origin_y = self.canvas_height - margin

        self.canvas.create_line(origin_x, origin_y, origin_x + scale, origin_y, fill="red", arrow="last")
        self.canvas.create_line(origin_x, origin_y, origin_x, origin_y - scale, fill="green", arrow="last")
        self.canvas.create_line(origin_x, origin_y, origin_x - scale, origin_y + scale, fill="blue", arrow="last")

        self.canvas.create_text(origin_x + scale + 10, origin_y, text="X", fill="red", font=("Arial", 10, "bold"))
        self.canvas.create_text(origin_x, origin_y - scale - 10, text="Y", fill="green", font=("Arial", 10, "bold"))
        self.canvas.create_text(origin_x - scale - 10, origin_y + scale + 5, text="Z", fill="blue", font=("Arial", 10, "bold"))    

    def _load_sphere(self, parts):
        """Ładuje kulę ze współrzędnych i dodaje ją do sceny."""
        x, y, z, radius = map(float, parts[1:5])
        color = list(map(float, parts[5:8]))
        self.scene.add_object(Sphere([x, y, z], radius, color))

    def _load_light(self, parts):
        """Ładuje światło i dodaje je do sceny."""
        x, y, z, intensity = map(float, parts[1:5])
        color = list(map(float, parts[5:8]))
        self.scene.add_light(Light([x, y, z], intensity, color))

    def _load_portal(self, parts):
        """Ładuje portal i dodaje go do sceny."""
        pos_a = np.array(list(map(float, parts[1:4])))
        pos_b = np.array(list(map(float, parts[4:7])))
        dir_a = np.array(list(map(float, parts[7:10])))
        dir_b = np.array(list(map(float, parts[10:13])))
        radius = float(parts[13])
        self.scene.add_portal(Portal(pos_a, pos_b, dir_a, dir_b, radius))