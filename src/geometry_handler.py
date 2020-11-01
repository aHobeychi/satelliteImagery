from shapely import geometry


def remove_third_dimension(points):
    """
    Removes the third dimension from a list of points,
    (x,y,z) -> (x,y)
    """
    reduced_points = []
    for point in points:
        y_dim, x_dim, _ = point
        new_point = (x_dim, y_dim)
        reduced_points.append(new_point)

    return reduced_points


def create_geometry(points):
    """
    Creates a polygon from a list of points.
    """
    poly = geometry.Polygon([[float(p[1]), float(p[0])] for p in points])
    return poly
