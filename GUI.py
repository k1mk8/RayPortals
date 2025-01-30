import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import numpy as np
from Scene import Scene
from Portal import Portal
from Sphere import Sphere
from Light import Light
from PIL import Image, ImageTk

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Scene Editor")
        self.root.geometry("900x600")
        self.root.configure(bg="#2E2E2E")

        self.scene = Scene()

        # Ustawienie stylu
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#2E2E2E")
        self.style.configure("TLabel", background="#2E2E2E", foreground="white", font=("Arial", 12))
        self.style.configure("TButton", background="#444", foreground="white", font=("Arial", 10), padding=5)

        self.options_frame = ttk.Frame(self.root, width=250, padding=10)
        self.options_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas_frame = ttk.Frame(self.root)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas_width = 600
        self.canvas_height = 500
        self.canvas = tk.Canvas(self.canvas_frame, bg="#1E1E1E", width=self.canvas_width, height=self.canvas_height, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(self.options_frame, text="Add Object").pack(pady=5)
        ttk.Button(self.options_frame, text="Add Sphere", command=self.add_sphere_dialog).pack(pady=5, fill=tk.X)
        ttk.Button(self.options_frame, text="Add Portal", command=self.add_portal_dialog).pack(pady=5, fill=tk.X)
        ttk.Button(self.options_frame, text="Add Light", command=self.add_light_dialog).pack(pady=5, fill=tk.X)
        ttk.Button(self.options_frame, text="Render Full Scene", command=self.render_full_scene).pack(pady=10, fill=tk.X)
        ttk.Button(self.options_frame, text="Load Demo Scene", command=self.demo_scene).pack(pady=5, fill=tk.X)
        ttk.Button(self.options_frame, text="Load Scene From File", command=self.load_scene_from_file).pack(pady=5)

        self.param_frame = ttk.Frame(self.options_frame)
        self.param_frame.pack(pady=10, fill=tk.X)

        self.draw_axes()
        

    def add_sphere_dialog(self):
        self.clear_param_frame()

        tk.Label(self.param_frame, text="Sphere Parameters").pack()
        tk.Label(self.param_frame, text="X:").pack()
        self.sphere_x = tk.Entry(self.param_frame)
        self.sphere_x.pack()

        tk.Label(self.param_frame, text="Y:").pack()
        self.sphere_y = tk.Entry(self.param_frame)
        self.sphere_y.pack()

        tk.Label(self.param_frame, text="Z:").pack()
        self.sphere_z = tk.Entry(self.param_frame)
        self.sphere_z.pack()

        tk.Label(self.param_frame, text="Radius:").pack()
        self.sphere_radius = tk.Entry(self.param_frame)
        self.sphere_radius.pack()

        tk.Label(self.param_frame, text="Color (R,G,B):").pack()
        self.sphere_color = tk.Entry(self.param_frame)
        self.sphere_color.pack()

        tk.Button(self.param_frame, text="Add Sphere", command=self.add_sphere).pack(pady=10)
    
    def add_portal_dialog(self):
        self.clear_param_frame()
        tk.Label(self.param_frame, text="Portal A Position (x, y, z):").pack()
        self.portal_a_entry = tk.Entry(self.param_frame)
        self.portal_a_entry.pack()
        tk.Label(self.param_frame, text="Portal B Position (x, y, z):").pack()
        self.portal_b_entry = tk.Entry(self.param_frame)
        self.portal_b_entry.pack()
        tk.Label(self.param_frame, text="Portal A Direction (x, y, z):").pack()
        self.direction_a_entry = tk.Entry(self.param_frame)
        self.direction_a_entry.pack()
        tk.Label(self.param_frame, text="Portal B Direction (x, y, z):").pack()
        self.direction_b_entry = tk.Entry(self.param_frame)
        self.direction_b_entry.pack()
        tk.Button(self.param_frame, text="Add Portal", command=self.add_portal).pack(pady=5)


    def add_portal(self):
        try:
            pos_a = np.array(eval(self.portal_a_entry.get()))
            pos_b = np.array(eval(self.portal_b_entry.get()))
            dir_a = np.array(eval(self.direction_a_entry.get()))
            dir_b = np.array(eval(self.direction_b_entry.get()))
            portal = Portal(pos_a, pos_b, dir_a, dir_b)
            self.scene.add_portal(portal)
            messagebox.showinfo("Success", "Portal added successfully!")
            self.scene.render_simplified(self.canvas, self.canvas_width, self.canvas_height)
            self.draw_axes()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add portal: {e}")

    def add_light_dialog(self):
        self.clear_param_frame()

        tk.Label(self.param_frame, text="Light Parameters").pack()
        tk.Label(self.param_frame, text="X:").pack()
        self.light_x = tk.Entry(self.param_frame)
        self.light_x.pack()

        tk.Label(self.param_frame, text="Y:").pack()
        self.light_y = tk.Entry(self.param_frame)
        self.light_y.pack()

        tk.Label(self.param_frame, text="Z:").pack()
        self.light_z = tk.Entry(self.param_frame)
        self.light_z.pack()

        tk.Label(self.param_frame, text="Intensity:").pack()
        self.light_intensity = tk.Entry(self.param_frame)
        self.light_intensity.pack()

        tk.Label(self.param_frame, text="Color (R,G,B):").pack()
        self.light_color = tk.Entry(self.param_frame)
        self.light_color.pack()

        tk.Button(self.param_frame, text="Add Light", command=self.add_light).pack(pady=10)


    def add_light(self):
        try:
            x = float(self.light_x.get())
            y = float(self.light_y.get())
            z = float(self.light_z.get())
            intensity = float(self.light_intensity.get())
            color = [float(c) for c in self.light_color.get().split(",")]

            if not (0 <= color[0] <= 1 and 0 <= color[1] <= 1 and 0 <= color[2] <= 1):
                raise ValueError("Color values must be between 0 and 1")

            light = Light(position=[x, y, z], intensity=intensity, color=color)
            self.scene.add_light(light)
            self.scene.render_simplified(self.canvas, self.canvas_width, self.canvas_height)

            messagebox.showinfo("Info", "Light added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def clear_param_frame(self):
        for widget in self.param_frame.winfo_children():
            widget.destroy()

    def add_sphere(self):
        try:
            x = float(self.sphere_x.get())
            y = float(self.sphere_y.get())
            z = float(self.sphere_z.get())
            radius = float(self.sphere_radius.get())
            color = [float(c) for c in self.sphere_color.get().split(",")]
            if not (0 <= color[0] <= 1 and 0 <= color[1] <= 1 and 0 <= color[2] <= 1):
                raise ValueError("Color values must be between 0 and 1")
            self.scene.add_object(Sphere([x, y, z], radius, color))
            self.scene.render_simplified(self.canvas, self.canvas_width, self.canvas_height)
            self.draw_axes()
            messagebox.showinfo("Info", "Sphere added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

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

    def render_full_scene(self):
        """Renderuje pełną scenę w lepszej jakości i wyświetla w osobnym oknie"""
        
        width, height = 1920, 1080
        fov = np.pi / 4
        image = self.scene.render_full(width, height, fov)
        image = (image * 255).astype(np.uint8)
        pil_image = Image.fromarray(image)
        
        pil_image = pil_image.resize((1920, 1080), Image.Resampling.LANCZOS)  
        img_window = tk.Toplevel(self.root)
        img_window.title("Rendered Scene")
        self.tk_image = ImageTk.PhotoImage(pil_image)
        label = tk.Label(img_window, image=self.tk_image)
        label.pack()

    def load_scene_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return
        
        try:
            with open(file_path, "r") as file:
                self.scene = Scene()  
                for line in file:
                    parts = line.strip().split()
                    if not parts:
                        continue
                    obj_type = parts[0].lower()
                    
                    if obj_type == "sphere":
                        x, y, z, radius = map(float, parts[1:5])
                        color = list(map(float, parts[5:8]))
                        self.scene.add_object(Sphere([x, y, z], radius, color))
                    elif obj_type == "light":
                        x, y, z, intensity = map(float, parts[1:5])
                        color = list(map(float, parts[5:8]))
                        self.scene.add_light(Light([x, y, z], intensity, color))
                    elif obj_type == "portal":
                        pos_a = np.array(list(map(float, parts[1:4])))
                        pos_b = np.array(list(map(float, parts[4:7])))
                        dir_a = np.array(list(map(float, parts[7:10])))
                        dir_b = np.array(list(map(float, parts[10:13])))
                        radius =   float(parts[13])
                        self.scene.add_portal(Portal(pos_a, pos_b, dir_a, dir_b, radius))
                
                self.scene.render_simplified(self.canvas, self.canvas_width, self.canvas_height)
                self.draw_axes()
                print("loaded scene successfully!")
        except Exception as e:
            print("error")
    def demo_scene(self):
        """Creates an advanced demo scene showcasing portals with multiple lights."""
        self.scene = Scene()

        # Objects
        sphere1 = Sphere(center=np.array([-3, 0, 3]), radius=1, color=np.array([1, 0, 0]))  # Red sphere
        self.scene.add_object(sphere1)

        sphere2 = Sphere(center=np.array([2, -1, 7]), radius=1.5, color=np.array([0, 1, 0]))  # Green sphere
        self.scene.add_object(sphere2)

        sphere3 = Sphere(center=np.array([4, 2, 10]), radius=2, color=np.array([0, 0, 1]))  # Blue sphere
        self.scene.add_object(sphere3)

        # Lights
        light1 = Light(position=np.array([-5, 5, -2]), intensity=15.0, color=np.array([1, 1, 1]))  # White light
        self.scene.add_light(light1)

        light2 = Light(position=np.array([3, 5, 2]), intensity=4.0, color=np.array([1, 0.5, 0]))  # Warm light
        self.scene.add_light(light2)

        light3 = Light(position=np.array([0, -3, 5]), intensity=3.0, color=np.array([0, 0.5, 1]))  # Cool light
        self.scene.add_light(light3)

        # Portals
        # portal_entry_position = np.array([1, 0, 5])
        # portal_entry_direction = np.array([0, 0, 1])

        # portal_exit_position = np.array([-4, 0, 6])
        # portal_exit_direction = np.array([0, 0, -1])

        # portal1 = Portal(portal_entry_position, portal_exit_position, portal_entry_direction, portal_exit_direction, 1)
        # self.scene.add_portal(portal1)

        portal_entry2_position = np.array([4, 1, 5])
        portal_entry2_direction = np.array([-1, 0, 0])

        portal_exit2_position = np.array([-4, 1, 5])
        portal_exit2_direction = np.array([1, 0, 0])

        portal2 = Portal(portal_entry2_position, portal_exit2_position, portal_entry2_direction, portal_exit2_direction, 1)
        self.scene.add_portal(portal2)

        # Render the scene
        self.scene.render_simplified(self.canvas, self.canvas_width, self.canvas_height)
        self.draw_axes()

