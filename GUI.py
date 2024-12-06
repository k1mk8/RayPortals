import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from Scene import Scene
from Portal import Portal
from Sphere import Sphere

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Scene Editor")
        self.scene = Scene()

        self.options_frame = tk.Frame(self.root, width=200, padx=10)
        self.options_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas_width = 600
        self.canvas_height = 400
        self.canvas = tk.Canvas(self.canvas_frame, bg="black", width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.options_frame, text="Add Object").pack(pady=5)
        tk.Button(self.options_frame, text="Add Sphere", command=self.add_sphere_dialog).pack(pady=5)
        tk.Button(self.options_frame, text="Add Portal", command=self.add_portal_dialog).pack(pady=5)
        tk.Button(self.options_frame, text="Render Full Scene", command=self.render_full_scene).pack(pady=20)

        self.param_frame = tk.Frame(self.options_frame)
        self.param_frame.pack(pady=10, fill=tk.X)

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
        portal_a_entry = tk.Entry(self.param_frame)
        portal_a_entry.pack()
        tk.Label(self.param_frame, text="Portal B Position (x, y, z):").pack()
        portal_b_entry = tk.Entry(self.param_frame)
        portal_b_entry.pack()
        tk.Label(self.param_frame, text="Portal A Direction (x, y, z):").pack()
        direction_a_entry = tk.Entry(self.param_frame)
        direction_a_entry.pack()
        tk.Label(self.param_frame, text="Portal B Direction (x, y, z):").pack()
        direction_b_entry = tk.Entry(self.param_frame)
        direction_b_entry.pack()

        def add_portal():
            try:
                pos_a = np.array(eval(portal_a_entry.get()))
                pos_b = np.array(eval(portal_b_entry.get()))
                dir_a = np.array(eval(direction_a_entry.get()))
                dir_b = np.array(eval(direction_b_entry.get()))
                portal = Portal(pos_a, pos_b, dir_a, dir_b)
                self.scene.add_portal(portal)
                messagebox.showinfo("Success", "Portal added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add portal: {e}")

        tk.Button(self.param_frame, text="Add Portal", command=add_portal).pack(pady=5)

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
            self.scene.render(self.canvas, self.canvas_width, self.canvas_height)
            messagebox.showinfo("Info", "Sphere added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def render_full_scene(self):
        """Pełne renderowanie sceny"""
        width, height = 800, 600
        fov = np.pi / 4
        image = self.scene.render_full(width, height, fov)

        plt.imshow(image)
        plt.axis("off")
        plt.show()