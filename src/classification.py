"""
CLASSIFICATION FILE, USED TO ADD CLUSTERING TO IMAGES
"""

import os
from sklearn.cluster import KMeans
import gdal
import numpy as np


def kmeans_classifiy(project, clusters, image_type='allbands', cropped=True):

    image_path = project.get_image_paths(image_type, cropped)
    tiff_driver = gdal.GetDriverByName('GTiff')
    raster_data = gdal.Open(image_path)
    nbands = raster_data.RasterCount
    data = np.empty((raster_data.RasterXSize*raster_data.RasterYSize, nbands))

    print(image_path)
    for i in range(1, nbands+1):
        band = raster_data.GetRasterBand(i).ReadAsArray()
        data[:, i-1] = band.flatten()

    km = KMeans(n_clusters=clusters)
    km.fit(data)
    km.predict(data)

    out_data = km.labels_.reshape((raster_data.RasterYSize,
                                  raster_data.RasterXSize))

    date = 0
    output_path = ''
    if cropped:
        date = image_path.split('/')[-3]
        output_path = (project.get_classification_folder_path() + date +
                       os.sep + 'cropped' + os.sep +
                       '{}_kMeans_{}.tiff'.format(image_type, clusters))
    else:
        date = image_path.split('/')[-2]
        output_path = (project.get_classification_folder_path() + date +
                       os.sep +
                       '{}_kMeans_{}.tiff'.format(image_type, clusters))


    print(output_path)
    # save the original image with gdal
    output_data = tiff_driver.Create(output_path,
                                     raster_data.RasterXSize,
                                     raster_data.RasterYSize,
                                     1, gdal.GDT_Float32)

    output_data.SetGeoTransform(raster_data.GetGeoTransform())
    output_data.SetProjection(raster_data.GetProjection())
    output_data.GetRasterBand(1).SetNoDataValue(-9999.0)
    output_data.GetRasterBand(1).WriteArray(out_data)
