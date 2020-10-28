"""
Handles the project structure,
creation of different project specific folder,
unzipping the data and keeping track of the image paths
"""

import os
from shutil import copy, move
from zipfile import ZipFile
from kmlHandler import KmlHandler
from apiSession import ApiSession
from datetime import date


class ProjectManager():

    def __init__(self, project_name=''):
        self.root_folder = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        self.projects_folder = self.root_folder + os.sep + 'projects'
        self.create_project_structure()
        self.project_name = ''
        if not project_name == '':
            self.add_project(project_name)
        self.kml_handler = KmlHandler()
        self.api_session = ApiSession()

    def create_project_structure(self):
        projects_folder = self.root_folder + os.sep + 'projects'
        if not os.path.exists(projects_folder):
            os.mkdir(projects_folder)

    def add_project(self, project_name):
        self.project_name = project_name
        folder_path = self.projects_folder + os.sep + project_name
        data_path = folder_path + os.sep + 'data'
        images_path = folder_path + os.sep + 'images'
        classification_path = folder_path + os.sep + 'classification'

        if os.path.exists(folder_path):
            print('project already exists')
        else:
            os.mkdir(folder_path)
            os.mkdir(data_path)
            os.mkdir(images_path)
            os.mkdir(classification_path)
            print('project created succesfully')

        self.add_kml()
        self.add_kml(self.project_name)
        self.api_session = ApiSession()

    def set_project_name(self, project_name):
        self.project_name = project_name

    def __get_project_list(self):
        sub_directories = os.listdir(self.projects_folder)
        return (folder for folder in sub_directories if os.listdir(folder))

    def add_kml(self, p_name='null'):
        kml_path = self.root_folder + os.sep + 'kmlFiles'
        kml_files = os.listdir(kml_path)
        desired_path = ''
        for k_file in kml_files:
            if self.project_name == k_file.split('.')[0]:
                desired_path = k_file

        if not desired_path == '':
            org_file = kml_path + os.sep + desired_path
            new_file = (self.projects_folder + os.sep + self.project_name
                        + os.sep + desired_path)

            if not os.path.exists(new_file):
                copy(org_file, new_file)

        else:
            print('no kml found')

    def get_download_path(self):
        return (self.projects_folder + os.sep +
                self.project_name + os.sep + 'data' + os.sep)

    def get_images_folder_path(self):
        return (self.projects_folder + os.sep +
                self.project_name + os.sep + 'images' + os.sep)

    def get_classification_folder_path(self):
        return (self.projects_folder + os.sep +
                self.project_name + os.sep + 'classification' + os.sep)

    def unzip_downlaod(self):
        zipped_name = ''
        download_path = self.get_download_path()
        for current_file in os.listdir(download_path):
            if current_file.endswith('.zip'):
                zipped_name = current_file

        # Extract date and time from the dowloaded data folder
        unformated_date = zipped_name.split('_')[2]
        year = unformated_date[0:4]
        month = unformated_date[4:6]
        day = unformated_date[6:8]
        formatted_date = '{}_{}_{}'.format(year, month, day)
        os.mkdir(download_path + formatted_date)

        with ZipFile(download_path + zipped_name) as zipped:
            zipped.extractall(download_path + formatted_date)

        end = zipped_name.find('.zip')
        os.remove(download_path + zipped_name)

        data_folder = '{}.SAFE'.format(zipped_name[:end]) + os.sep
        data_folder_path = (download_path + formatted_date
                            + os.sep + data_folder)

        for folders in os.listdir(data_folder_path):
            move(data_folder_path + os.sep + folders,
                 download_path + formatted_date)

    def get_footprint(self):
        kml_path = (self.projects_folder + os.sep +
                    self.project_name + os.sep + self.project_name + '.kml')
        return self.kml_handler.get_foot_print(kml_path)

    def get_catalog(self):
        footprint = self.get_footprint()
        query = self.api_session.query(footprint)
        return self.api_session.to_geo_df(query)

    def download_data(self, link):
        """downloads the data from the specific link"""
        self.api_session.download(link, self.get_download_path())
        self.unzip_downlaod()


    def get_resolution_paths(self):
        """returns the path of the resolution from the data forlder"""
        data_path = self.get_download_path()
        image_path = self.get_images_folder_path()
        all_dates = os.listdir(data_path)
        print('Select one of the dates to create images:')

        for num, date in enumerate(all_dates):
            print('({}): {}'.format(num, date))

        selected = input()

        if not os.path.exists(image_path + all_dates[int(selected)]):
            os.mkdir(image_path + all_dates[int(selected)])
            os.mkdir(image_path + all_dates[int(selected)] + os.sep + 'cropped')
            os.mkdir(self.get_classification_folder_path() +
                     all_dates[int(selected)] + os. sep)
            os.mkdir(self.get_classification_folder_path() +
                     all_dates[int(selected)] + os. sep + 'cropped')
        else:
            answ = input('The image folder already exists do you want to continue(y/n)?:')
            if answ == 'n':
                return False

        if not os.path.exists(image_path + all_dates[int(selected)] +
                              os.sep + 'cropped'):

            os.mkdir(image_path + all_dates[int(selected)]
                     + os.sep + 'cropped')

        data_folder = data_path + all_dates[int(selected)] + os.sep
        granule_path = data_folder + 'GRANULE' + os.sep
        granule_next = granule_path + os.listdir(granule_path)[0] + os.sep
        final_folder = granule_next + 'IMG_DATA' + os.sep

        references = []
        resolutions = ['R10m', 'R20m', 'R60m']

        for res in resolutions:
            resolution_dict = {}
            for data in os.listdir(final_folder + os.sep + res):
                key = data.split('_')[2]
                value = final_folder + res + os.sep + data
                resolution_dict[key] = value

            references.append(resolution_dict)
        return (references, image_path + all_dates[int(selected)] + os.sep)

    def create_projection(self, projection_type):
        file_path = (self.projects_folder + os.sep + self.project_name +
                     os.sep + self.project_name + '.kml')
        return self.kml_handler.create_projection(projection_type, file_path)

    def get_bounding_box(self, projection_type):
        """
        Returns bounding box around area of interest
        """
        file_path = (self.projects_folder + os.sep + self.project_name +
                     os.sep + self.project_name + '.kml')
        return self.kml_handler.create_bounding_box(projection_type, file_path)

    def get_image_paths(self, image_type, cropped=True):
        image_path = self.get_images_folder_path()
        all_dates = os.listdir(image_path)
        print('Select one of the dates to view the Images:')

        for num, date in enumerate(all_dates):
            print('({}): {}'.format(num, date))

        selected = input()
        path = image_path + all_dates[int(selected)]

        if cropped:
            path = path + os.sep + 'cropped'

        for files in os.listdir(path):
            if image_type in files.lower():
                return path + os.sep + files

    def get_classification_path(self, image_type, n_clusters, cropped=True):
        classification_path = self.get_classification_folder_path()
        all_dates = os.listdir(classification_path)

        print('Select one of the dates to view the classification:')

        for num, date in enumerate(all_dates):
            print('({}): {}'.format(num, date))

        selected = input()
        selection = all_dates[int(selected)]

        final_folder = ''
        if cropped:
            final_folder = classification_path + selection + os.sep + 'cropped'
        else:
            final_folder = classification_path + selection

        for files in os.listdir(final_folder):
            if image_type in files.lower():
                if str(n_clusters) in files:
                    return final_folder + os.sep + files

