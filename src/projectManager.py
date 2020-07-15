import os
from zipfile import ZipFile
from kmlHandler import kmlHandler
from apiSession import apiSession


class projectManager():

    def __init__(self, projectName):
        self.PROJECTNAME = projectName
        self.SRCPATH = os.getcwd() + os.sep
        self.DOWNIMGPATH = os.path.normpath(os.getcwd() + os.sep + os.pardir
                                            + '\\downloadedImages\\') + os.sep
        self.KEYPATH = os.path.normpath(os.getcwd() + os.sep + os.pardir
                                        + '\\ressources\\') + os.sep + 'apiKey.txt'
        self.KMLPATH = os.path.normpath(os.getcwd() + os.sep + os.pardir
                                        + '\\kmlFiles\\{}\\'.format(projectName)) + os.sep + '{}.kml'.format(projectName)
        self.kmlHander = kmlHandler(self.KMLPATH)
        self.api = apiSession(projectName)

    def __CreateDownloadFolder(self):
        os.mkdir(self.DOWNIMGPATH + self.PROJECTNAME)

    def __unZipDownload(self):
        downloadpath = self.DOWNIMGPATH + self.PROJECTNAME
        filename = ''
        for file in os.listdir(downloadpath):
            if file.endswith('.zip'):
                filename = file

        with ZipFile('{}\\{}'.format(downloadpath, filename)) as zip_ref:
            zip_ref.extractall(downloadpath)

        end = filename.find('.zip')

        os.remove('{}\\{}'.format(downloadpath, filename))
        workingFolder = '{}.SAFE'.format(filename[:end])
        granulePath = '{}\\{}\\GRANULE'.format(downloadpath, workingFolder)

        fileL2A = os.listdir(granulePath)[0]
        imagePath = '{}\\{}\\IMG_DATA\\'.format(granulePath, fileL2A)
        return imagePath

        """create Image file location references
        """

    def createImageReference(self, path):

        imageRef = []
        differentResolutions = ['R10m\\', 'R20m\\', 'R60m\\']

        for res in differentResolutions:
            dict = {}
            for file in os.listdir('{}{}'.format(path, res)):
                key = file.split('_')[2]
                dict[key] = '{}{}{}'.format(path, res, file)

            imageRef.append(dict)

        return imageRef

    def getGeoPanda(self):
        return self.kmlHander.getGeoPanda()

    def createProjection(self, projectionType):
        return self.kmlHander.createProjection(projectionType)

    def getFootPrint(self):
        return self.kmlHander.getFootPrint()

    def getGeoDataFrame(self, footprint):
        catalog = self.api.query(footprint)
        return self.api.toGeoDf(catalog)

    def downloadData(self, link):
        self.__CreateDownloadFolder()
        self.api.download(link, self.DOWNIMGPATH + self.PROJECTNAME)
        return self.__handleZippedData()

    def __handleZippedData(self):
        img = self.__unZipDownload()
        return self.createImageReference(img)

        """return dictionnary containing image files location
        """

    def findImageFiles(self):
        path = self.DOWNIMGPATH + self.PROJECTNAME
        firstFolder = os.listdir(path)[0]
        granule = '{}\\{}\\GRANULE\\'.format(path, firstFolder)
        nextFolder = os.listdir(granule)[0]
        finalFolder = '{}{}\\IMG_DATA\\'.format(granule, nextFolder)
        return self.createImageReference(finalFolder)
