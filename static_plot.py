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
from scipy.optimize import curve_fit
import urllib2
import pandas as pd
import seaborn as sns

from os import listdir

fig, (ax1,ax2) = plt.subplots(1,2,figsize=(10,4))
def PointsInCircum(r,n=100):
    return [(math.cos(2*np.pi/n*x)*r,math.sin(2*np.pi/n*x)*r) for x in xrange(0,n+1)]
#print(PointsInCircum(1,100))
# scatter periods and amplitudes
np.random.seed(0)
sns.set_style("white")
def func(x,m,b,c,d):
    c=c+1
    return m*((x/b)**c)/(1+(x/b)**c)+d

# dominos_sizes=[10,12,14,16]
# pizza_hut_sizes=[6,12,14]
# papa_johns_sizes=[12,14,16]
dominos_sizes=[10,12,14,16]
pizza_hut_sizes=[6,12,14]
papa_johns_sizes=[12,14,16]
meta_sizes=[pizza_hut_sizes,dominos_sizes,papa_johns_sizes]
size_vect=np.array([])
price_vect=np.array([])
color_vect=[]
#### Import data
dirs=["pizza_data/pizza_hut/","pizza_data/dominos/","pizza_data/papa_johns/"]
colors=['red','blue','green']
names=['Pizza Hut','Dominos','Papa Johns']
states=['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
]
state_rank=[]
name_vect=[]
state_vect=[]
mean_vect=[]
mean_array=np.zeros((3,51))
cheapest_pizzas=[]
for l,dir in enumerate(dirs):
    for j,file in enumerate(listdir(dir)):

        values = pickle.load(open(dir+file, 'rb'))[1]
        state=pickle.load(open(dir+file, 'rb'))[0]
        temp_price=[]
        for k,type in enumerate(meta_sizes[l]):
            size_vect=np.append(size_vect,type*np.ones(len(values[k])))
            temp_price=temp_price+values[k]
            price_vect = np.append(price_vect,values[k])
            color_vect.append([colors[l]]*len(values[k]))
            name_vect.append([names[l]]*len(values[k]))
            state_vect.append([state] * len(values[k]))
            cheapest_pizzas.append(values[k][0])
        mean_array[l,j]=np.mean(temp_price)
        state_rank.append(state)
colors = [item for sublist in color_vect for item in sublist]
states = [item for sublist in state_vect for item in sublist]
names = [item for sublist in name_vect for item in sublist]

value_vect=price_vect/(np.pi*(size_vect/2)**2)
P = value_vect
N= price_vect/(np.pi*(size_vect))
A = size_vect+.2*np.random.rand(len(value_vect))-0.1




# points = ax1.scatter(A, P, c=colors, alpha=0.025)
# x_dat=np.linspace(min(A),max(A),100)
# popt,pcov=curve_fit(func,A,P)
# print(popt)
# ax1.plot(x_dat,func(x_dat,popt[0],popt[1],popt[2],popt[3]),color='k',linewidth=3)
#
# ax1.set_title('Total Pizza Value')
# ax1.set_xlabel('Diameter (inches)')
# ax1.set_ylabel('Price per Square Inch')
#
# ax2.scatter(A, N, c=colors,alpha=0.025)
#
# popt,pcov=curve_fit(func,A,N)
#
# ax2.plot(x_dat,func(x_dat,popt[0],popt[1],popt[2],popt[3]),color='k',linewidth=3)
#
# ax1.set_title('Total Pizza Value')
# ax1.set_xlabel('Diameter (inches)')
# ax1.set_ylabel('Price per Inch of Crust')
#
# plt.savefig('static.png')


###ploting swarm
fig2,(ax3,ax4)= plt.subplots(1,2,figsize=(10,4))
d={'Pizza Place':names[0::10],'State':states[0::10],'Prices':price_vect[0::10],'Price per Square Inch of Pizza':value_vect[0::10],'Price per Inch of Crust':N[0::10],'Size (Inches)':size_vect[0::10]}

df=pd.DataFrame(d)
df.drop_duplicates()
sorted_keys, sorted_vals = zip(*sorted(set(zip(np.mean(mean_array,0),state_rank))))
#fig2= plt.figure()
#sns.violinplot(x="Size (Inches)", y="Price per Square Inch of Pizza",hue='Pizza Place',data=df)
sns.swarmplot(x="Size (Inches)", y="Price per Square Inch of Pizza",hue='Pizza Place',data=df,ax=ax3)
sns.swarmplot(x="Size (Inches)", y="Price per Inch of Crust",hue='Pizza Place',data=df,ax=ax4)
ax3.set_title('Pizza Value')
ax4.set_title('Crust Value')
ax4.legend([])
plt.tight_layout()
plt.savefig('swarm.png',dpi=200)


## ploting violin
fig3= plt.figure()
d2={'Pizza Place':names,'State':states,'Prices':price_vect,'Price per Square Inch of Pizza':value_vect,'Price per Inch of Crust':N,'Size (Inches)':size_vect}
df=pd.DataFrame(d2)
df.drop_duplicates()
sorted_keys, sorted_vals = zip(*sorted(set(zip(np.mean(mean_array,0),state_rank))))
sns.violinplot(x="Size (Inches)", y="Price per Square Inch of Pizza",hue='Pizza Place',data=df)
plt.tight_layout()
plt.savefig('violin.png',dpi=200)

### plotting barplot
fig4= plt.figure()
sns.boxplot(x="Prices", y="State",data=df)
plt.tight_layout()
plt.savefig('box.png',dpi=200)

# sns.swarmplot(x="Size (Inches)", y="Price per Square Inch of Pizza", hue="Pizza Place", data=df,ax=ax3)
# ax3.set_title('Pizza Value')
# sns.swarmplot(x="Size (Inches)", y="Price per Inch of Crust", hue="Pizza Place", data=df,ax=ax4)
# ax4.set_title('Crust Value')
# ax4.legend([])
# plt.tight_layout()
# plt.savefig('swarmplot.png',dpi=200)
