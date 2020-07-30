import geopandas as gdp
import fiona
import geometryObject


class kmlHandler():

    def __init__(self, filePath=False):
        fiona.supported_drivers['kml'] = 'rw'
        fiona.supported_drivers['KML'] = 'rw'
        fiona.supported_drivers['LIBKML'] = 'rw'
        if filePath != False:
            self.filePath = filePath

    def getGeoPanda(self, filePath=False):
        if filePath == False:
            return gdp.read_file(self.filePath)
        else:
            return gdp.read_file(filePath)

    def createProjection(self, projectionType):
        return gdp.read_file(self.filePath).to_crs(projectionType)

    def setFilePath(self, filePath):
        self.filePath = filePath

    def getFootPrint(self, filePath=False):
        if filePath == False:
            return self.createFootPrint()
        else:
            return self.createFootPrint(filePath)

        """returns a list from a polygon object.
        """

    def polygonToListOfPoints(self, polygon):

        stringRep = str(polygon)
        start = stringRep.find('(')
        stringRep = stringRep[start:]
        stringRep = stringRep.replace('(', '').strip().replace(')', '').strip()
        listOfCoord = stringRep.split(',')

        listOfPoints = []
        for coords in listOfCoord:
            point = []
            point.append(coords.split(' '))
            for p in point:
                if p != '':
                    listOfPoints.append(p)

        return listOfPoints

    """returns dictionnary containing all usefull information of the
        given kml file
    """

    def parseKml(self, filePath):

        information = {}

        with open(filePath, 'r') as myfile:
            data = myfile.read()

        coordStart = data.find('<coordinates>')
        coordEnd = data.find('</coordinates>')
        coords = data[coordStart:coordEnd].replace(
            '<coordinates>', '').strip().split(' ')
        coordinates = []
        for points in coords:
            point = []
            point.append(points.split(','))
            coordinates.append(point[0])

        information['coordinates'] = coordinates

        return information

    def createFootPrint(self, filePath=False):

        if filePath == False:
            parsedKml = self.parseKml(self.filePath)
            listOfCoordinates = geometryObject.\
                removeThridDimension(parsedKml['coordinates'])
            footprint = geometryObject.createGeometry(listOfCoordinates)
            return footprint

        else:
            parsedKml = self.parseKml(filePath)
            listOfCoordinates = geometryObject.\
                removeThridDimension(parsedKml['coordinates'])
            footprint = geometryObject.createGeometry(listOfCoordinates)
            return footprint
