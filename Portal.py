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
            new_origin = self.position_b + self.direction_b * 0.01  
            new_direction = self.transform_direction(ray.direction, self.direction_a, self.direction_b)
            print(f"Ray entered Portal A -> B: Origin: {ray.origin}, Direction: {ray.direction}")
            return Ray(new_origin, new_direction)
        elif self.is_ray_entering(ray, self.position_b, self.direction_b):
            new_origin = self.position_a + self.direction_a * 0.01
            new_direction = self.transform_direction(ray.direction, self.direction_b, self.direction_a)
            print(f"Ray entered Portal B -> A: Origin: {ray.origin}, Direction: {ray.direction}")
            return Ray(new_origin, new_direction)

        return None

    def is_ray_entering(self, ray, portal_position, portal_direction):
        to_portal = portal_position - ray.origin
        portal_plane_dist = np.dot(to_portal, portal_direction) / np.linalg.norm(portal_direction)

        is_facing_portal = np.dot(ray.direction, portal_direction) < 0
        is_close_to_plane = abs(portal_plane_dist) < 0.1  
        return is_facing_portal and is_close_to_plane

   
    def transform_direction(self, direction, from_direction, to_direction):
        rotation_matrix = self.calculate_rotation_matrix(from_direction, to_direction)
        transformed_direction = rotation_matrix @ direction
        print(f"Transforming direction {direction} using {from_direction} -> {to_direction}")
        print(f"Transformed direction: {transformed_direction}")
        return transformed_direction


    def calculate_rotation_matrix(self, from_direction, to_direction):
        v = np.cross(from_direction, to_direction)
        s = np.linalg.norm(v)
        c = np.dot(from_direction, to_direction)
        if s == 0:
            return np.identity(3)
        vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        return np.identity(3) + vx + vx @ vx * ((1 - c) / (s ** 2))
