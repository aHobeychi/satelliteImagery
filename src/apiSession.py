from sentinelsat import SentinelAPI
import os
import zipfile

query = {
    'url': 'https://scihub.copernicus.eu/dhus',
    'platform': 'Sentinel-2',
    'processing': 'Level-2A',
    'begin': '20150710',
    'end': '20200710',
}


class apiSession():

    def __init__(self, projectName):
        self.KEYFILEPATH = '../ressources/apiKey.txt'
        self.EXPORTDIRECTORY = (os.path.normpath(os.getcwd() + os.sep + os.pardir + "\\downloadedImages\\"))
        self.PROJECTNAME = projectName
        self.R10LOCATION = ''
        self.user, self.password = self.parseFile()
        self.api = SentinelAPI(self.user, self.password, query['url'])
        self.platform = 'Sentinel-2'

    def parseFile(self):
        f=open(self.KEYFILEPATH, 'r')
        info=[]
        for x in f:
            info.append(x.strip().split(',')[1])

        return (info[0], info[1])

    def query(self, footprint):
        return self.api.query(footprint, date=(query['begin'], query['end']),
        platformname=query['platform'], processinglevel=query['processing'])

    def toGeoDf(self, product):
        return self.api.to_geodataframe(product)

    def download(self, link, directory):
        self.api.download(
            link, directory_path=directory)

    def handleDownloadedFile(self, exportPath):

        fileName=''
        for file in os.listdir(exportPath):
            if file.endswith('.zip'):
                fileName=file

        with zipfile.ZipFile('{}\\{}'.format(exportPath, fileName)) as zip_ref:
            zip_ref.extractall('{}'.format(exportPath))

        end=fileName.find('.zip')
        newFileName='{}.SAFE'.format(fileName[:end])
        granulePath='{}\\{}\\GRANULE'.format(exportPath, newFileName)

        fileL2A=''
        for file in os.listdir(granulePath):
            if file.endswith(''):
                fileL2A=file

        imgPathR10='{}\\{}\\IMG_DATA\\R10m\\'.format(granulePath, fileL2A)
        self.R10LOCATION = imgPathR10
        imgPathR20='{}\\{}\\IMG_DATA\\R20m\\'.format(granulePath, fileL2A)
        imgPathR60='{}\\{}\\IMG_DATA\\R60m\\'.format(granulePath, fileL2A)

        r10ImageFiles=[]
        r10Dict={}
        for file in os.listdir(imgPathR10):
            if file.endswith(''):
                key=file.split('_')[2]
                r10Dict[key]=(imgPathR10 + file)

        return r10Dict


    def imageDictionnary(self, filepath):

        r10Dict={}
        for file in os.listdir(filepath):
            if file.endswith(''):
                key=file.split('_')[2]
                r10Dict[key]=(filepath + os.sep + file)

        return r10Dict

    def getR10MLocation(self):
        return self.R10LOCATION