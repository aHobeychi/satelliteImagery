"""
raster data creates the imagery from the different spectral band
info about the band can be found at: 
https://gisgeography.com/sentinel-2-bands-combinations/ 
https://www.satimagingcorp.com/satellite-sensors/other-satellite-sensors/sentinel-2a/
"""

from os import listdir, path
import numpy as np
import rasterio
import rasterio.mask
from osgeo import gdal

THREEBANDS = ['rgb', 'agri', 'bathy', 'swi', 'geo']

BRIGHTNESS = {
    'rgb': 8,
    'agri': 3,
    'geo': 2,
}


def create_images(project):
    info = project.get_resolution_paths()
    if info is False:
        print('images were already created')
        return

    output = info[1]
    create_agri(info, project, output)
    create_bathy(info, project, output)
    create_geo(info, project, output)
    create_ndvi(info, project, output)
    create_swi(info, project, output)
    create_rgb(info, project, output)
    create_ndbi(info, project, output)
    create_all_bands(info, project, output)
    crop_images(info, project, output)


def crop_images(info, project, output):

    b02 = rasterio.open(info[0][0]['B02'])
    proj_types = b02.crs
    projection = project.create_projection(proj_types)
    non_cropped_path = output
    output_path = path.join(output, 'cropped')

    files = listdir(non_cropped_path)
    for data in files:
        if (path.isdir(path.join(non_cropped_path, data)) or
                '_Cropped' in data or '.aux' in data):
            continue
        else:
            filepath = path.join(non_cropped_path, data)
            with rasterio.open(filepath) as src:
                out_image, out_transform = rasterio.mask.mask(
                    src, projection.geometry, crop=True)
                out_meta = src.meta.copy()
                out_meta.update({"driver": "GTiff",
                                 "height": out_image.shape[1],
                                 "width": out_image.shape[2],
                                 "transform": out_transform})

        write_path = path.join(output_path, data.replace('.tiff',
                                                         '_Cropped.tiff'))
        with rasterio.open(write_path, "w", **out_meta) as dest:
            dest.write(out_image)


def create_ndbi(info, project, output):

    filepath = path.join(output, '{}_{}'.format(
        project.project_name, 'NDBI.tiff'))

    # print(info[0][1])
    r20 = info[0][1]

    nir_reader = rasterio.open(r20['B8A'], driver='JP2OpenJPEG')
    swir_reader = rasterio.open(r20['B11'], driver='JP2OpenJPEG')

    nir = nir_reader.read(1).astype('float64')
    swir = swir_reader.read(1).astype('float64')

    ndbi = np.where((swir+nir) == 0, 0, (swir-nir)/(swir+nir))
    ndbi_image = rasterio.open(filepath, 'w', driver='Gtiff',
                               width=nir_reader.width,
                               height=nir_reader.height,
                               count=1, crs=nir_reader.crs,
                               transform=nir_reader.transform,
                               dtype='float64')
    ndbi_image.write(ndbi, 1)
    ndbi_image.close()


def create_ndvi(info, project, output):

    filepath = path.join(output, '{}_{}'.format(
        project.project_name, 'NDVI.tiff'))

    r10 = info[0][0]
    nir_reader = rasterio.open(r10['B08'], driver='JP2OpenJPEG')
    red_reader = rasterio.open(r10['B04'], driver='JP2OpenJPEG')

    nir = nir_reader.read(1).astype('float64')
    red = red_reader.read(1).astype('float64')

    ndvi = np.divide((nir-red), (nir+red))
    ndvi_image = rasterio.open(filepath, 'w', driver='Gtiff',
                               width=nir_reader.width,
                               height=nir_reader.height,
                               count=1, crs=nir_reader.crs,
                               transform=nir_reader.transform,
                               dtype='float64')
    ndvi_image.write(ndvi, 1)
    ndvi_image.close()


def create_swi(info, project, output):

    filepath = path.join(output, '{}_{}'.format(
        project.project_name, 'SWI.tiff'))

    r10 = info[0][0]
    r20 = info[0][1]
    red = rasterio.open(r10['B04'], driver='JP2OpenJPEG')
    b8a = rasterio.open(r20['B8A'], driver='JP2OpenJPEG')
    b12 = rasterio.open(r20['B12'], driver='JP2OpenJPEG')
    with rasterio.open(filepath, 'w', driver='Gtiff', width=red.width,
                       height=red.height, count=3,
                       crs=red.crs, transform=red.transform,
                       dtype=red.dtypes[0]) as rgb:

        rgb.write(red.read(1), 1)
        rgb.write(b8a.read(1), 2)
        rgb.write(b12.read(1), 3)
        rgb.close()


