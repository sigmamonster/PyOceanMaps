PyOceanMaps
-----------
This package plots the ocean floor bathymetry. The package is based on python's basemap (see requirements). There's a lot that could still be done so feel free to fork and contribute. There's a to do list for the master branch (version 1.0) at the bottom of this file. 

#### Requirements ####
* [ETOPO1 file](http://www.ngdc.noaa.gov/mgg/global/relief/ETOPO1/data/ice_surface/grid_registered/netcdf/ETOPO1_Ice_g_gmt4.grd.gz) 377MB
* Python 2.6 or 2.7
* Matplotlib
* Basemap (mpl_toolkits)

#### Package Contents ####
* this readme
* bath_map
* bath_section
* haversine

#### To Do ####
1. **haversine:** add options where input can be n,2 and more - see the top of the file for full list
2. **bath_map:** make it more pythonic and create standalone function plotting the bathymetry
3. **bath_section:** same as *bath map* abd improve ouput
4. **general:** make tests that the functions need to pass to check for simple bugs
