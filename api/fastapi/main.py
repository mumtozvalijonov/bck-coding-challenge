from fastapi import FastAPI

from apps.geometry.usecase import UseCase as GeometryUseCase
from apps.geometry.handlers.fastapi.geometry import GeometryHandler


app = FastAPI()

geometry_usecase = GeometryUseCase()
geometry_handler = GeometryHandler(geometry_usecase)
geometry_handler.register(app)
