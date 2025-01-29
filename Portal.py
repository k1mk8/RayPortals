import numpy as np
from Ray import Ray

class Portal:
    def __init__(self, position_a, position_b, direction_a, direction_b):
        self.position_a = np.array(position_a)
        self.position_b = np.array(position_b)
        self.direction_a = np.array(direction_a) / np.linalg.norm(direction_a)
        self.direction_b = np.array(direction_b) / np.linalg.norm(direction_b)

    def transport_ray(self, ray):
        """Transports a ray from portal A to portal B, maintaining the correct entry position and direction."""

        # Step 1: Compute intersection point with portal A
        denom = np.dot(ray.direction, self.direction_a)
        if abs(denom) < 1e-6:  # Ray is parallel to the portal plane
            return None

        t = np.dot(self.position_a - ray.origin, self.direction_a) / denom
        if t < 0:  # The portal is behind the ray
            return None

        intersection_point = ray.origin + t * ray.direction  # The actual entry point

        # Step 2: Compute the entry offset from portal A's center (ignoring normal component)
        entry_offset = intersection_point - self.position_a
        entry_offset -= np.dot(entry_offset, self.direction_a) * self.direction_a  # Remove normal component

        # Step 3: Compute the exit position using the same offset
        exit_position = self.position_b + entry_offset

        # Step 4: Reflect the ray direction relative to the portal plane
        reflected_direction = ray.direction - 2 * np.dot(ray.direction, self.direction_a) * self.direction_a

        # Step 5: Rotate the reflected direction to match portal B's orientation
        new_direction = self.transform_direction(reflected_direction, self.direction_a, self.direction_b)

        # Debugging print
        print(f"\n=== PORTAL TRANSPORT DEBUG ==="
              f"\nRay Origin: {ray.origin}"
              f"\nRay Direction: {ray.direction}"
              f"\nIntersection Point: {intersection_point}"
              f"\nEntry Offset from Portal Center: {entry_offset}"
              f"\nExit Position: {exit_position}"
              f"\nReflected Direction: {reflected_direction}"
              f"\nNew Direction: {new_direction}"
              f"\nPortal A Position: {self.position_a}"
              f"\nPortal B Position: {self.position_b}"
              f"\n==============================")

        return Ray(exit_position, new_direction)


    def is_ray_entering(self, ray, portal_position, portal_direction):
        to_portal = portal_position - ray.origin
        portal_plane_dist = np.dot(to_portal, portal_direction) / np.linalg.norm(portal_direction)

        is_facing_portal = np.dot(ray.direction, portal_direction) < 0
        is_close_to_plane = abs(portal_plane_dist) < 0.3  # Increased threshold

        return is_facing_portal and is_close_to_plane


    def transform_direction(self, direction, from_direction, to_direction):
        rotation_matrix = self.calculate_rotation_matrix(from_direction, to_direction)
        transformed_direction = rotation_matrix @ direction
        return transformed_direction

    def calculate_rotation_matrix(self, from_direction, to_direction):
        v = np.cross(from_direction, to_direction)
        s = np.linalg.norm(v)
        c = np.dot(from_direction, to_direction)

        if s == 0:
            if c > 0:  
                return np.identity(3)
            else:  
                return -np.identity(3)

        vx = np.array([[0, -v[2], v[1]], 
                       [v[2], 0, -v[0]], 
                       [-v[1], v[0], 0]])

        return np.identity(3) + vx + vx @ vx * ((1 - c) / (s ** 2))
