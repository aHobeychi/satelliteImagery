"""
raster data creates the imagery from the different spectral band
info about the band can be found at: 
https://gisgeography.com/sentinel-2-bands-combinations/ 
https://www.satimagingcorp.com/satellite-sensors/other-satellite-sensors/sentinel-2a/
"""

from os import listdir, path, mkdir
import numpy as np
import rasterio
import rasterio.mask
from osgeo import gdal

THREEBANDS = ['rgb', 'agri', 'bathy', 'swi', 'geo']

brightness = {
    'rgb': 8,
    'agri': 3,
    'geo': 2,
}


def createImages(project):
    info = project.findImageFiles()
    createAgri(info, project)
    createBathy(info, project)
    createGeo(info, project)
    createNDVI(info, project)
    createSWI(info, project)
    createRGB(info, project)
    createNDBI(info, project)
    createTrainingData(project)
    cropImage(info, project)


def cropImage(info, project):

    b02 = rasterio.open(info[0]['B02'])
    projType = b02.crs
    projection = project.createProjection(projType)
    originalFilePath = project.IMGDWN
    outputPath = path.join(originalFilePath, 'cropped')
    if not path.exists(outputPath):
        mkdir(outputPath)
    files = listdir(originalFilePath)
    for f in files:
        if path.isdir(path.join(originalFilePath, f)) or '_Cropped' in f or '.aux' in f:
            continue
        else:
            filepath = path.join(originalFilePath, f)
            with rasterio.open(filepath) as src:
                out_image, out_transform = rasterio.mask.mask(
                    src, projection.geometry, crop=True)
                out_meta = src.meta.copy()
                out_meta.update({"driver": "GTiff",
                                 "height": out_image.shape[1],
                                 "width": out_image.shape[2],
                                 "transform": out_transform})

        writePath = path.join(outputPath, f.replace('.tiff', '_Cropped.tiff'))
        with rasterio.open(writePath, "w", **out_meta) as dest:
            dest.write(out_image)


def createNDBI(info, project):

    filepath = path.join(project.IMGDWN, '{}{}'.format(
        project.PROJECTNAME, 'NDBI.tiff'))
    if path.exists(filepath):
        return

    r20 = info[1]
    nirReader = rasterio.open(r20['B8A'], driver='JP2OpenJPEG')
    swirReader = rasterio.open(r20['B11'], driver='JP2OpenJPEG')

    nir = nirReader.read(1).astype('float64')
    swir = swirReader.read(1).astype('float64')

    ndbi = np.where((swir+nir) == 0, 0, (swir-nir)/(swir+nir))
    ndbiImage = rasterio.open(filepath, 'w', driver='Gtiff',
                              width=nirReader.width,
                              height=nirReader.height,
                              count=1, crs=nirReader.crs,
                              transform=nirReader.transform,
                              dtype='float64')
    ndbiImage.write(ndbi, 1)
    ndbiImage.close()


def createNDVI(info, project):

    filepath = path.join(project.IMGDWN, '{}{}'.format(
        project.PROJECTNAME, 'NDVI.tiff'))
    if path.exists(filepath):
        return

    r10 = info[0]
    nirReader = rasterio.open(r10['B08'], driver='JP2OpenJPEG')
    redReader = rasterio.open(r10['B04'], driver='JP2OpenJPEG')

    nir = nirReader.read(1).astype('float64')
    red = redReader.read(1).astype('float64')

    ndvi = np.divide((nir-red), (nir+red))
    ndviImage = rasterio.open(filepath, 'w', driver='Gtiff',
                              width=nirReader.width,
                              height=nirReader.height,
                              count=1, crs=nirReader.crs,
                              transform=nirReader.transform,
                              dtype='float64')
    ndviImage.write(ndvi, 1)
    ndviImage.close()


def createSWI(info, project):

    filepath = path.join(project.IMGDWN, '{}{}'.format(
        project.PROJECTNAME, 'SWI.tiff'))
    if path.exists(filepath):
        r10 = info[0]
        r20 = info[1]
        red = rasterio.open(r10['B04'], driver='JP2OpenJPEG')
        b8a = rasterio.open(r20['B8A'], driver='JP2OpenJPEG')
        b12 = rasterio.open(r20['B12'], driver='JP2OpenJPEG')
        with rasterio.open(filepath, 'w', driver='Gtiff', width=red.width, height=red.height, count=3,
                           crs=red.crs, transform=red.transform,
                           dtype=red.dtypes[0]) as rgb:
            rgb.write(red.read(1), 1)
            rgb.write(b8a.read(1), 2)
            rgb.write(b12.read(1), 3)
            rgb.close()


def createRGB(info, project):

    filepath = path.join(project.IMGDWN, '{}{}'.format(
        project.PROJECTNAME, 'RGB.tiff'))
    if path.exists(filepath):
        return

    r10 = info[0]
    blue = rasterio.open(r10['B02'], driver='JP2OpenJPEG')
    green = rasterio.open(r10['B03'], driver='JP2OpenJPEG')
    red = rasterio.open(r10['B04'], driver='JP2OpenJPEG')
    with rasterio.open(filepath, 'w', driver='Gtiff', width=red.width,
                       height=red.height, count=3, crs=red.crs, transform=red.transform,
                       dtype=red.dtypes[0]) as rgb:
        rgb.write(red.read(1), 1)
        rgb.write(green.read(1), 2)
        rgb.write(blue.read(1), 3)
        rgb.close()


