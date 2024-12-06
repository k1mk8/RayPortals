import numpy as np

class Sphere:

    def __init__(self, center, radius, color, is_light=False):
        self.center = np.array(center)
        self.radius = radius
        self.color = np.array(color)
        self.is_light = is_light

    def intersect(self, ray):
        oc = ray.origin - self.center
        a = np.dot(ray.direction, ray.direction)
        b = 2.0 * np.dot(oc, ray.direction)
        c = np.dot(oc, oc) - self.radius ** 2
        discriminant = b ** 2 - 4 * a * c
        if discriminant < 0:
            return None, None
        t1 = (-b - np.sqrt(discriminant)) / (2 * a)
        t2 = (-b + np.sqrt(discriminant)) / (2 * a)
        return t1, t2