def create_rgb(info, project, output):

    filepath = path.join(output, '{}_{}'.format(
        project.project_name, 'RGB.tiff'))

    r10 = info[0][0]
    blue = rasterio.open(r10['B02'], driver='JP2OpenJPEG')
    green = rasterio.open(r10['B03'], driver='JP2OpenJPEG')
    red = rasterio.open(r10['B04'], driver='JP2OpenJPEG')
    with rasterio.open(filepath, 'w', driver='Gtiff', width=red.width,
                       height=red.height, count=3, crs=red.crs,
                       transform=red.transform,
                       dtype=red.dtypes[0]) as rgb:

        rgb.write(red.read(1), 1)
        rgb.write(green.read(1), 2)
        rgb.write(blue.read(1), 3)
        rgb.close()


def create_geo(info, project, output):

    filepath = path.join(output, '{}_{}'.format(
        project.project_name, 'GEO.tiff'))

    r10 = info[0][0]
    r20 = info[0][1]
    blue = rasterio.open(r10['B02'], driver='JP2OpenJPEG')
    b11 = rasterio.open(r20['B11'], driver='JP2OpenJPEG')
    b12 = rasterio.open(r20['B12'], driver='JP2OpenJPEG')
    with rasterio.open(filepath, 'w', driver='Gtiff', width=blue.width,
                       height=blue.height, count=3, crs=blue.crs,
                       transform=blue.transform,
                       dtype=blue.dtypes[0]) as rgb:

        rgb.write(blue.read(1), 1)
        rgb.write(b11.read(1), 2)
        rgb.write(b12.read(1), 3)
        rgb.close()


def create_bathy(info, project, output):

    filepath = path.join(output, '_{}_{}'.format(
        project.project_name, 'BAT.tiff'))

    r10 = info[0][0]
    r60 = info[0][2]
    green = rasterio.open(r10['B03'], driver='JP2OpenJPEG')
    red = rasterio.open(r10['B04'], driver='JP2OpenJPEG')
    b01 = rasterio.open(r60['B01'], driver='JP2OpenJPEG')
    with rasterio.open(filepath, 'w', driver='Gtiff', width=red.width,
                       height=red.height, count=3, crs=red.crs,
                       transform=red.transform,
                       dtype=red.dtypes[0]) as rgb:
        rgb.write(red.read(1), 1)
        rgb.write(green.read(1), 2)
        rgb.write(b01.read(1), 3)
        rgb.close()


def create_agri(info, project, output):

    filepath = path.join(output, '_{}_{}'.format(
        project.project_name, 'AGRI.tiff'))

    r10 = info[0][0]
    r20 = info[0][1]
    blue = rasterio.open(r10['B02'], driver='JP2OpenJPEG')
    b11 = rasterio.open(r20['B11'], driver='JP2OpenJPEG')
    b08 = rasterio.open(r10['B08'], driver='JP2OpenJPEG')
    with rasterio.open(filepath, 'w', driver='Gtiff', width=blue.width,
                       height=blue.height, count=3, crs=blue.crs,
                       transform=blue.transform,
                       dtype=blue.dtypes[0]) as rgb:

        rgb.write(blue.read(1), 1)
        rgb.write(b11.read(1), 2)
        rgb.write(b08.read(1), 3)
        rgb.close()


def create_all_bands(info, project, output):

    file_path = path.join(output, '{}_{}'.format(
        project.project_name, 'ALLBANDS.tiff'))

    addresses = list(info[0][0].values())
    with rasterio.open(addresses[0]) as src:
        meta = src.meta

    meta.update(count=len(info[0][0]))
    with rasterio.open(file_path, 'w', **meta) as dst:
        for ids, layer in enumerate(addresses, start=1):
            with rasterio.open(layer) as src1:
                dst.write_band(ids, src1.read(1).astype('uint16'))


def image_information(project, image_type, cropped=True):

    image_path = project.getImagePath(image_type, cropped)

    dataset = gdal.Open(image_path)
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