def createGeo(info, project):

    filepath = path.join(project.IMGDWN, '{}{}'.format(
        project.PROJECTNAME, 'GEO.tiff'))
    if path.exists(filepath):
        return

    r10 = info[0]
    r20 = info[1]
    blue = rasterio.open(r10['B02'], driver='JP2OpenJPEG')
    b11 = rasterio.open(r20['B11'], driver='JP2OpenJPEG')
    b12 = rasterio.open(r20['B12'], driver='JP2OpenJPEG')
    with rasterio.open(filepath, 'w', driver='Gtiff', width=blue.width,
                       height=blue.height, count=3, crs=blue.crs, transform=blue.transform,
                       dtype=blue.dtypes[0]) as rgb:
        rgb.write(blue.read(1), 1)
        rgb.write(b11.read(1), 2)
        rgb.write(b12.read(1), 3)
        rgb.close()


def createBathy(info, project):

    filepath = path.join(project.IMGDWN, '{}{}'.format(
        project.PROJECTNAME, 'BAT.tiff'))
    if path.exists(filepath):
        return

    r10 = info[0]
    r60 = info[2]
    green = rasterio.open(r10['B03'], driver='JP2OpenJPEG')
    red = rasterio.open(r10['B04'], driver='JP2OpenJPEG')
    b01 = rasterio.open(r60['B01'], driver='JP2OpenJPEG')
    with rasterio.open(filepath, 'w', driver='Gtiff', width=red.width,
                       height=red.height, count=3, crs=red.crs, transform=red.transform,
                       dtype=red.dtypes[0]) as rgb:
        rgb.write(red.read(1), 1)
        rgb.write(green.read(1), 2)
        rgb.write(b01.read(1), 3)
        rgb.close()


def createAgri(info, project):

    filepath = path.join(project.IMGDWN, '{}{}'.format(
        project.PROJECTNAME, 'AGRI.tiff'))
    if path.exists(filepath):
        return

    r10 = info[0]
    r20 = info[1]
    blue = rasterio.open(r10['B02'], driver='JP2OpenJPEG')
    b11 = rasterio.open(r20['B11'], driver='JP2OpenJPEG')
    b08 = rasterio.open(r10['B08'], driver='JP2OpenJPEG')
    with rasterio.open(filepath, 'w', driver='Gtiff', width=blue.width,
                       height=blue.height, count=3, crs=blue.crs, transform=blue.transform,
                       dtype=blue.dtypes[0]) as rgb:
        rgb.write(blue.read(1), 1)
        rgb.write(b11.read(1), 2)
        rgb.write(b08.read(1), 3)
        rgb.close()


def createTrainingData(project):

    filePath = path.join(project.IMGDWN, '{}{}'.format(
        project.PROJECTNAME, 'ALLBANDS.tiff'))
    if path.exists(filePath):
        return

    paths = project.findImageFiles()
    addresses = list(paths[0].values())
    with rasterio.open(addresses[0]) as src:
        meta = src.meta

    meta.update(count=len(paths[0]))
    with rasterio.open(filePath, 'w', **meta) as dst:
        for id, layer in enumerate(addresses, start=1):
            with rasterio.open(layer) as src1:
                dst.write_band(id, src1.read(1).astype('uint16'))


def imageInformation(project, imageType, cropped=True):

    imagePath = project.getImagePath(imageType, cropped)

    dataset = gdal.Open(imagePath)
    print('Image Raster Count: {}'.format(dataset.RasterCount))

    num_bands = dataset.RasterCount
    print('Number of bands in the image: {}'.format(num_bands))

    rows = dataset.RasterYSize
    cols = dataset.RasterXSize
    print('Image size is: {} rows by {} columns'.format(rows, cols))

    desc = dataset.GetDescription()
    metadata = dataset.GetMetadata()
    print('Raster description: {}'.format(desc))
    print('Raster metadata: {}'.format(metadata))

    driver = dataset.GetDriver()
    print('Raster driver: {}'.format(driver.ShortName))

    proj = dataset.GetProjection()
    print('Image projection: {}'.format(proj))

    gt = dataset.GetGeoTransform()
    print('Image geo-transform: {gt}'.format(gt=gt))

    blue = dataset.GetRasterBand(1)
    print('Band datatype: {}'.format(blue.DataType))
    datatype_name = gdal.GetDataTypeName(blue.DataType)
    print('Band datatype: {}'.format(datatype_name))

    type_size = gdal.GetDataTypeSize(blue.DataType)
    print('Band datatype size: {} bytes'.format(type_size))

    band_max, band_min, band_mean, band_stddev = blue.GetStatistics(0, 1)
    print('Band range: {} - {}'.format(band_max, band_min))
    print('Band mean, stddev: {}, {}'.format(band_mean, band_stddev))
