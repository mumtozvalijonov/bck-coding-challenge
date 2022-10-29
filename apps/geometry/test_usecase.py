import unittest

from apps.geometry.usecase import UseCase as GeometryUseCase
from domain.geometry.dto import PlaneDTO, PointDTO, PolygonDTO
from domain.geometry.entity import Plane, Polygon, Point
from domain.geometry.errors import (
    ErrPolygonNotConvex,
    ErrPolygonNotOnXYPlane,
    ErrPlaneNotOrthogonalToPolygon,
    ErrPlaneDoesNotIntersectPolygon
)


class TestGeometryUsecase(unittest.IsolatedAsyncioTestCase):

    async def test__is_polygon_on_xy_plane_true(self):
        usecase = GeometryUseCase()

        polygon = Polygon(
            vertices=[
                Point(x=0, y=0, z=0),
                Point(x=0, y=1, z=0),
                Point(x=1, y=1, z=0),
            ]
        )

        result = usecase._is_polygon_on_xy_plane(polygon)
        self.assertTrue(result)

    async def test__is_polygon_on_xy_plane_false(self):
        usecase = GeometryUseCase()

        polygon = Polygon(
            vertices=[
                Point(x=0, y=0, z=0),
                Point(x=0, y=1, z=0),
                Point(x=1, y=1, z=1),
            ]
        )

        result = usecase._is_polygon_on_xy_plane(polygon)
        self.assertFalse(result)

    async def test__is_polygon_convex_true(self):
        usecase = GeometryUseCase()

        polygon = Polygon(
            vertices=[
                Point(x=0, y=0, z=0),
                Point(x=0, y=1, z=0),
                Point(x=1, y=1, z=0),
            ]
        )

        result = usecase._is_polygon_is_convex(polygon)
        self.assertTrue(result)

    async def test__is_polygon_convex_false(self):
        usecase = GeometryUseCase()

        polygon = Polygon(
            vertices=[
                Point(x=0, y=0, z=0),
                Point(x=0, y=1, z=0),
                Point(x=0.1, y=0.1, z=0),
                Point(x=1, y=0, z=0),
            ]
        )

        result = usecase._is_polygon_is_convex(polygon)
        self.assertFalse(result)

    async def test__is_plane_orthogonal_to_polygon_true(self):
        usecase = GeometryUseCase()

        polygon = Polygon(
            vertices=[
                Point(x=0, y=0, z=0),
                Point(x=0, y=1, z=0),
                Point(x=1, y=1, z=0),
            ]
        )

        plane = Plane(
            p1=Point(x=0, y=0, z=1),
            p2=Point(x=0, y=1, z=0),
            p3=Point(x=0, y=0, z=0),
        )

        result = usecase._is_plane_orthogonal_to_polygon(plane, polygon)
        self.assertTrue(result)

    async def test__is_plane_orthogonal_to_polygon_false(self):
        usecase = GeometryUseCase()

        polygon = Polygon(
            vertices=[
                Point(x=0, y=0, z=0),
                Point(x=0, y=1, z=0),
                Point(x=1, y=1, z=0),
            ]
        )

        plane = Plane(
            p1=Point(x=0, y=0, z=0),
            p2=Point(x=0, y=1, z=0),
            p3=Point(x=1, y=0, z=0),
        )

        result = usecase._is_plane_orthogonal_to_polygon(plane, polygon)
        self.assertFalse(result)

    async def test__calculate_intersection_point(self):
        usecase = GeometryUseCase()

        plane = Plane(
            p1=Point(x=0, y=0, z=0.5),
            p2=Point(x=0, y=1, z=0.5),
            p3=Point(x=1, y=0, z=0.5),
        )
        p1 = Point(x=0, y=0, z=1)
        p2 = Point(x=0, y=0, z=-1)

        result = usecase._calculate_intersection_point(p1, p2, plane)
        self.assertEqual(result, Point(x=0, y=0, z=0.5))

        # The intersection point is not on within the edge
        plane = Plane(
            p1=Point(x=0, y=0, z=5),
            p2=Point(x=0, y=1, z=5),
            p3=Point(x=1, y=0, z=5),
        )
        result = usecase._calculate_intersection_point(p1, p2, plane)
        self.assertIsNone(result)

        plane = Plane(
            p1=Point(x=0, y=0, z=-5),
            p2=Point(x=0, y=1, z=-5),
            p3=Point(x=1, y=0, z=-5),
        )
        result = usecase._calculate_intersection_point(p1, p2, plane)
        self.assertIsNone(result)

        # The segment is parallel to the plane
        plane = Plane(
            p1=Point(x=0, y=0, z=0),
            p2=Point(x=0, y=1, z=0),
            p3=Point(x=0, y=1, z=1),
        )
        result = usecase._calculate_intersection_point(p1, p2, plane)
        self.assertIsNone(result)

    async def test_cut_polygon_at_plane_fails_on_non_xy_plane(self):
        usecase = GeometryUseCase()

        polygon = PolygonDTO(
            vertices=[
                PointDTO(x=0, y=0, z=0),
                PointDTO(x=0, y=1, z=0),
                PointDTO(x=1, y=1, z=1),
            ]
        )

        plane = PlaneDTO(
            p1=PointDTO(x=0, y=0, z=0),
            p2=PointDTO(x=0, y=1, z=0),
            p3=PointDTO(x=1, y=0, z=0),
        )

        with self.assertRaises(ErrPolygonNotOnXYPlane):
            await usecase.cut_polygon_at_plane(polygon, plane)

    async def test_cut_polygon_at_plane_fails_on_non_convex_polygon(self):
        usecase = GeometryUseCase()

        polygon = PolygonDTO(
            vertices=[
                PointDTO(x=0, y=0, z=0),
                PointDTO(x=0, y=1, z=0),
                PointDTO(x=0.1, y=0.1, z=0),
                PointDTO(x=1, y=0, z=0),
            ]
        )

        plane = PlaneDTO(
            p1=PointDTO(x=0, y=0, z=0),
            p2=PointDTO(x=0, y=1, z=0),
            p3=PointDTO(x=1, y=0, z=0),
        )

        with self.assertRaises(ErrPolygonNotConvex):
            await usecase.cut_polygon_at_plane(polygon, plane)

    async def test_cut_polygon_at_plane_fails_on_non_orthogonal_plane(self):
        usecase = GeometryUseCase()

        polygon = PolygonDTO(
            vertices=[
                PointDTO(x=0, y=0, z=0),
                PointDTO(x=0, y=1, z=0),
                PointDTO(x=1, y=1, z=0),
            ]
        )

        plane = PlaneDTO(
            p1=PointDTO(x=0, y=0, z=0),
            p2=PointDTO(x=0, y=1, z=0),
            p3=PointDTO(x=1, y=0, z=0),
        )

        with self.assertRaises(ErrPlaneNotOrthogonalToPolygon):
            await usecase.cut_polygon_at_plane(polygon, plane)

    async def test_cut_polygon_at_plane_fails_on_no_intersection(self):
        usecase = GeometryUseCase()

        polygon = PolygonDTO(
            vertices=[
                PointDTO(x=0.1, y=0.1, z=0),
                PointDTO(x=0.1, y=1, z=0),
                PointDTO(x=1, y=1, z=0),
            ]
        )

        plane = PlaneDTO(
            p1=PointDTO(x=0, y=0, z=0),
            p2=PointDTO(x=0, y=0, z=1),
            p3=PointDTO(x=1, y=0, z=0),
        )

        with self.assertRaises(ErrPlaneDoesNotIntersectPolygon):
            await usecase.cut_polygon_at_plane(polygon, plane)

    async def test_cut_polygon_at_plane(self):
        usecase = GeometryUseCase()

        polygon = PolygonDTO(
            vertices=[
                PointDTO(x=0, y=0, z=0),
                PointDTO(x=0, y=1, z=0),
                PointDTO(x=1, y=1, z=0),
            ]
        )

        plane = PlaneDTO(
            p1=PointDTO(x=0, y=0, z=0),
            p2=PointDTO(x=0, y=0, z=1),
            p3=PointDTO(x=1, y=0.5, z=0),
        )

        result = await usecase.cut_polygon_at_plane(polygon, plane)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], Point(x=0, y=0, z=0))
