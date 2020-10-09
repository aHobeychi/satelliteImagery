import geopandas as gdp
import fiona
import geometryObject


class KmlHandler():

    def __init__(self, filepath=False):
        fiona.supported_drivers['kml'] = 'rw'
        fiona.supported_drivers['KML'] = 'rw'
        fiona.supported_drivers['LIBKML'] = 'rw'
        if filepath is not False:
            self.filepath = filepath

    def get_geo_pandaa(self, filepath=False):
        if filepath is False:
            return gdp.read_file(self.filepath)
        else:
            return gdp.read_file(filepath)

    def create_projection(self, projection_type, file_path):
        return gdp.read_file(file_path).to_crs(projection_type)

    def set_file_path(self, filepath):
        self.file_path = filepath

    def get_foot_print(self, filepath=False):

        if filepath is False:
            return self.create_projection()
        else:
            return self.create_foot_print(filepath)

        """returns a list from a polygon object.
        """

    """returns dictionnary containing all usefull information of the
        given kml file
    """

    def parse_kml(self, filepath):

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

    def create_foot_print(self, filepath=False):

        if filepath is False:
            parsed_kml = self.parseKml(self.filepath)
            list_of_coordinates = (geometryObject.removeThridDimension
                                   (parsed_kml['coordinates']))
            footprint = geometryObject.create_geometry(list_of_coordinates)
            return footprint

        else:
            parsed_kml = self.parse_kml(filepath)
            list_of_coordinates = (geometryObject.remove_third_dimension
                                   (parsed_kml['coordinates']))
            footprint = geometryObject.create_geometry(list_of_coordinates)
            return footprint
