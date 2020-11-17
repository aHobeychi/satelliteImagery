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
    'begin':        '20191001',
    'end':          '20201116',
}


class ApiSession():
    """
    ApiSession Class handles all connections with SentinelAPI.
    """
    def __init__(self):
        self.key_file_path = '../ressources/apiKey.txt'
        self.export_directory = (os.path.normpath(
            os.path.join(os.getcwd(), os.pardir, 'downloadedImages')))
        self.user, self.password = self.parsefile()
        self.api = SentinelAPI(self.user, self.password, query['url'])
        self.platform = 'Sentinel-2'

    def parsefile(self):
        """
        Parses the apiKey.txt and returns a tuple containing the username
        and password for the SentinelAPI.
        """
        text = ''
        try:
            text = open(self.key_file_path, 'r')
        except FileExistsError as exception:
            print('Api key file not found, must be in ressources/apiKey.txt')
            print('Raised Error: {}'.format(exception))

        info = []
        for line in text:
            info.append(line.strip().split(',')[1])

        return (info[0], info[1])

    def query(self, footprint):
        """
        Queries the SentinelAPI and returns a geojson containing data
        candidates.
        """
        return self.api.query(footprint, date=(query['begin'], query['end']),
                              platformname=query['platform'],
                              processinglevel=query['processing'])

    def to_geo_df(self, product):
        """
        Returns GeoDataFrame
        """
        return self.api.to_geodataframe(product)

    def download(self, link, directory):
        """
        Dowloads Data to directory using link provided.
        """
        self.api.download(
            link, directory_path=directory)

    def query_to_dataframe(self, footprint, output_path, contains=True):
        """
        Saves the queried geopandas to a csv file so that it could be
        used in the future.
        contains: if true will only save the links that fully contain the
            footprint
        """
        catalog = self.query(footprint)
        catalog = self.to_geo_df(catalog)
        desired_columns = [
            'summary', 'vegetationpercentage', 'notvegetatedpercentage',
            'waterpercentage', 'unclassifiedpercentage', 'snowicepercentage',
            'cloudcoverpercentage', 'geometry', 'size'
        ]
        filtered_catalog = catalog[desired_columns]
        if contains:
            contains = [footprint.within(geometry) for
                        geometry in catalog['geometry']]
            filtered_catalog = filtered_catalog[contains]

        output = filtered_catalog.to_csv()
        output_file = open(output_path, 'w')
        output_file.write(output)
        output_file.close()


