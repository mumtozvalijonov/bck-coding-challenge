
class ErrInvalidPolygon(Exception):
    pass


class ErrPolygonNotOnXYPlane(ErrInvalidPolygon):
    def __init__(
        self,
        message="Polygon must lie on the XY plane."
    ):
        super().__init__(message)


class ErrPolygonNotConvex(ErrInvalidPolygon):
    def __init__(
        self,
        message="Polygon must be convex."
    ):
        super().__init__(message)


class ErrPlaneNotOrthogonalToPolygon(ErrInvalidPolygon):
    def __init__(
        self,
        message="Plane must be orthogonal to the polygon."
    ):
        super().__init__(message)


class ErrPlaneDoesNotIntersectPolygon(ErrInvalidPolygon):
    def __init__(
        self,
        message="Plane does not intersect the polygon."
    ):
        super().__init__(message)
