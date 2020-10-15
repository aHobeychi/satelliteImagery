"""
HANDLES API SESSION AND DOWNLOADS DATA
REQUIRES AN API KEY FROM https://scihub.copernicus.eu/dhus/
"""

import os
from sentinelsat import SentinelAPI

# API QUERY PARAMETERS
query = {
    'url':          'https://scihub.copernicus.eu/dhus',
    'platform':     'Sentinel-2',
    'processing':   'Level-2A',
    'begin':        '20180710',
    'end':          '20200710',
}


class ApiSession():

    def __init__(self):
        self.KEYFILEPATH = '../ressources/apiKey.txt'
        self.EXPORTDIRECTORY = (os.path.normpath(
            os.path.join(os.getcwd(), os.pardir, 'downloadedImages')))
        self.user, self.password = self.parsefile()
        self.api = SentinelAPI(self.user, self.password, query['url'])
        self.platform = 'Sentinel-2'

    def parsefile(self):
        text = ''
        try:
            text = open(self.KEYFILEPATH, 'r')
        except Exception as e:
            print('Api key file not found, must be in ressources/apiKey.txt')
            print('Raised Error: {}'.format(e))

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
        self.api.download(
            link, directory_path=directory)

    def change_query_date(self, start, end):
        """Changes the dates of the query. Accepts date objects"""
        start_string = '{}{}{}'.format(*start.strftime('%Y/%m/%d').split('/'))
        end_string = '{}{}{}'.format(*end.strftime('%Y/%m/%d').split('/'))
        query['begin'] = start_string
        query['end'] = end_string
