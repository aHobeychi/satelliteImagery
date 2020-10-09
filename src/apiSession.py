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


class ApiSession():

    def __init__(self, project_name):
        self.KEYFILEPATH = '../ressources/apiKey.txt'
        self.EXPORTDIRECTORY = (os.path.normpath(
            os.path.join(os.getcwd(), os.pardir, 'downloadedImages')))
        self.PROJECTNAME = project_name
        self.user, self.password = self.parsefile()
        self.api = SentinelAPI(self.user, self.password, query['url'])
        self.platform = 'Sentinel-2'

    def parsefile(self):
        text = open(self.KEYFILEPATH, 'r')
        info = []
        for line in text:
            info.append(line.strip().split(',')[1])

        return (info[0], info[1])

    def query(self, footprint):
        return self.api.query(footprint, date=(query['begin'], query['end']),
                              platformname=query['platform'],
                              processinglevel=query['processing'])

    def to_geo_df(self, product):
        return self.api.to_geodataframe(product)

    def download(self, link, directory):
        print(directory)
        self.api.download(
            link, directory_path=directory)
