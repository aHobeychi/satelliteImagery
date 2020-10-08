"""
HANDLES API SESSION AND DOWNLOADS DATA
REQUIRES AN API KEY FROM https://scihub.copernicus.eu/dhus/
"""

from sentinelsat import SentinelAPI
import os

# API QUERY PARAMETERS
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
        self.EXPORTDIRECTORY = (os.path.normpath(
            os.path.join(os.getcwd(), os.pardir, 'downloadedImages')))
        self.PROJECTNAME = projectName
        self.user, self.password = self.parseFile()
        self.api = SentinelAPI(self.user, self.password, query['url'])
        self.platform = 'Sentinel-2'

    def parseFile(self):
        f = open(self.KEYFILEPATH, 'r')
        info = []
        for x in f:
            info.append(x.strip().split(',')[1])

        return (info[0], info[1])

    def query(self, footprint):
        return self.api.query(footprint, date=(query['begin'], query['end']),
                              platformname=query['platform'],
                              processinglevel=query['processing'])

    def toGeoDf(self, product):
        return self.api.to_geodataframe(product)

    def download(self, link, directory):
        self.api.download(
            link, directory_path=directory)

    def imageDictionnary(self, filepath):

        r10Dict = {}
        for file in os.listdir(filepath):
            if file.endswith(''):
                key = file.split('_')[2]
                r10Dict[key] = (filepath + os.sep + file)

        return r10Dict
