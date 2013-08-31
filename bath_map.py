import os 
import sys
from matplotlib.pylab import *
import itertools as itt
import scipy as sp


class coords:
    def __init__(self):
        self.x1 = -180
        self.x2 = 180
        self.y1 = 90
        self.y2 = -90

def globmap(**kwds):
    from mpl_toolkits.basemap import Basemap
    from scipy.io.netcdf import netcdf_file
    rcParams['font.size']=10
    
    bm = kwds.pop('bm',True)
    print "Drawing selection map"
    
    # SETTING DOMAIN
    # MAP
    fig = figure(figsize=[10,4],dpi=100)
            
    m = Basemap(projection='cyl',
        llcrnrlon=-180,llcrnrlat=-90,
        urcrnrlon=180,urcrnrlat=90,
        resolution='c')
    if bm: 
        m.bluemarble(scale=.6)

    # MAP FEATURES    
    parallels = [-60,-30,0,30,60]
    meridians = [-120,-60,0,60,120]   
    m.drawparallels(parallels,color='k',labels=[1,0,0,1],linewidth=1)
    m.drawmeridians(meridians,color='k',labels=[1,0,0,1],linewidth=1)
    
    def click(event):
        # Function to round the degrees of the boundary box
        def roundnresize(r):
            # Rounds to the nearest x degrees
            coords.x1,coords.x2 = round(xlim()[0]/r)*r,round(xlim()[1]/r)*r
            coords.y2,coords.y1 = round(ylim()[0]/r)*r,round(ylim()[1]/r)*r
            xlim(coords.x1,coords.x2)
            ylim(coords.y2,coords.y1)
            draw()
            print 'UpperLeft  = \t%.3f N,  %.3f E'%(coords.y1,coords.x1)
            print 'LowerRight = \t%.3f N,  %.3f E'%(coords.y2,coords.x2)
            
        tb = get_current_fig_manager().toolbar
        if event.button==1 and event.inaxes and tb.mode == '':
            roundnresize(5)
                        
        if event.button==3 and event.inaxes and tb.mode == '':
            roundnresize(1)
            
        if event.button==2 and event.inaxes and tb.mode == '':
            roundnresize(0.1)
    
    gca().set_autoscale_on(False)
    connect('button_press_event',click)
    fig.subplots_adjust(left=0.06, right=0.67)
    instr = """
    Intstructions:

    1. Select region to plot by using the
        build in zoom function
    
    2. Unselect zoom
    
    3. Left click rounds to nearest deg
    4. Right click rounds to 1/10 of a deg
    5. Middle click does not round
    NOTE: on clicking window will readjust
    
    6. Close the window to plot
        
        
    NOTE: Negative is either S or W
    
    """
    figtext(0.69,0.91,instr,va='top',ha='left')
    
    show()
    close('all')
