from project_manager import ProjectManager
import image_creator
from display import show_image, show_classification
from classification import kmeans_cluster, plot_cost_function
from classification import dbscan_cluster, gmm_cluster


def download_sample(project):
    """
    Downloads Sample Image for a given project
    takes into consideration cloud coverage only
    """

    footprint = project.get_footprint()
    catalog = project.get_catalog()
    # REMOVE LINKS WITH TOO MUCH CLOUD COVERAGE
    catalog = catalog[catalog.cloudcoverpercentage < 5]
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
    # projectName = 'kilimanjaro'
    projectName = 'montreal'
    project = ProjectManager(projectName)

    # 3. create images
    answ = input('Do you want to create the images (y/n)?: ')
    if answ == 'y':
        answ = input('Batch create(y/n)?: ')
        if answ == 'y':
            project.batch_create_imagery()
        else: image_creator.create_images(project)

    # 4. display the image
    answ = input('Do you want to display the images (y/n)?: ')
    if answ == 'y':
        show_image(project, 'rgb', cropped=False)

    # CLASSIFICATION
    clusters = 5
    cropped = True
    image_type = 'ndvi'
    # 5. classify the image
    answ = input('Do you want to classify the images (y/n)?: ')
    # answ = 'y'
    if answ == 'y':
        kmeans_cluster(project, clusters, image_type, cropped)
        # gmm_cluster(project, clusters, image_type, cropped)
        # dbscan_cluster(project, 5, 100, image_type, cropped)
        # plot_cost_function(project, 'ndvi')

    # 6. show classified image
    answ = input('Do you want to show the classified images (y/n)?: ')
    if answ == 'y':
        # convert_to_png(project, 'ndvi', False, True, clusters)
        show_classification(project, cropped)


if __name__ == "__main__":
    main()
