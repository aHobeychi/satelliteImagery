import os
from zipfile import ZipFile
from kmlHandler import kmlHandler
from apiSession import apiSession


class ProjectManager():

    def __init__(self, projectname):
        basefilepath = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        self.PROJECTNAME = projectname
        self.SRCPATH = os.getcwd()
        self.DOWNIMGPATH = os.path.join(basefilepath, 'downloadedData')
        self.KEYPATH = os.path.join(basefilepath, 'ressources', 'apiKey.txt')
        self.KMLPATH = os.path.join(
            basefilepath, 'kmlFiles', projectname, '{}.kml'.format(projectname))
        self.IMGDWN = os.path.join(basefilepath, 'outputImages', projectname)
        self.CLASSIMG = os.path.join(
            basefilepath, 'classification', projectname)
        self.CROPPEDIMG = os.path.join(self.IMGDWN, 'cropped')
        self.kmlHander = kmlHandler(self.KMLPATH)
        self.api = apiSession(projectname)
        self.createClassificationFolder()

    def createDownloadFolder(self):
        if os.path.exists(os.path.join(self.DOWNIMGPATH, self.PROJECTNAME)):
            return
        else:
            os.mkdir(os.path.join(self.DOWNIMGPATH, self.PROJECTNAME))

    def createClassificationFolder(self):
        if os.path.exists(self.CLASSIMG):
            return
        else:
            os.mkdir(self.CLASSIMG)

    def createImageOutputFolder(self):
        if os.path.exists(self.IMGDWN):
            return
        else:
            os.mkdir(self.IMGDWN)

    def unzipDownload(self):
        downloadpath = os.path.join(self.DOWNIMGPATH, self.PROJECTNAME)
        filename = ''
        for current_file in os.listdir(downloadpath):
            if current_file.endswith('.zip'):
                filename = current_file

        with ZipFile('{}{}{}'.format(downloadpath, os.sep, filename)) as zip_ref:
            zip_ref.extractall(downloadpath)

        end = filename.find('.zip')

        os.remove(os.path.join(downloadpath, filename))

        working_folder = '{}.SAFE'.format(filename[:end])
        granule_path = os.path.join(downloadpath, working_folder, 'GRANULE')

        file_l2a = os.listdir(granule_path)[0]
        image_path = os.path.join(granule_path, file_l2a, 'IMG_DATA')
        return image_path

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

    def getImagePaths(self):

        return references

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
        self.createDownloadFolder()
        self.api.download(link, self.DOWNIMGPATH + os.sep + self.PROJECTNAME)
        # return self.handleZippedData()

    def handleZippedData(self):
        img = self.unzipDownload()
        return self.createImageReference(img)

    """return dictionnary containing image files location
    """

    def findImageFiles(self):
        path = os.path.join(self.DOWNIMGPATH, self.PROJECTNAME)
        firstFolder = os.listdir(path)[0]
        granule = os.path.join(path, firstFolder, 'GRANULE')
        nextFolder = os.listdir(granule)[0]
        finalFolder = os.path.join(granule, nextFolder, 'IMG_DATA')
        self.createImageOutputFolder()
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
                    if 'png' in f or 'jpg' in f:
                        continue
                    imagePath = os.path.join(path, f)
        else:
            path = self.IMGDWN
            listOfFiles = os.listdir(path)
            for f in listOfFiles:
                if imageType.lower() in f.lower():
                    if 'png' in f or 'jpg' in f:
                        continue
                    imagePath = os.path.join(path, f)

        return imagePath

    def getClassificationPath(self, filename):

        return self.CLASSIMG + os.sep + filename
