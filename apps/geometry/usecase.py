from typing import List

from domain.geometry import entity, errors
from domain.geometry.dto import PointDTO, PolygonDTO, PlaneDTO
from domain.geometry.usecase import UseCase


class UseCase(UseCase):

    async def cut_polygon_at_plane(
        self,
        polygon: PolygonDTO,
        plane: PlaneDTO,
    ) -> List[PointDTO]:
        polygon = polygon.to_entity()
        plane = plane.to_entity()

        # Validate polygon lies on the XY plane
        if not self._is_polygon_on_xy_plane(polygon):
            raise errors.ErrPolygonNotOnXYPlane()

        # Validate the polygon is convex
        if not self._is_polygon_is_convex(polygon):
            raise errors.ErrPolygonNotConvex()

        # Validate plane is orthogonal to the polygon
        if not self._is_plane_orthogonal_to_polygon(plane, polygon):
            raise errors.ErrPlaneNotOrthogonalToPolygon()

        # Iterate over all edges of the polygon and check if they intersect
        # with the plane. If they do, add the intersection point to the list
        # of intersection points.
        intersection_points = []

        for i in range(len(polygon.vertices)):
            p1 = polygon.vertices[i]
            p2 = polygon.vertices[(i + 1) % len(polygon.vertices)]

            # Calculate the intersection point between the edge and the plane
            # and add it to the list of vertices
            intersection_point = self._calculate_intersection_point(
                p1, p2, plane
            )
            if intersection_point is not None and \
                    intersection_point not in intersection_points:
                intersection_points.append(intersection_point)

        if not intersection_points:
            raise errors.ErrPlaneDoesNotIntersectPolygon()
        return intersection_points

    def _calculate_intersection_point(
        self,
        p1: entity.Point,
        p2: entity.Point,
        plane: entity.Plane
    ) -> entity.Point:
        # Calculate the normal of the plane
        v1: entity.Vector = plane.p2 - plane.p1
        v2: entity.Vector = plane.p3 - plane.p1
        plane_normal = v1.cross(v2)

        # Calculate the normal of the edge
        edge_normal = p2 - p1

        # Calculate the dot product of the two normals
        dot_product = plane_normal.dot(edge_normal)

        # If the dot product is 0, the edge is parallel to the plane and
        # does not intersect with the plane
        if dot_product == 0:
            return None

        # Calculate the intersection point
        t = (plane.p1 - p1).dot(plane_normal) / dot_product

        # If t is negative, the intersection point is behind the first vertex
        # of the edge and does not intersect with the plane
        if t < 0:
            return None

        # If t is greater than 1, the intersection point is beyond the second
        # vertex of the edge and does not intersect with the plane
        if t > 1:
            return None

        return p1 + t * edge_normal

    def _is_polygon_on_xy_plane(
        self,
        polygon: entity.Polygon
    ) -> bool:
        for vertex in polygon.vertices:
            if vertex.z != 0:
                return False
        return True

    def _is_polygon_is_convex(
        self,
        polygon: entity.Polygon
    ) -> bool:
        # For each consecutive triple of vertices, calculate the cross product
        # of the vectors between the vertices. If for all cross products the
        # z component is positive or negative, the polygon is convex.
        prev_z = None
        for i in range(len(polygon.vertices)):
            p1 = polygon.vertices[i]
            p2 = polygon.vertices[(i + 1) % len(polygon.vertices)]
            p3 = polygon.vertices[(i + 2) % len(polygon.vertices)]

            v1 = p2 - p1
            v2 = p2 - p3
            cross_product = v1.cross(v2)

            if prev_z is not None and prev_z * cross_product.z < 0:
                return False
            prev_z = cross_product.z
        return True

    def _is_plane_orthogonal_to_polygon(
        self,
        plane: entity.Plane,
        polygon: entity.Polygon
    ) -> bool:
        # Calculate the normal of the plane
        v1: entity.Vector = plane.p2 - plane.p1
        v2: entity.Vector = plane.p3 - plane.p1
        plane_normal = v1.cross(v2)

        # Calculate the normal of the polygon
        v1 = polygon.vertices[1] - polygon.vertices[0]
        v2 = polygon.vertices[2] - polygon.vertices[0]
        polygon_normal = v1.cross(v2)

        # If the dot product of the two normals is 0, the plane is orthogonal
        # to the polygon
        return plane_normal.dot(polygon_normal) == 0
