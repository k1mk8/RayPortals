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
            return None, None  # No intersection
    
        # Compute the two intersection points
        t1 = (-b - np.sqrt(discriminant)) / (2 * a)
        t2 = (-b + np.sqrt(discriminant)) / (2 * a)
    
        # Step 1: Reject intersections behind the ray
        if t1 < 0 and t2 < 0:
            return None, None  # The sphere is behind the ray
    
        # Step 2: Ensure the correct hit is returned
        if t1 < 0:  # If t1 is negative, use t2 (entering the sphere)
            return t2, None
        if t2 < 0:  # If t2 is negative, use t1 (exiting the sphere)
            return t1, None
    
        return t1, t2  # Valid intersection