import numpy as np

class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def trace(self, scene, depth=6):

        if depth <= 0:
            return np.array([0, 0, 0])  # Black for max recursion

        closest_t = float("inf")
        closest_obj = None
        closest_portal = None
        hit = False

        # Check for intersections with objects
        obj_hit, obj_t, obj = scene.find_closest_intersection(self)
        if obj_hit and obj_t < closest_t:
            closest_t = obj_t
            closest_obj = obj
            hit = True

        # Check for intersections with portals
        for portal in scene.portals:
            portal_t = portal.intersect(self)
            if portal_t is not None and portal_t < closest_t:
                closest_t = portal_t
                closest_portal = portal
                closest_obj = None
                hit = True

        if hit:
            hit_point = self.origin + closest_t * self.direction

            # If a portal was hit first, transport the ray
            if closest_portal:
                new_ray = closest_portal.transport_ray(self, closest_t)
                if new_ray:
                    return new_ray.trace(scene, depth - 1)

            # Otherwise, shade the object normally
            if closest_obj:
                normal = (hit_point - closest_obj.center) / np.linalg.norm(hit_point - closest_obj.center)
                color = scene.shade(hit_point, normal, closest_obj)
                return np.clip(color, 0, 1)

        return np.array([0, 0, 0])  # Black background if nothing was hit