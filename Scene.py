import numpy as np
from Ray import Ray
from Sphere import Sphere
from Portal import Portal


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

    def add_light(self, light):
        self.lights.append(light)

    def render_simplified(self, canvas, width, height):
        canvas.delete("all")
        scale = 50
        offset_x = width // 2
        offset_y = height // 2

        for obj in self.objects:
            if isinstance(obj, Sphere):
                x, y, z = obj.center
                r = obj.radius
                color = self.rgb_to_hex(obj.color)
                scale = 50*((0.85)**z)

                screen_x = int(offset_x + x * scale)
                screen_y = int(offset_y - y * scale)
                screen_r = int(r * scale)

                canvas.create_oval(
                    screen_x - screen_r, screen_y - screen_r,
                    screen_x + screen_r, screen_y + screen_r,
                    fill=color, outline=color
                )

        # Render portals
        for portal in self.portals:
            if isinstance(portal, Portal):
                x_a, y_a, z_a = portal.position_a
                x_b, y_b, z_b = portal.position_b
                dir_a = portal.direction_a
                dir_b = portal.direction_b

                scale = 50*((0.85)**z_a)

                screen_x_a = int(offset_x + x_a * scale)
                screen_y_a = int(offset_y - y_a * scale)
                screen_x_b = int(offset_x + x_b * scale)
                screen_y_b = int(offset_y - y_b * scale)
                screen_r = portal.radius*scale

                canvas.create_oval(
                    screen_x_a - screen_r, screen_y_a - screen_r,
                    screen_x_a + screen_r, screen_y_a + screen_r,
                    fill="blue", outline="blue"
                )
                canvas.create_oval(
                    screen_x_b - screen_r, screen_y_b - screen_r,
                    screen_x_b + screen_r, screen_y_b + screen_r,
                    fill="red", outline="red"
                )
                canvas.create_line(
                    screen_x_a, screen_y_a,
                    screen_x_a + int(dir_a[0] * 20), screen_y_a - int(dir_a[1] * 20),
                    fill="cyan"
                )
                canvas.create_line(
                    screen_x_b, screen_y_b,
                    screen_x_b + int(dir_b[0] * 20), screen_y_b - int(dir_b[1] * 20),
                    fill="green"
                )

    def render_full(self, width, height, fov):
        print("Render started")
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

        i, j = np.meshgrid(np.arange(width), np.arange(height), indexing="xy")
        u = i / (width - 1)
        v = j / (height - 1)

        # Compute all ray directions at once
        directions = lower_left_corner + u[..., None] * horizontal + v[..., None] * vertical - camera_origin
        directions /= np.linalg.norm(directions, axis=-1, keepdims=True)

        # Prepare arguments as a list of tuples
        args_list = [(i, j, directions[j, i], camera_origin, self) for j in range(height) for i in range(width)]

        # Use multiprocessing pool
        with Pool() as pool:
            results = pool.map(trace_pixel, args_list)

        # Assign results back to the image
        for i, j, color in results:
            image[height - j - 1, i, :] = color

        return image
    
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
        """Calculate the color at a point based on lights."""
        total_color = np.zeros(3)

        for light in self.lights:
            light_dir = light.position - point
            distance = np.linalg.norm(light_dir)
            light_dir = light_dir / distance

            #Todo uncomment logic

            # shadow_ray = Ray(point + normal * 0.01, light_dir)  # Increased offset
            # shadow_hit, _, _ = self.find_closest_intersection(shadow_ray)

            shadow_hit = False  # Manual override for debugging

            if not shadow_hit:
                dot_product = max(np.dot(normal, light_dir), 0)
                attenuation = 1 / (distance + 1)  # Modified attenuation
                intensity = dot_product * light.intensity * attenuation
                total_color += intensity * obj.color * light.color

            # Debugging print
            # print(f"\n=== SHADING DEBUG ==="
            #       f"\nHit Point: {point}"
            #       f"\nNormal: {normal}"
            #       f"\nObject Color: {obj.color}"
            #       f"\nLight Position: {light.position}"
            #       f"\nLight Direction: {light_dir}"
            #       f"\nDistance to Light: {distance}"
            #       f"\nDot Product (Angle Effect): {dot_product}"
            #       f"\nAttenuation Factor: {attenuation}"
            #       f"\nShadow Hit: {shadow_hit}"
            #       f"\nFinal Intensity: {intensity}"
            #       f"\nAccumulated Color: {total_color}"
            #       f"\n=====================")

        return np.clip(total_color, 0, 1)

    @staticmethod
    def rgb_to_hex(rgb):
        r, g, b = (int(c * 255) for c in rgb)
        return f"#{r:02x}{g:02x}{b:02x}"
