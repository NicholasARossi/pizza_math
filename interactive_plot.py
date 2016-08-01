import matplotlib
import textwrap
import matplotlib.pyplot as plt
import numpy as np
import mpld3
from mpld3 import plugins, utils
import math
import matplotlib.patches as mpatches
import matplotlib.cm as cm
import matplotlib.lines as mlines
import pickle
import urllib2
from os import listdir
class LinkedView(plugins.PluginBase):
    """A simple plugin showing how multiple axes can be linked"""

    JAVASCRIPT = """
    mpld3.register_plugin("linkedview", LinkedViewPlugin);
    LinkedViewPlugin.prototype = Object.create(mpld3.Plugin.prototype);
    LinkedViewPlugin.prototype.constructor = LinkedViewPlugin;
    LinkedViewPlugin.prototype.requiredProps = ["idpts", "idline", "data"];
    LinkedViewPlugin.prototype.defaultProps = {}
    function LinkedViewPlugin(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    LinkedViewPlugin.prototype.draw = function(){
      var pts = mpld3.get_element(this.props.idpts);
      var line = mpld3.get_element(this.props.idline);
      var data = this.props.data;

      function mouseover(d, i){
        line.data = data[i];
        line.elements().transition()
            .attr("d", line.datafunc(line.data))
            .style("stroke", this.style.fill);
      }
      pts.elements().on("mouseover", mouseover);
    };
    """

    def __init__(self, points, line, linedata):
        if isinstance(points, matplotlib.lines.Line2D):
            suffix = "pts"
        else:
            suffix = None

        self.dict_ = {"type": "linkedview",
                      "idpts": utils.get_id(points, suffix),
                      "idline": utils.get_id(line),
                      "data": linedata}

fig, (ax1,ax2) = plt.subplots(1,2,figsize=(10,4))
def PointsInCircum(r,n=100):
    return [(math.cos(2*np.pi/n*x)*r,math.sin(2*np.pi/n*x)*r) for x in xrange(0,n+1)]
print(PointsInCircum(1,100))
# scatter periods and amplitudes
np.random.seed(0)


dominos_sizes=[10,12,14,16]
pizza_hut_sizes=[6,12,14]
papa_johns_sizes=[12,14,16]
meta_sizes=[pizza_hut_sizes,dominos_sizes,papa_johns_sizes]
size_vect=np.array([])
price_vect=np.array([])
color_vect=[]
#### Import data
dirs=["pizza_data/pizza_hut/","pizza_data/dominos/","pizza_data/papa_johns/"]

colors=['blue','green','red']
for l,dir in enumerate(dirs):

    # for file in listdir(dir):
    file=listdir(dir)[24]
    values = pickle.load(open(dir+file, 'rb'))[1]
    for k,type in enumerate(meta_sizes[l]):
        size_vect=np.append(size_vect,type*np.ones(len(values[k])))
        price_vect = np.append(price_vect,values[k])
        color_vect.append([colors[l]]*len(values[k]))

colors = [item for sublist in color_vect for item in sublist]
value_vect=price_vect/(np.pi*(size_vect/2)**2)
P = value_vect
A = size_vect



x = np.linspace(0, 1, 101)
#A=np.asarray(A)


x = np.linspace(-1.0, 1.0, 100)
y = np.linspace(-1.0, 1.0, 100)
X, Y = np.meshgrid(x,y)
F = X**2 + Y**2


# for size in Pizza_hut_sizes:
#     datum=PointsInCircum(size, 100)
#     data.append(datum)

data = np.array([zip(*PointsInCircum(size/2,100))
                 for size in size_vect])

points = ax1.scatter(A, P, c=colors,s=200, alpha=0.2)
ax1.set_title('Minnesota Pizza Prices')
ax1.set_xlabel('Diameter (inches)')
ax1.set_ylabel('Price per Square Inch')
# red_line = mlines.Line2D([], [], color='blue',
#                           linewidth=5, label='Pizza Hut')
red_line = mlines.Line2D([], [], color='red',
                           linewidth=5, label='Pizza Hut')
blue_line = mlines.Line2D([], [], color='blue',
                           linewidth=5, label='Dominos')
green_line = mlines.Line2D([], [], color='green',
                          linewidth=5, label='Papa Johns')
#green_patch = mpatches.Patch(color='green')
#
# blue_patch = mpatches.Patch(color='blue', label='Pizza hut')
#ax2.legend([red_line,blue_line,green_line],['Pizza Hut','Dominos','Papa Johns'],loc='center left', bbox_to_anchor=(1, 0.5))





# create the line object


ax2.set(adjustable='box-forced', aspect='equal')

lines = ax2.plot(x, 0 * x, '-w', lw=3, alpha=0.5)
ax2.set_ylim(-10, 10)
ax2.set_xlim(-10, 10)
ax2.set_title("Pizza Shape")

# transpose line data and add plugin
linedata = data.transpose(0, 2, 1).tolist()
plugins.connect(fig, LinkedView(points, lines[0], linedata))


plt.tight_layout()
#mpld3.show()
mpld3.save_html(fig,'minnesota')

# print(textwrap.fill(html,width=140))
#
# # print(textwrap.fill(html))
# #
# #
# #
# #
# #
#
# Html_file= open("graph_html","w")
# Html_file.write(textwrap.fill(html,width=140))
# Html_file.close()