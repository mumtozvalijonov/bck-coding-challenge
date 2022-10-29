from fastapi import FastAPI
from fastapi.testclient import TestClient
import unittest

from apps.geometry.usecase import UseCase as GeometryUseCase
from apps.geometry.handlers.fastapi.geometry import GeometryHandler
from domain.geometry import errors


class TestGeometryHandler(unittest.IsolatedAsyncioTestCase):
    app: FastAPI
    client: TestClient

    def setUp(self) -> None:
        self.app = FastAPI()
        geometry_handler = GeometryHandler(GeometryUseCase())
        geometry_handler.register(self.app)
        self.client = TestClient(self.app)

        self._normal_payload = {
            "polygon": {
                "vertices": [
                    {"x": 0, "y": 0, "z": 0},
                    {"x": 1, "y": 0, "z": 0},
                    {"x": 0, "y": 1, "z": 0},
                ]
            },
            "plane": {
                "p1": {"x": 0, "y": 0, "z": 0},
                "p2": {"x": 0, "y": 0, "z": 1},
                "p3": {"x": 1, "y": 0, "z": 1}
            }
        }
        self._invalid_polygon_not_on_xy_plane_payload = {
            "polygon": {
                "vertices": [
                    {"x": 0, "y": 0, "z": 0},
                    {"x": 1, "y": 0, "z": 0},
                    {"x": 0, "y": 1, "z": 1},
                ]
            },
            "plane": {
                "p1": {"x": 0, "y": 0, "z": 0},
                "p2": {"x": 0, "y": 0, "z": 1},
                "p3": {"x": 1, "y": 0, "z": 1}
            }
        }
        self._invalid_polygon_not_convex_payload = {
            "polygon": {
                "vertices": [
                    {"x": 0, "y": 0, "z": 0},
                    {"x": 0, "y": 1, "z": 0},
                    {"x": 0.1, "y": 0.1, "z": 0},
                    {"x": 1, "y": 0, "z": 0},
                ]
            },
            "plane": {
                "p1": {"x": 0, "y": 0, "z": 0},
                "p2": {"x": 0, "y": 0, "z": 1},
                "p3": {"x": 1, "y": 0, "z": 1}
            }
        }
        self._invalid_polygon_plane_not_orthogonal_payload = {
            "polygon": {
                "vertices": [
                    {"x": 0, "y": 0, "z": 0},
                    {"x": 0, "y": 1, "z": 0},
                    {"x": 1, "y": 0, "z": 0},
                ]
            },
            "plane": {
                "p1": {"x": 0, "y": 0, "z": 0},
                "p2": {"x": 0, "y": 1, "z": 0},
                "p3": {"x": 1, "y": 0, "z": 0}
            }
        }
        self._invalid_polygon_plane_does_not_intersect_payload = {
            "polygon": {
                "vertices": [
                    {"x": 0, "y": 0, "z": 0},
                    {"x": 0, "y": 1, "z": 0},
                    {"x": 1, "y": 0, "z": 0},
                ]
            },
            "plane": {
                "p1": {"x": 10, "y": 10, "z": 4},
                "p2": {"x": 10, "y": 10, "z": 0},
                "p3": {"x": 10, "y": 0, "z": 0}
            }
        }

    def test_cut_polygon_at_plane(self):
        response = self.client.post(
            "/geometry/cut",
            json=self._normal_payload
        )
        assert response.status_code == 200
        assert response.json() == [
            {"x": 1, "y": 0, "z": 0},
            {"x": 0, "y": 0, "z": 0}
        ]

    def test_cut_polygon_at_plane_fails_on_polygon_not_on_xy_plane(self):
        response = self.client.post(
            "/geometry/cut",
            json=self._invalid_polygon_not_on_xy_plane_payload
        )

        assert response.status_code == 400
        assert response.json()["message"] == "Invalid polygon"
        assert response.json()["details"] == \
            str(errors.ErrPolygonNotOnXYPlane())

    def test_cut_polygon_at_plane_fails_on_polygon_not_convex(self):
        response = self.client.post(
            "/geometry/cut",
            json=self._invalid_polygon_not_convex_payload
        )

        assert response.status_code == 400
        assert response.json()["message"] == "Invalid polygon"
        assert response.json()["details"] == str(errors.ErrPolygonNotConvex())

    def test_cut_polygon_at_plane_fails_on_plane_not_orthogonal(self):
        response = self.client.post(
            "/geometry/cut",
            json=self._invalid_polygon_plane_not_orthogonal_payload
        )

        assert response.status_code == 400
        assert response.json()["message"] == "Invalid polygon"
        assert response.json()["details"] == \
            str(errors.ErrPlaneNotOrthogonalToPolygon())

    def test_cut_polygon_at_plane_fails_on_plane_does_not_intersect(self):
        response = self.client.post(
            "/geometry/cut",
            json=self._invalid_polygon_plane_does_not_intersect_payload
        )

        assert response.status_code == 400
        assert response.json()["message"] == "Invalid polygon"
        assert response.json()["details"] == \
            str(errors.ErrPlaneDoesNotIntersectPolygon())
