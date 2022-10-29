from typing import List
from pydantic import BaseModel


class Vector(BaseModel):
    x: float
    y: float
    z: float

    def cross(self, other: 'Vector') -> 'Vector':
        return Vector(
            x=self.y * other.z - self.z * other.y,
            y=self.z * other.x - self.x * other.z,
            z=self.x * other.y - self.y * other.x,
        )

    def dot(self, other: 'Vector') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __mul__(self, other: float) -> 'Vector':
        return Vector(
            x=self.x * other,
            y=self.y * other,
            z=self.z * other,
        )

    __rmul__ = __mul__


class Point(BaseModel):
    x: float
    y: float
    z: float

    def __sub__(self, other: "Point") -> Vector:
        return Vector(
            x=self.x - other.x,
            y=self.y - other.y,
            z=self.z - other.z,
        )

    def __add__(self, vector: Vector) -> "Point":
        return Point(
            x=self.x + vector.x,
            y=self.y + vector.y,
            z=self.z + vector.z,
        )


class Plane(BaseModel):
    p1: Point
    p2: Point
    p3: Point


class Polygon(BaseModel):
    vertices: List[Point]
