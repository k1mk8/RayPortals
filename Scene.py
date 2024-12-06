import numpy as np
from Ray import Ray
from Sphere import Sphere

class Scene:
    def __init__(self):
        self.objects = []
        self.lights = []
        self.portals = []
        self.camera = None

    def add_object(self, obj):
        self.objects.append(obj)

    def add_portal(self, portal):
        self.portals.append(portal)

    def render(self, canvas, width, height):
        canvas.delete("all")
        scale = 100 
        offset_x = width // 2
        offset_y = height // 2

        for obj in self.objects:
            if isinstance(obj, Sphere):
                x, y, z = obj.center
                r = obj.radius
                color = self.rgb_to_hex(obj.color)

                screen_x = int(offset_x + x * scale)
                screen_y = int(offset_y - y * scale)
                screen_r = int(r * scale)

                canvas.create_oval(
                    screen_x - screen_r, screen_y - screen_r,
                    screen_x + screen_r, screen_y + screen_r,
                    fill=color, outline=color
                )

    def render_full(self, width, height, fov):
        aspect_ratio = width / height
        image = np.zeros((height, width, 3))
        camera_origin = np.array([0, 0, -5])
        viewport_height = 2.0
        viewport_width = viewport_height * aspect_ratio
        focal_length = 1.0

        horizontal = np.array([viewport_width, 0, 0])
        vertical = np.array([0, viewport_height, 0])
        lower_left_corner = (
            camera_origin
            - horizontal / 2
            - vertical / 2
            + np.array([0, 0, focal_length])
        )
        for j in range(height):
            for i in range(width):
                u = i / (width - 1)
                v = j / (height - 1)
                direction = lower_left_corner + u * horizontal + v * vertical - camera_origin
                direction = direction / np.linalg.norm(direction)
                ray = Ray(camera_origin, direction)
                color = self.trace_ray(ray)
                image[height - j - 1, i, :] = np.clip(color, 0, 1)
        return image

    def trace_ray(self, ray, depth=5):
        if depth <= 0:
            return np.array([0, 0, 0])
        hit, t_min, obj = self.find_closest_intersection(ray)
        if hit:
            hit_point = ray.origin + t_min * ray.direction
            normal = (hit_point - obj.center) / np.linalg.norm(hit_point - obj.center)
            return self.shade(hit_point, normal, obj)
        for portal in self.portals:
            new_ray = portal.transport_ray(ray)
            if new_ray:
                return self.trace_ray(new_ray, depth - 1)
        return np.array([255, 255, 255])

    def find_closest_intersection(self, ray):
        closest_t = float("inf")
        closest_obj = None
        hit = False
        for obj in self.objects:
            if isinstance(obj, Sphere):
                t1, t2 = obj.intersect(ray)
                if t1 is not None and t1 < closest_t:
                    closest_t = t1
                    closest_obj = obj
                    hit = True
                if t2 is not None and t2 < closest_t:
                    closest_t = t2
                    closest_obj = obj
                    hit = True
        return hit, closest_t, closest_obj

    def shade(self, point, normal, obj):
        light_dir = np.array([1, 1, -1])
        light_dir = light_dir / np.linalg.norm(light_dir)
        intensity = max(np.dot(normal, light_dir), 0)
        return intensity * obj.color

    @staticmethod
    def rgb_to_hex(rgb):
        r, g, b = (int(c * 255) for c in rgb)
        return f"#{r:02x}{g:02x}{b:02x}"