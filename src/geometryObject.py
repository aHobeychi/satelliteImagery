from shapely import geometry


def remove_third_dimension(points):
    reduced_points = []
    for point in points:
        y, x, z = point
        new_point = (x, y)
        reduced_points.append(new_point)

    return reduced_points


def create_geometry(points):
    poly = geometry.Polygon([[float(p[1]), float(p[0])] for p in points])
    return poly
