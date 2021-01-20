# This is designed to separate the water from the image taken from Landsat 8

from __future__ import division
from osgeo import gdal
import glob
import numpy as np
import matplotlib.pyplot as plt
import natsort

def Get_array(tif):
    ds = gdal.Open(tif)
    infor = ds.GetGeoTransform() # get size of raster, resolution, cordinate system
    band = ds.GetRasterBand(1) # Fetch the band
    bandtype = gdal.GetDataTypeName(band.DataType)
    print("Basic Information = {}, Band Type {}".format(infor, bandtype))
    array = band.ReadAsArray()
    return array


def Cal_NDWI(b3, b5):
    
    upper = b3.astype(np.float) - b5.astype(np.float)
    lower = b3.astype(np.float) + b5.astype(np.float)
    ndwi = upper/lower
    nan_index = np.isnan(ndwi)
    ndwi[nan_index] = 0
    return ndwi


def plot_water_bin(ndwi):
    how_you_feel = 0
    while how_you_feel == 0:
        threshold = eval(input('Please input a threshold, range from -1 to 1:'))
        binmask = np.where(ndwi >= threshold,1,0)
        plt.figure()
        plt.xticks = []
        plt.yticks = []
        plt.imshow(binmask)
        plt.show()
        how_you_feel = eval(input('If that is OK, input 1. If not, input 0:'))

def plot_water(ndwi, cmap, dpi):
    width = ndwi.shape[0]
    height = ndwi.shape[1]
    plt.figure()
    plt.xticks([])
    plt.yticks([])
    plt.imshow(ndwi, cmap = cmap)
    plt.savefig('processed_image.png', figsize=(width/dpi, height/dpi) ,dpi = dpi)
    #plt.show()
    

def sissors(x,y,band): # 裁剪band对象。x还有y通过输入一个数组，例如[200,300]表示最小200，最大300
    new_band = band[x[0]:x[1], y[0]:y[1]]
    return new_band


if __name__ == '__main__':
    print('The original author is 何新辰（Xinchen He）')
    print('Please give credit to the original author when you use it elsewhere')
    print('Get a nice figure of your research area from the Landsat8 OLI image')
    
    # 输入图片文件夹
    while True:
        input_dir = input('Input the dir name of your raster images:')
        Tif_list = glob.glob(input_dir + '/*.TIF') # 读取文件夹中所有TIF文件
        if Tif_list == []:
            print('Wrong dir name, please try again')
        else:
            break
    
    # 用natsort防止1后面就是10
    Tif_list = natsort.natsorted(Tif_list)
    print(Tif_list)
    
    # 读取图片数据
    b4 = Get_array(Tif_list[3])
    b2 = Get_array(Tif_list[1])
    b3 = Get_array(Tif_list[2])
    b5 = Get_array(Tif_list[4])
    
    # 选择调色板
    cmap_list = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 
    'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges',
     'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 
     'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 
     'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 
     'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 
     'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r',
      'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 
      'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 
      'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 
      'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 
      'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 
      'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 
      'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 
      'winter_r']
    while True:
        cmap = input('Please go to the website of maplotlib: https://matplotlib.org/tutorials/colors/colormaps.html and select a colormaps you like. For example, I prefer using Spectral:')
        if cmap in cmap_list:
            break
        else:
            print('Wrong colormap, please try again:')


    # 选择NDWI还是MNDWI
    how_you_feel = 0
    while how_you_feel == 0:
        method = input('NDWI or MNDWI. I suggest using MNDWI on eutrophicated lakes:')
        if method == 'NDWI':
            b3_1 = sissors([4000,7000],[2000,5000],b3)
            b5_1 = sissors([4000,7000],[2000,5000],b5)
            ndwi = Cal_NDWI(b3,b5)
            dpi = eval(input('Inpu the value of the DPI you want:'))
            plot_water(ndwi, cmap, dpi)
            how_you_feel = 1
        elif method == 'MNDWI':
            b2_1 = sissors([4000,7000],[2000,5000],b2)
            b5_1 = sissors([4000,7000],[2000,5000],b5)
            mndwi = Cal_NDWI(b2, b5)
            dpi = eval(input('Inpu the value of the DPI you want:'))
            plot_water(mndwi, cmap, dpi)
            how_you_feel = 1
        else:
            print('Wrong method, please input again')




