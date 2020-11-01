"""
Handles all kml operations such as as creating the geometry of the imagery
"""
import geopandas as gdp
from geopandas import GeoSeries
import fiona
import geometry_handler
from shapely.geometry import box


class KmlHandler():
    """
    Handles all kml file operations.
    """
    def __init__(self):
        fiona.supported_drivers['kml'] = 'rw'
        fiona.supported_drivers['KML'] = 'rw'
        fiona.supported_drivers['LIBKML'] = 'rw'
        self.file_path = ''

    def get_geo_pandas(self, filepath=False):
        """
        Get Geopanda from kml file.
        """
        if filepath is False:
            return gdp.read_file(self.file_path)
        return gdp.read_file(filepath)

    def create_projection(self, projection_type, file_path):
        """
        Creates Projection of the kml file so that it can be used as a polygon
        to crop the raster Images
        """
        return gdp.read_file(file_path).to_crs(projection_type)

    def create_bounding_box(self, projection_type, file_path):
        """
        Creates a bounding box around the kml project so that the images can
        be cropped without the black boundaries
        """
        projection = self.create_projection(projection_type, file_path)
        geometry = projection.geometry.iloc[0]
        return GeoSeries(box(*geometry.bounds))

    def parse_kml(self, filepath):
        """returns dictionnary containing all usefull information of the
            given kml file
        """
        information = {}

        with open(filepath, 'r') as myfile:
            data = myfile.read()

        coord_start = data.find('<coordinates>')
        coord_end = data.find('</coordinates>')
        coords = data[coord_start:coord_end].replace(
            '<coordinates>', '').strip().split(' ')
        coordinates = []
        for points in coords:
            point = []
            point.append(points.split(','))
            coordinates.append(point[0])

        information['coordinates'] = coordinates

        return information

    def get_foot_print(self):
        """
        Creates footprint from kml file and return it
        """

        parsed_kml = self.parse_kml(self.file_path)
        list_of_coordinates = (geometry_handler.remove_third_dimension
                               (parsed_kml['coordinates']))
        footprint = geometry_handler.create_geometry(list_of_coordinates)
        return footprint
