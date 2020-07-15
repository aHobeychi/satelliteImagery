from apiSession import apiSession
from projectManager import projectManager


def getData(project):

    projectMap = project.getGeoPanda()
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

def processImages(imgInfo):
    print('here')

def main():
    projectName = 'rice lake'
    project = projectManager(projectName)
    # project.handleZippedData()
    # getData(project)
    info = project.findImageFiles()
    processImages(info)


if __name__ == "__main__":
    main()