def bath_map(lat,lon,**kwargs):
    """
    Plots a map (using Basemap) for the defined area. 
    Can choose to have bathymetry (bath = 'contours/color/both/marble')
    x,y are scatter points which will be plotted on the map

    lats = [min,max]
    lons = [min,max]
    cmap = cm.---
    bath = [contour,color,both]
    """
    from mpl_toolkits.basemap import Basemap
    from scipy.io.netcdf import netcdf_file

    print 
    print 'Drawing output map'
  
    bath  = kwargs.pop('bath','color')
    cmap  = kwargs.pop('cmap',cm.Spectral_r)
    title = kwargs.pop('title',None)
    pvmin = kwargs.pop('pvmin',None)
    pvmax = kwargs.pop('pvmax',None)
    figsz = kwargs.pop('figsz',None)
    resin = kwargs.pop('resin','i')
    lvls  = kwargs.pop('lvls',np.arange(-6000,000,500))
    
    
    # SETTING DOMAIN
    minLat, maxLat = map(float, lat)
    minLon, maxLon = map(float, lon)
    lond = maxLon-minLon
    latd = maxLat-minLat
    i= ceil(sqrt(lond*latd)/10)
    if resin: res = resin
    # SETTING FIGURE SIZE
    coord_ratio = latd/lond
    if not figsz:
        figsz = [8,8]
        if coord_ratio > 1:
            figsz[0] = figsz[0] / coord_ratio
        else: 
            figsz[1] = figsz[1] * coord_ratio
    
    # MAP
    print "\t creating map object"
    fig = plt.figure(figsize=figsz)
    
    m = Basemap(llcrnrlon  = minLon,
              llcrnrlat  = minLat,
              urcrnrlon  = maxLon,
              urcrnrlat  = maxLat,
              resolution = res[0],
              projection = 'cyl',
              #~ lon_0 = minLon+(maxLon-minLon)/2,
              #~ lat_0 = minLat+(maxLat-minLat)/2,
              area_thresh=100000)
    # MAP FEATURES
    
    print "\t drawing coastlines and continents"
    
    m.fillcontinents(color='#DEDEDE')
    m.drawcoastlines(linewidth=1)
    
    if not pvmax: pvmax = 0
    
    # BATHYMETRY
    
    if bath and (bath!='marble') and (bath!='none'):
        print "\t processing bathymetry"
        bathfile = '/home/luke/Dropbox/Data/ETOPO/ETOPO1_Ice_g_gmt4.grd'
        nc = netcdf_file(bathfile,'r')
        
        ncX = nc.variables['x'][::i]
        ncY = nc.variables['y'][::i]
        ncZ = nc.variables['z'][::i,::i]
        ncXind = (ncX>minLon-.0002) & (ncX<maxLon+.0002)
        ncYind = (ncY>minLat-.0002) & (ncY<maxLat+.0002) 
        
        X = ncX[ncXind]
        Y = ncY[ncYind]
        Z = sp.array([z[ncXind] for z in ncZ[ncYind]])
        X,Y = m(*meshgrid( X, Y))
    
    if (bath is 'color') or (bath is 'both'):
        print "\t plotting colour bathymetry "
        m.pcolormesh(X,Y,Z,cmap=cmap,vmin=pvmin,vmax=pvmax)
        colorbar()
    
    if (bath is 'contour') or (bath is 'both'):
        print "\t plotting contour bathymetry"
        
        contours = m.contour(X,Y,Z,levels=lvls,colors='gray',linestyles='-',linewidths=1.,alpha=1.0)#
        clabel(contours,fmt='%.0f', fontsize=6) 
        

    # GRIDLINES
    print "\t adding axis labels"
    pstep = None
    mstep = None
    for degs in [10,20,50,100]:
        if (latd<=degs) & (not pstep):pstep=degs/10
        if (lond<=degs) & (not mstep):mstep=degs/10
    if not pstep: pstep=20
    if not mstep: mstep=20
    if pstep>mstep:mstep=pstep
    if mstep>pstep:pstep=mstep
    parallels = arange(floor(minLat),ceil(maxLat)+1,pstep)
    meridians = arange(floor(minLon),ceil(maxLon)+1,mstep)

    if len(meridians)>10:meridians=meridians[::2]
    m.drawparallels(parallels,color='k',labels=[1,0,0,0],linewidth=0.0,dashes=[1,3])#,fontsize=6)
    m.drawmeridians(meridians,color='k',labels=[0,0,1,0],linewidth=0.0,dashes=[1,3],)#fontsize=6)

    return m


if __name__=='__main__':
    
    """
    To make selection map appear faster remove the colour shading 
    by adding the option: bm = None
    if nothing is selected the global range will be applied
    
    bathmap options:
    bath = bathymetry output type (contour, [color], both)
    lvls = contour levels [np.arange(-6000,8000,500)]
    cmap = colormap used  [cm.Sepctral_r]
    pvmin = minimum depth for color bathymetry [min depth]
    pvmax = maximum depth for color bathymetry [0m]
    resin = coastline resolution  (f,[i],l,c)
    
    add scatter of plot data
    """
    globmap()

    lat = [coords.y2,coords.y1,]
    lon = [coords.x1,coords.x2,]
    
    print lat ,lon
    m = bath_map(lat,lon,
        #~ bath  = 'color',
        #~ lvls = [-200,-500,-1000], 
        #~ cmap  = cm.jet,
        #~ pvmin = -1000,
        #~ pvmax = 0,
        resin = 'l',
        #~ figsz = [10,10]
        )
    
    
    #~ m.drawcoastlines(linewidth=1.0)
    #~ m.drawrivers(linewidth=1.0,color='gray')
    #~ m.drawcountries(linewidth=1.0)
    #~ m.drawmapscale(16,-34.5,16,-32.5,150,barstyle='fancy',units='km',fontsize=6)
    
    #~ sname = 'C:/Users/Luke/Desktop/map.pdf'
    #~ savefig(sname)
    show()
