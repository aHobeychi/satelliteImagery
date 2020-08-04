from os import path
import numpy as np
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt

THREEBANDS = ['rgb', 'agri', 'bathy', 'swi', 'geo']

brightness = {
    'rgb': 8,
    'agri': 3,
    'geo': 2,
}


def convertPNG(project, imageType, cropped=True):

    filePath = project.getImagePath(imageType, cropped)

    if path.exists(filePath.replace('tiff', 'png')):
        return

    if imageType.lower() in THREEBANDS:
        __convertThreeBands(filePath, imageType)
        return

    src = rasterio.open(filePath)
    data = src.read()
    img = plt.imshow(data[0], cmap='RdYlGn')
    output = filePath.replace('tiff', 'png')
    plt.axis('off')
    plt.savefig(output, dpi=2000, bbox_inches='tight', pad_inches=0)


def __convertThreeBands(filePath, imageType):
    src = rasterio.open(filePath)
    data = src.read()
    stack1 = __normalizeArray(data[0], imageType)
    stack2 = __normalizeArray(data[1], imageType)
    stack3 = __normalizeArray(data[2], imageType)
    normedd = np.dstack((stack1, stack2, stack3))
    img = plt.imshow(normedd)
    output = filePath.replace('tiff', 'png')
    plt.axis('off')
    plt.savefig(output, dpi=2000, bbox_inches='tight', pad_inches=0)


def showImage(project, imageType, cropped=True):

    filePath = project.getImagePath(imageType, cropped)
    if imageType.lower() in THREEBANDS:
        __showThreeBands(filePath, imageType)
        return

    img = rasterio.open(filePath)
    ax = rasterio.plot.show(img, title=imageType,
                            cmap='RdYlGn', vmin=-1, vmax=1)


def __showThreeBands(filePath, imageType):
    src = rasterio.open(filePath)
    data = src.read()
    stack1 = __normalizeArray(data[0], imageType)
    stack2 = __normalizeArray(data[1], imageType)
    stack3 = __normalizeArray(data[2], imageType)
    normed = np.dstack((stack1, stack2, stack3))
    plt.imshow(normed)
    plt.show()


def __normalizeArray(a, imageType):

    min = np.min(a).astype('float32')
    max = np.max(a).astype('float32')
    norm = brightness[imageType]*(a.astype('float32')-min)/(max + min)
    return norm.clip(min=0)