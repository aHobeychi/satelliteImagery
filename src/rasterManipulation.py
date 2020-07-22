from os import listdir, path, mkdir, sep
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from rasterio import plot
from rasterio import mask


def createImages(info, project):
    createAgri(info, project)
    createBathy(info, project)
    createGeo(info, project)
    createNDVI(info, project)
    createSWI(info, project)
    createRGB(info, project)
    cropImage(info, project)


def cropImage(info, project):

    b02 = rasterio.open(info[0]['B02'])
    projType = b02.crs
    projection = project.createProjection(projType)
    originalFilePath = project.IMGDWN
    print(originalFilePath)
    outputPath = path.join(originalFilePath, 'cropped')
    print(outputPath)
    if not path.exists(outputPath):
        mkdir(outputPath)
    files = listdir(originalFilePath)
    for f in files:
        if path.isdir(path.join(originalFilePath,f)) or '_Cropped' in f or '.aux' in f:
            continue
        else:
            filepath = path.join(originalFilePath, f)
            with rasterio.open(filepath) as src:
                out_image, out_transform = mask.mask(
                    src, projection.geometry, crop=True)
                out_meta = src.meta.copy()
                out_meta.update({"driver": "GTiff",
                                 "height": out_image.shape[1],
                                 "width": out_image.shape[2],
                                 "transform": out_transform})

        writePath = path.join(outputPath, f.replace('.tiff', '_Cropped.tiff'))
        with rasterio.open(writePath, "w", **out_meta) as dest:
            dest.write(out_image)


def createNDVI(info, project):

    filepath = path.join(project.IMGDWN, '{}{}'.format(project.PROJECTNAME,'NDVI.tiff'))
    if path.exists(filepath):
        return

    r10 = info[0]
    nirReader = rasterio.open(r10['B08'])
    redReader = rasterio.open(r10['B04'])

    nir = nirReader.read(1).astype('float64')
    red = redReader.read(1).astype('float64')

    ndvi = np.where((nir+red) == 0, 0, (nir-red)/(nir+red))
    ndviImage = rasterio.open(filepath, 'w', driver='Gtiff',
                              width=nirReader.width,
                              height=nirReader.height,
                              count=1, crs=nirReader.crs,
                              transform=nirReader.transform,
                              dtype='float64')
    ndviImage.write(ndvi, 1)
    ndviImage.close()
    # ndvi = rasterio.open(filepath)
    # fig = plt.figure(figsize=(18,12))
    # plot.show(ndvi)


def createSWI(info, project):

    filepath = path.join(project.IMGDWN, '{}{}'.format(project.PROJECTNAME, 'SWI.tiff'))
    if path.exists(filepath):
        return

    r10 = info[0]
    r20 = info[1]
    red = rasterio.open(r10['B04'])
    b8a = rasterio.open(r20['B8A'])
    b12 = rasterio.open(r20['B12'])
    with rasterio.open(filepath, 'w', driver='Gtiff', width=red.width,
                       height=red.height, count=3, crs=red.crs, transform=red.transform,
                       dtype=red.dtypes[0]) as rgb:
        rgb.write(red.read(1), 1)
        rgb.write(b8a.read(1), 2)
        rgb.write(b12.read(1), 3)
        rgb.close()


def createRGB(info, project):

    filepath = path.join(project.IMGDWN, '{}{}'.format(project.PROJECTNAME, 'RGB.tiff'))
    if path.exists(filepath):
        return

    r10 = info[0]
    blue = rasterio.open(r10['B02'])
    green = rasterio.open(r10['B03'])
    red = rasterio.open(r10['B04'])
    with rasterio.open(filepath, 'w', driver='Gtiff', width=red.width,
                       height=red.height, count=3, crs=red.crs, transform=red.transform,
                       dtype=red.dtypes[0]) as rgb:
        rgb.write(red.read(1), 1)
        rgb.write(green.read(1), 2)
        rgb.write(blue.read(1), 3)
        rgb.close()


def createGeo(info, project):

    filepath = path.join(project.IMGDWN, '{}{}'.format(project.PROJECTNAME,'GEO.tiff'))
    if path.exists(filepath):
        return

    r10 = info[0]
    r20 = info[1]
    blue = rasterio.open(r10['B02'])
    b11 = rasterio.open(r20['B11'])
    b12 = rasterio.open(r20['B12'])
    with rasterio.open(filepath, 'w', driver='Gtiff', width=blue.width,
                       height=blue.height, count=3, crs=blue.crs, transform=blue.transform,
                       dtype=blue.dtypes[0]) as rgb:
        rgb.write(blue.read(1), 1)
        rgb.write(b11.read(1), 2)
        rgb.write(b12.read(1), 3)
        rgb.close()


def createBathy(info, project):

    filepath = path.join(project.IMGDWN, '{}{}'.format(project.PROJECTNAME, 'BAT.tiff'))
    if path.exists(filepath):
        return

    r10 = info[0]
    r60 = info[2]
    green = rasterio.open(r10['B03'])
    red = rasterio.open(r10['B04'])
    b01 = rasterio.open(r60['B01'])
    with rasterio.open(filepath, 'w', driver='Gtiff', width=red.width,
                       height=red.height, count=3, crs=red.crs, transform=red.transform,
                       dtype=red.dtypes[0]) as rgb:
        rgb.write(red.read(1), 1)
        rgb.write(green.read(1), 2)
        rgb.write(b01.read(1), 3)
        rgb.close()


def createAgri(info, project):

    filepath = path.join(project.IMGDWN, '{}{}'.format(project.PROJECTNAME, 'AGRI.tiff'))
    if path.exists(filepath):
        return

    r10 = info[0]
    r20 = info[1]
    blue = rasterio.open(r10['B02'])
    b11 = rasterio.open(r20['B11'])
    b08 = rasterio.open(r10['B08'])
    with rasterio.open(filepath, 'w', driver='Gtiff', width=blue.width,
                       height=blue.height, count=3, crs=blue.crs, transform=blue.transform,
                       dtype=blue.dtypes[0]) as rgb:
        rgb.write(blue.read(1), 1)
        rgb.write(b11.read(1), 2)
        rgb.write(b08.read(1), 3)
        rgb.close()
