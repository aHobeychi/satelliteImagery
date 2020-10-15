"""
CLASSIFICATION FILE, USED TO ADD CLUSTERING TO IMAGES
"""

import os
from sklearn.cluster import KMeans
import gdal
import numpy as np
import matplotlib.pyplot as plt
import numpy


def plot_cost_function(project, image_type='allbands', cropped=True):

    image_path = project.get_image_paths(image_type, cropped)
    raster_data = gdal.Open(image_path)
    nbands = raster_data.RasterCount
    data = np.empty((raster_data.RasterXSize*raster_data.RasterYSize, nbands))

    for i in range(1, nbands+1):
        band = raster_data.GetRasterBand(i).ReadAsArray()
        data[:, i-1] = band.flatten()

    kval = range(2, 15)
    cost = [KMeans(n_clusters=k, random_state=1).fit(data).inertia_
            for k in kval]

    plt.plot(kval, cost)
    plt.xticks(kval)
    plt.title('K-means cost across K using {} image'.format
              (image_type))
    plt.xlabel('K')
    plt.ylabel('cost')
    plt.show()


def kmeans_classifiy(project, clusters, image_type='allbands', cropped=True):

    image_path = project.get_image_paths(image_type, cropped)
    tiff_driver = gdal.GetDriverByName('GTiff')
    raster_data = gdal.Open(image_path)
    nbands = raster_data.RasterCount
    data = np.empty((raster_data.RasterXSize*raster_data.RasterYSize, nbands))
    print(data)
    print(data.shape)

    for i in range(1, nbands+1):
        band = raster_data.GetRasterBand(i).ReadAsArray()
        data[:, i-1] = band.flatten()

    print(data)
    print(data.min(axis=1))
    print(data.max(axis=1))
    print(numpy.isnan(data).any())
    km = KMeans(n_clusters=clusters)
    km.fit(data)
    km.predict(data)

    out_data = km.labels_.reshape((raster_data.RasterYSize,
                                  raster_data.RasterXSize))

    date = 0
    output_path = ''
    if cropped:
        date = image_path.split(os.sep)[-3]
        output_path = (project.get_classification_folder_path() + date +
                       os.sep + 'cropped' + os.sep +
                       '{}_kMeans_{}.tiff'.format(image_type, clusters))
    else:
        date = image_path.split(os.sep)[-2]
        output_path = (project.get_classification_folder_path() + date +
                       os.sep +
                       '{}_kMeans_{}.tiff'.format(image_type, clusters))


    # save the original image with gdal
    output_data = tiff_driver.Create(output_path,
                                     raster_data.RasterXSize,
                                     raster_data.RasterYSize,
                                     1, gdal.GDT_Float32)

    output_data.SetGeoTransform(raster_data.GetGeoTransform())
    output_data.SetProjection(raster_data.GetProjection())
    output_data.GetRasterBand(1).SetNoDataValue(-9999.0)
    output_data.GetRasterBand(1).WriteArray(out_data)
