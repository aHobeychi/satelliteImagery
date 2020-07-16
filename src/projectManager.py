import os
from zipfile import ZipFile
from kmlHandler import kmlHandler
from apiSession import apiSession


class projectManager():

    def __init__(self, projectName):
        baseFilePath = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        self.PROJECTNAME = projectName
        self.SRCPATH = os.getcwd() + os.sep
        self.DOWNIMGPATH = baseFilePath + '\\downloadedImages\\' + os.sep
        self.KEYPATH = baseFilePath + '\\ressources\\' + os.sep + 'apiKey.txt'
        self.KMLPATH = baseFilePath + '\\kmlFiles\\{}\\'.format(projectName)\
            + os.sep + '{}.kml'.format(projectName)
        self.IMGDWN = baseFilePath + '\\outputImages\\' + projectName + os.sep
        self.kmlHander = kmlHandler(self.KMLPATH)
        self.api = apiSession(projectName)

    def __createDownloadFolder(self):
        if os.path.exists(self.DOWNIMGPATH + self.PROJECTNAME):
            return
        else:
            os.mkdir(self.DOWNIMGPATH + self.PROJECTNAME)

    def __createImageOutputFolder(self):
        if os.path.exists(self.IMGDWN):
            return
        else:
            os.mkdir(self.IMGDWN)

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
        self.__createDownloadFolder()
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
        self.__createImageOutputFolder()
        return self.createImageReference(finalFolder)
