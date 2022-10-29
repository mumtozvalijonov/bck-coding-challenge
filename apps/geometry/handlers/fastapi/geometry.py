from typing import List
from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse

from domain.geometry.dto import PlaneDTO, PointDTO, PolygonDTO
from domain.geometry.errors import ErrInvalidPolygon
from domain.geometry.usecase import UseCase as GeometryUseCase


class GeometryHandler:

    def __init__(self, geometry_usecase: GeometryUseCase):
        self._geometry_usecase = geometry_usecase

    def register(self, app: FastAPI, prefix: str = "/geometry"):
        router = APIRouter()

        router.post("/cut", response_model=List[PointDTO])(
            self.cut_polygon_at_plane)

        app.include_router(router, prefix=prefix)
        app.exception_handler(ErrInvalidPolygon)(self._handle_invalid_polygon)

    async def cut_polygon_at_plane(
        self,
        polygon: PolygonDTO,
        plane: PlaneDTO,
    ) -> List[PointDTO]:
        return await self._geometry_usecase\
            .cut_polygon_at_plane(polygon, plane)

    async def _handle_invalid_polygon(self, request, exc):
        if isinstance(exc, ErrInvalidPolygon):
            return JSONResponse(
                status_code=400,
                content={
                    "message": "Invalid polygon",
                    "details": str(exc),
                },
            )
        else:
            return JSONResponse(
                status_code=500,
                content={
                    "message": "Internal server error",
                    "details": str(exc),
                },
            )
