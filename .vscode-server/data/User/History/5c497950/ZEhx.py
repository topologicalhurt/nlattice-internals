import numpy as np
from models.consts import Types
from shapely.geometry import Point, Polygon


class ray_intersect:

    def __init__(self, mesh: Types.Mesh):
        self._mesh = mesh
    
    def Random_Points_in_Bounds(polygon, number):   
        minx, miny, maxx, maxy = polygon.bounds
        x = np.random.uniform( minx, maxx, number )
        y = np.random.uniform( miny, maxy, number )
        return x, y
