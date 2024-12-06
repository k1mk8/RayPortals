import numpy as np
from Ray import Ray

class Portal:
    def __init__(self, position_a, position_b, direction_a, direction_b):
        self.position_a = np.array(position_a)
        self.position_b = np.array(position_b)
        self.direction_a = np.array(direction_a) / np.linalg.norm(direction_a)
        self.direction_b = np.array(direction_b) / np.linalg.norm(direction_b)

    def transport_ray(self, ray):
        if self.is_ray_entering(ray, self.position_a, self.direction_a):
            new_origin = self.position_b
            new_direction = self.transform_direction(ray.direction, self.direction_a, self.direction_b)
            return Ray(new_origin, new_direction)
        elif self.is_ray_entering(ray, self.position_b, self.direction_b):
            new_origin = self.position_a
            new_direction = self.transform_direction(ray.direction, self.direction_b, self.direction_a)
            return Ray(new_origin, new_direction)

        return None

    def is_ray_entering(self, ray, portal_position, portal_direction):
        to_portal = portal_position - ray.origin
        is_facing_portal = np.dot(ray.direction, portal_direction) < 0
        is_closer = np.dot(to_portal, portal_direction) > 0
        return is_facing_portal and is_closer

    def transform_direction(self, direction, from_direction, to_direction):
        rotation_matrix = self.calculate_rotation_matrix(from_direction, to_direction)
        return rotation_matrix @ direction

    def calculate_rotation_matrix(self, from_direction, to_direction):
        v = np.cross(from_direction, to_direction)
        s = np.linalg.norm(v)
        c = np.dot(from_direction, to_direction)
        if s == 0:
            return np.identity(3)
        vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        return np.identity(3) + vx + vx @ vx * ((1 - c) / (s ** 2))