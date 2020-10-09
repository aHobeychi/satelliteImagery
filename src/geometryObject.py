from shapely import geometry


def removeThridDimension(points):
    reducedPoints = []
    for point in points:
        y, x, z = point
        newPoint = (x, y)
        reducedPoints.append(newPoint)

    return reducedPoints


def createGeometry(points):
    poly = geometry.Polygon([[float(p[1]), float(p[0])] for p in points])
    return poly

    """Returns the coordinate of the top left Corner.
    """
