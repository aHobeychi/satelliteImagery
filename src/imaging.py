from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import rasterio


def imageInformation(project, imageType, cropped=True):

    imagePath = project.getImagePath(imageType, cropped)

    dataset = gdal.Open(imagePath)
    print('Image Raster Count: '.format(dataset.RasterCount))

    num_bands = dataset.RasterCount
    print('Number of bands in image: {n}\n'.format(n=num_bands))

    # How many rows and columns?
    rows = dataset.RasterYSize
    cols = dataset.RasterXSize
    print('Image size is: {r} rows x {c} columns\n'.format(r=rows, c=cols))
    # Does the raster have a description or metadata?
    desc = dataset.GetDescription()
    metadata = dataset.GetMetadata()

    print('Raster description: {desc}'.format(desc=desc))
    print('Raster metadata:')
    print(metadata)
    print('\n')

    # What driver was used to open the raster?
    driver = dataset.GetDriver()
    print('Raster driver: {d}\n'.format(d=driver.ShortName))

    # What is the raster's projection?
    proj = dataset.GetProjection()
    print('Image projection:')
    print(proj + '\n')

    # What is the raster's "geo-transform"
    gt = dataset.GetGeoTransform()
    print('Image geo-transform: {gt}\n'.format(gt=gt))

    blue = dataset.GetRasterBand(1)
    # What is the band's datatype?
    datatype = blue.DataType
    print('Band datatype: {dt}'.format(dt=blue.DataType))

    # If you recall from our discussion of enumerated types, this "3" we printed has a more useful definition for us to use
    datatype_name = gdal.GetDataTypeName(blue.DataType)
    print('Band datatype: {dt}'.format(dt=datatype_name))

    # We can also ask how much space does this datatype take up
    bytes = gdal.GetDataTypeSize(blue.DataType)
    print('Band datatype size: {b} bytes\n'.format(b=bytes))

    # How about some band statistics?
    band_max, band_min, band_mean, band_stddev = blue.GetStatistics(0, 1)
    print('Band range: {minimum} - {maximum}'.format(maximum=band_max,
                                                     minimum=band_min))
    print('Band mean, stddev: {m}, {s}\n'.format(m=band_mean, s=band_stddev))


def showImage(project, imageType, cropped=True):

    filePath = project.getImagePath(imageType, cropped)
    img = rasterio.open(filePath)
    rasterio.plot.show(img, title=imageType, cmap='RdYlGn', vmin=-1, vmax=1)
