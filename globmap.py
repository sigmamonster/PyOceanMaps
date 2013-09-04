#! /bin/python
# marble global map for selection

from pylab import *
global rect 
rcParams['font.size'] = 8
rcParams['font.family'] = 'monospace'

class xy:
    
    def __init__(self):
        self.y = [-90, 90]
        self.x = [-180, 180]
        self.adjuster = 1.
        self.i = 1

xy = xy()

def onselect(eclick, erelease):
    xy.y[0], xy.y[1] = sort([erelease.ydata, eclick.ydata])
    xy.x[0], xy.x[1] = sort([erelease.xdata, eclick.xdata])
    
    draw_selection()
    
def draw_selection():   
    # add the new selection rectangle
    gca().add_patch(Rectangle(( xy.x[0],xy.y[0]),
                                xy.x[1]-xy.x[0],
                                xy.y[1]-xy.y[0],
                                edgecolor='orange',
                                linewidth=3,
                                facecolor='none',
                                alpha=.5))
    
    # add the cooridinates in the description text
    text_bg = {'fc':'#BBBBBB', 'ec':'none', 'pad':20}
    gcf().text(0.8,  0.3, "%.2f"%xy.y[1],bbox=text_bg)
    gcf().text(0.74, 0.25,"%.2f"%xy.x[0],bbox=text_bg)
    gcf().text(0.86, 0.25,"%.2f"%xy.x[1],bbox=text_bg)
    gcf().text(0.8, 0.2, "%.2f" %xy.y[0],bbox=text_bg)
    
    yr = .15 * (xy.y[1] - xy.y[0])
    xr = .15 * (xy.x[1] - xy.x[0])
    gca().set_ylim(xy.y[0]-yr, xy.y[1]+yr)
    gca().set_xlim(xy.x[0]-xr, xy.x[1]+xr)
    
    gcf().canvas.draw()

def remove_rect(even):
    # remove the previous rectangle patch
    try: 
        gca().findobj(matplotlib.patches.Rectangle)[0].remove()
        gcf().canvas.draw()
    except:
        pass

def reset_fig(event):
    if event.key in ['R','r']:
        gca().set_ylim(-90, 90)
        gca().set_xlim(-180,180)
        
        remove_rect(None)

def adjust_lims(event):
    
    if event.key == ' ':
        xy.i = int(~bool_(xy.i))
    i = xy.i
    
    if event.key == 'shift':
        if xy.adjuster == 1.:
            xy.adjuster = 10.
        else:
            xy.adjuster = 1.
        
    elif event.key == 'right':
        xy.x[i] = around(xy.x[i]) + xy.adjuster
    elif event.key == 'left':
        xy.x[i] = around(xy.x[i]) - xy.adjuster
    elif event.key == 'up':
        xy.y[i] = around(xy.y[i]) + xy.adjuster
    elif event.key == 'down':
        xy.y[i] = around(xy.y[i]) - xy.adjuster
    
    gca().findobj(matplotlib.lines.Line2D)[-1].remove()
    plot(xy.x[i], xy.y[i],'oy',mew=0)
    
    remove_rect(None)
    draw_selection()

def toggle(event):
    if event.button==3 and toggle.RS.active:
        print "off"
        toggle.RS.set_active(False)
    elif event.button==3 and not toggle.RS.active:
        print "on"
        toggle.RS.set_active(True)

def globmap(**kwargs):
    from mpl_toolkits.basemap import Basemap
    from scipy.io.netcdf import netcdf_file
    
    print "Drawing selection map"
    
    # draw and set up map
    fig = figure(figsize=[10,4],dpi=100)
    m = Basemap(projection='cyl',
                llcrnrlon=-180, llcrnrlat=-90,
                urcrnrlon= 180, urcrnrlat= 90,
                resolution='c')
    m.bluemarble(scale=.1)

    parallels = [-60, -30,0,30, 60]
    meridians = [-120,-60,0,60,120]   
    m.drawparallels(parallels,color='k',labels=[1,0,0,1],linewidth=1)
    m.drawmeridians(meridians,color='k',labels=[1,0,0,1],linewidth=1)
    
    fig.subplots_adjust(left=0.06, right=0.67)
    instr = kwargs.get("instructions","")
    
    figtext(0.69, 0.91, instr, 
            va='top', ha='left',
            size=8)
    
    if kwargs.get('rectangle'):
        from matplotlib.widgets import  RectangleSelector
        toggle.RS = RectangleSelector(gca(), onselect, 
                                        useblit=True,
                                        drawtype='box',
                                        button=[1],
                                        rectprops = dict( facecolor='orange', 
                                                    edgecolor = 'black',
                                                    alpha=0.3, fill=True))
        connect('button_press_event', toggle)
        connect('button_press_event', remove_rect)
        connect('key_press_event', reset_fig)
        connect('key_press_event', adjust_lims)
    
    show()

def test1(): # display input from mouse
    instr = """
    Intstructions:

    A basic string with 3x" to explain
    what should be done in this plot,
    
    i.e. draw a section, zoom in on 
    plotting region.
    """
    globmap(instructions=instr, rectangle=True)
    
    

if __name__ == "__main__":
    
    test1()
