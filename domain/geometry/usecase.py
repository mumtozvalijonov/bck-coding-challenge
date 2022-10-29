from abc import ABC, abstractmethod
from typing import List

from domain.geometry import dto


class UseCase(ABC):

    @abstractmethod
    async def cut_polygon_at_plane(
        self,
        polygon: dto.PolygonDTO,
        plane: dto.PlaneDTO,
    ) -> List[dto.PointDTO]:
        pass
