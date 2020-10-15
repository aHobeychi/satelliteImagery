from projectManager import ProjectManager
import rasterData
from display import show_image, show_classification, convert_to_png
from classification import kmeans_classifiy, plot_cost_function


def download_sample(project):

    footprint = project.get_footprint()
    catalog = project.get_catalog()
    # REMOVE LINKS WITH TOO MUCH CLOUD COVERAGE
    catalog = catalog[catalog.cloudcoverpercentage < 1]
    # REMOVE THOSE WHERE THE FOOTPRINT ISNT FULLY CONTAINED
    # MEANING WHERE THE AREA OF INTEREST ISN'T TOTALLY CONTAINED IN THE
    # SATELLITE IMAGE
    contained = []
    for i in range(catalog.shape[0]):
        contained.append(footprint.within(catalog['geometry'][i]))
    catalog = catalog[contained].sort_values(
        by=['cloudcoverpercentage'], ascending=[True])

    toDownload = catalog.index.values[0]
    project.download_data(toDownload)


def main():

    # 1. create project
    projectName = 'montreal'
    project = ProjectManager(projectName)

    # 2. download data
    answ = input('Do you want to download the data (y/n)?: ')
    if answ == 'y':
        download_sample(project)

    # 3. create images
    answ = input('Do you want to create the images (y/n)?: ')
    if answ == 'y':
        rasterData.create_images(project)

    # 4. display the image
    answ = input('Do you want to display the images (y/n)?: ')
    if answ == 'y':
        show_image(project, 'rgb')
        # convert_to_png(project, 'rgb', cropped=False)

    # CLASSIFICATION
    clusters = 5
    # 5. classify the image
    answ = input('Do you want to classify the images (y/n)?: ')
    if answ == 'y':
        kmeans_classifiy(project, clusters, 'ndvi', False)
        # plot_cost_function(project, 'ndvi')

    # 6. show classified image
    answ = input('Do you want to show the classified images (y/n)?: ')
    if answ == 'y':
        convert_to_png(project, 'ndvi', False, True, clusters)
        # show_classification(project, clusters, 'ndvi', False)


if __name__ == "__main__":
    main()
