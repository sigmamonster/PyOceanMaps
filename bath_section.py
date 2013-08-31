from pylab import *
from scipy.io.netcdf import netcdf_file
from haversine import haversine
rcParams['font.size']=10

global ETOPO1
ETOPO1 = '/home/luke/Dropbox/Data/ETOPO/ETOPO1_Ice_g_gmt4.grd'

class XYCoords:
    def __init__(slef):
        None

def bs_globmap(**kwds):
    from mpl_toolkits.basemap import Basemap
    from scipy.io.netcdf import netcdf_file
    
    print "Drawing selection map"
    
    # MAP
    fig = figure(figsize=[10,4],dpi=100)
    m = Basemap(projection='cyl',
        llcrnrlon=-180,llcrnrlat=-90,
        urcrnrlon=180,urcrnrlat=90,
        resolution='c')
    m.bluemarble(scale=.6)

    parallels = [-60,-30,0,30,60]
    meridians = [-120,-60,0,60,120]   
    m.drawparallels(parallels,color='k',labels=[1,0,0,1],linewidth=1)
    m.drawmeridians(meridians,color='k',labels=[1,0,0,1],linewidth=1)
    
    # Getting the section points
    XYCoords.gate1 = True
    XYCoords.gate2 = True
    
    class LineDrawer(object):
        # Class object to get the section
        # This "exports the line to the bathsection function"
        lines = []
        def draw_line(self):
            # Draw line when two points are selected
            tb = get_current_fig_manager().toolbar
            ax = plt.gca()
            
            xy = plt.ginput(n=2,mouse_add=3,mouse_pop=1,timeout=-1)
            
            XYCoords.x = [p[0] for p in xy]
            XYCoords.y = [p[1] for p in xy]
            line = plt.plot(XYCoords.x,XYCoords.y,'w',lw=2)
            ax.figure.canvas.draw()
            
            self.lines.append(line)
    
    ld = LineDrawer()
    
    fig.subplots_adjust(left=0.06, right=0.67)
    instr = """
    Intstructions:

    1. Zoom into the region of the section
    
    2. Unselect zoom
    
    3. Right click to place points
    4. Left click to remove points
    5. After two points a line will show
    
    6. Close the window to plot a 
        bathymetry section
    
    
    """
    figtext(0.69,0.91,instr,va='top',ha='left')
    
    ld.draw_line()
    show()
    close('all')


def bs_bathsection(lat,lon):
    stnA = [lat[0],lon[0]]
    stnZ = [lat[1],lon[1]]

    minLat, maxLat = min(lat),max(lat)
    minLon, maxLon = min(lon),max(lon)
    
    dist = haversine([stnA[0],stnZ[0],stnA[1],stnZ[1]])
    
    print 'Distance:    %.2f km'%dist

    lond = maxLon-minLon
    latd = maxLat-minLat
    i= 1
    print "Resolution:  %.2f km"%(float(i)*1.852)

    nc = netcdf_file(ETOPO1,'r')
    ncX = nc.variables['x'][::i]
    ncY = nc.variables['y'][::i]
    ncZ = nc.variables['z'][::i,::i]
    ncXind = (ncX>minLon-.0002) & (ncX<maxLon+.0002)
    ncYind = (ncY>minLat-.0002) & (ncY<maxLat+.0002) 

    X = ncX[ncXind]
    Y = ncY[ncYind]
    Z = array([z[ncXind] for z in ncZ[ncYind]])
    
    stnA[1] = X[argmin(abs(X-stnA[1]))]
    stnA[0] = Y[argmin(abs(Y-stnA[0]))]
    stnZ[1] = X[argmin(abs(X-stnZ[1]))]
    stnZ[0] = Y[argmin(abs(Y-stnZ[0]))]
    
    
    if stnA[1] > stnZ[1]:x = arange(stnA[1],stnZ[1],-.1/6)
    if stnA[1] < stnZ[1]:x = arange(stnA[1],stnZ[1],+.1/6)
    
    
    m = (stnA[0]-stnZ[0]) / (stnA[1]-stnZ[1])
    c = -(m*stnA[1] - stnA[0])
    y = m*x + c

    newy = [argmin(abs(Y-v)) for v in y]
    newx = [argmin(abs(X-v)) for v in x]

    figure (figsize = [7,3.5])
    axes ([0.15,0.15,0.75,0.75])

    depths = Z[newy,newx]
    dydx = abs((y[10]-y[30])/(x[10]-x[30]))

    if dydx < 1:
        plot(x,depths,c='k')
        fill_between(x,depths,y2=-10000,color='gray')
        xlim(stnA[1],stnZ[1],)
        xlabel('Longitude ( $^o$E )')
        
        # top axis labels
        ax2 = gca().twiny()
        xtick_label = ['%.0f'%x for x in linspace(0, dist, 10)]
        xtick_pos = linspace(stnA[1],stnZ[1],10)
        ax2.set_xlim(stnA[1],stnZ[1],)
        
        ax2.set_xticks(xtick_pos)
        ax2.set_xticklabels(xtick_label)
        ax2.set_xlabel('Distance (km)')
        
    else:
        plot(y,depths,c='k')
        fill_between(y,depths,y2=-10000,color='gray')
        xlim(stnA[0],stnZ[0],)
        xlabel('Latitude ( $^o$N )')
        
        # top axis labels
        ax2 = gca().twiny()
        xtick_label = ['%.0f'%x for x in linspace(0, dist, 10)]
        xtick_pos = linspace(stnA[0],stnZ[0],10)
        ax2.set_xlim(stnA[0],stnZ[0],)
        
        ax2.set_xticks(xtick_pos)
        ax2.set_xticklabels(xtick_label)
        ax2.set_xlabel('Distance (km)')
    axhline(0,c='k',zorder=-1)
    ylim(min(depths),max(depths))
    ylabel('Depth (m)')

def bs_bathmap(lat, lon):
    
    yr = abs(diff(lat)/10)[0]
    xr = abs(diff(lon)/10)[0]
    r = max([yr,xr])
    print yr, xr
    
    maplat=[min(lat)-r,max(lat)+r]
    maplon=[min(lon)-r,max(lon)+r]
    
    from bath_map import bath_map   
    m = bath_map(maplat,maplon)
    X, Y = m(lon,lat)
    m.plot(X, Y,'k-',lw=3,alpha=0.5)
    m.plot(X, Y,'ko')

def bath_section():
    
    bs_globmap()
    lat, lon = XYCoords.y, XYCoords.x
    
    bs_bathsection(lat,lon)
    bs_bathmap(lat,lon)
    
    show()
    

if __name__ == "__main__":
    bath_section()
