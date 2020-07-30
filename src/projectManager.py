import os
from zipfile import ZipFile
from kmlHandler import kmlHandler
from apiSession import apiSession


class projectManager():

    def __init__(self, projectName):
        baseFilePath = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        self.PROJECTNAME = projectName
        self.SRCPATH = os.getcwd()
        self.DOWNIMGPATH = os.path.join(baseFilePath, 'downloadedData')
        self.KEYPATH = os.path.join(baseFilePath, 'ressources', 'apiKey.txt')
        self.KMLPATH = os.path.join(
            baseFilePath, 'kmlFiles', projectName, '{}.kml'.format(projectName))
        self.IMGDWN = os.path.join(baseFilePath, 'outputImages', projectName)
        self.CROPPEDIMG = os.path.join(self.IMGDWN, 'cropped')
        self.kmlHander = kmlHandler(self.KMLPATH)
        self.api = apiSession(projectName)

    def __createDownloadFolder(self):
        if os.path.exists(os.path.join(self.DOWNIMGPATH, self.PROJECTNAME)):
            return
        else:
            os.mkdir(os.path.join(self.DOWNIMGPATH, self.PROJECTNAME))

    def __createImageOutputFolder(self):
        if os.path.exists(self.IMGDWN):
            return
        else:
            os.mkdir(self.IMGDWN)

    def __unZipDownload(self):
        downloadpath = os.path.join(self.DOWNIMGPATH, self.PROJECTNAME)
        filename = ''
        for file in os.listdir(downloadpath):
            if file.endswith('.zip'):
                filename = file

        with ZipFile('{}{}{}'.format(downloadpath, os.sep, filename)) as zip_ref:
            zip_ref.extractall(downloadpath)

        end = filename.find('.zip')

        os.remove(os.path.join(downloadpath, filename))

        workingFolder = '{}.SAFE'.format(filename[:end])
        granulePath = os.path.join(downloadpath, workingFolder, 'GRANULE')

        fileL2A = os.listdir(granulePath)[0]
        imagePath = os.path.join(granulePath, fileL2A, 'IMG_DATA')
        return imagePath

    """create Image file location references
    """

    def createImageReference(self, path):

        imageRef = []
        differentResolutions = ['R10m', 'R20m', 'R60m']

        for res in differentResolutions:
            dict = {}
            for file in os.listdir(os.path.join(path, res)):
                key = file.split('_')[2]
                dict[key] = os.path.join(path, res, file)

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
        path = os.path.join(self.DOWNIMGPATH, self.PROJECTNAME)
        firstFolder = os.listdir(path)[0]
        granule = os.path.join(path, firstFolder, 'GRANULE')
        nextFolder = os.listdir(granule)[0]
        finalFolder = os.path.join(granule, nextFolder, 'IMG_DATA')
        self.__createImageOutputFolder()
        return self.createImageReference(finalFolder)

    def getImageFilesPaths(self):
        images = os.listdir(self.IMGDWN)
        results = []
        for image in images:
            if '.tiff' in image:
                results.append(os.path.join(self.IMGDWN, image))

        return results

    def getCroppedImageFilesPaths(self):
        images = os.listdir(os.path.join(self.IMGDWN, 'cropped'))
        results = []
        for image in images:
            if '.tiff' in image:
                results.append(os.path.join(self.IMGDWN, image))

        return results

    def getImagePath(self, imageType, cropped=True):

        imagePath = ''
        if cropped == True:
            path = self.CROPPEDIMG
            listOfFiles = os.listdir(path)
            for f in listOfFiles:
                if imageType.lower() in f.lower():
                    imagePath = os.path.join(path, f)
        else:
            path = self.IMGDWN
            listOfFiles = os.listdir(path)
            for f in listOfFiles:
                if imageType.lower() in f.lower():
                    imagePath = os.path.join(path, f)

        return imagePath
