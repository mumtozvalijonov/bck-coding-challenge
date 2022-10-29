from typing import List
from pydantic import BaseModel

from domain.geometry import entity


class PointDTO(BaseModel):
    x: float
    y: float
    z: float

    @classmethod
    def from_entity(cls, entity: entity.Point) -> "PointDTO":
        return cls(**entity.dict())

    def to_entity(self) -> entity.Point:
        return entity.Point(**self.dict())


class PlaneDTO(BaseModel):
    p1: PointDTO
    p2: PointDTO
    p3: PointDTO

    @classmethod
    def from_entity(cls, entity: entity.Plane) -> "PlaneDTO":
        return cls(**entity.dict())

    def to_entity(self) -> entity.Plane:
        return entity.Plane(**self.dict())


class PolygonDTO(BaseModel):
    vertices: List[PointDTO]

    @classmethod
    def from_entity(cls, entity: entity.Polygon) -> "PolygonDTO":
        return cls(**entity.dict())

    def to_entity(self) -> entity.Polygon:
        return entity.Polygon(**self.dict())
