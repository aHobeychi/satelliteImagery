import geopandas as gdp
import fiona
import geometryObject
from shapely.geometry import box


class KmlHandler():

    def __init__(self, filepath=False):
        fiona.supported_drivers['kml'] = 'rw'
        fiona.supported_drivers['KML'] = 'rw'
        fiona.supported_drivers['LIBKML'] = 'rw'
        if filepath is not False:
            self.filepath = filepath

    def get_geo_pandas(self, filepath=False):
        if filepath is False:
            return gdp.read_file(self.filepath)
        else:
            return gdp.read_file(filepath)

    def create_projection(self, projection_type, file_path):
        """
        Creates Projection of the kml file so that it can be used as a polygon to crop
        the raster Images
        """
        return gdp.read_file(file_path).to_crs(projection_type)

    def create_bounding_box(self, projection_type, file_path):
        """
        Creates a bounding box around the kml project so that the images can be cropped 
        without the black boundaries
        """
        projection = self.create_projection(projection_type, file_path)
        # projection.geometry return a dataframe, we want the first row of data
        geometry =  projection.geometry.iloc[0]
        from geopandas import GeoSeries
        
        return GeoSeries(box(*geometry.bounds))
        


    def set_file_path(self, filepath):
        self.file_path = filepath

    def get_foot_print(self, filepath=False):
        """returns a list from a polygon object.
        """

        if filepath is False:
            return self.create_projection()
        else:
            return self.create_foot_print(filepath)


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
