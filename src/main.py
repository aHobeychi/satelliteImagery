from projectManager import ProjectManager
import rasterData
from display import showImage, showClassification
from classification import createKmeansClassification


def getData(project):

    footprint = project.getFootPrint()
    catalog = project.getGeoDataFrame(footprint)

    # REMOVE LINKS WITH TOO MUCH CLOUD COVERAGE
    catalog = catalog[catalog.cloudcoverpercentage < 1]

    # REMOVE THOSE WHERE THE FOOTPRINT ISNT CONTAINED
    contained = []
    for i in range(catalog.shape[0]):
        contained.append(footprint.within(catalog['geometry'][i]))
    catalog = catalog[contained].sort_values(
        by=['cloudcoverpercentage'], ascending=[True])

    toDownload = catalog.index.values[0]
    project.downloadData(toDownload)




def main():
    projectName = 'sanFrancisco'
    project = ProjectManager(projectName)
    # createKmeansClassification(project,4)
    # rasterData.createImages(project)
    # showImage(project,'ndvi')
    # showClassification(project, 4)

    # getData(project)

    # rasterData.convertPNG(project, 'rgb', cropped=True)
    # rasterData.createImages(project)


if __name__ == "__main__":
    main()
