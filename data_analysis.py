import json
import matplotlib.pyplot as pp
import numpy as np
=
f = open('vessel_geometry_data5.json')


# Function to calculate diameter reduction
def calculate_diameter_reduction(radii):
    normal_radius = np.max(radii)
    stenotic_radius = np.min(radii)
    diameter_reduction = (normal_radius - stenotic_radius) / normal_radius
    return diameter_reduction

# Function to calculate cross-sectional area reduction
def calculate_cross_sectional_area_reduction( radii):
    max_area = np.pi * (np.max(radii) / 2) ** 2
    area = np.pi * (np.min(radii) / 2) ** 2
    area_reduction = (max_area - area)/ max_area
    return area_reduction


def relative_gradient(radii):
    gradient = np.gradient(radii)
    rel_gradient = gradient / mean_value
    max_idx = np.argmax(rel_gradient)
    return rel_gradient[max_idx]





  
data = json.load(f)


# # print(data['Vessel_gemotricAnalysis'].keys())
RadiusArraysize=len(data['Vessel_gemotricAnalysis']['PointData']['MaximumInscribedSphereRadius'])
print("numberOfSpeheres: ",RadiusArraysize)
SphereRadiusWithPoints=[]
for i in range(0,len(data['Vessel_gemotricAnalysis']['PointData']['MaximumInscribedSphereRadius'])):
    # print(i)
    SphereRadiusWithPoints.append(
        {
            'xyz-coords': data['Vessel_gemotricAnalysis']['Points'][i],
            'radius': data['Vessel_gemotricAnalysis']['PointData']['MaximumInscribedSphereRadius'][i],
    })

# print(SphereRadiusWithPoints)
Radiusarray = np.array(data['Vessel_gemotricAnalysis']['PointData']['MaximumInscribedSphereRadius'])

mean_value=np.mean(Radiusarray)
standard_deviation= np.std(Radiusarray)
ration_of_cv=standard_deviation/mean_value

# print("cv: ",ration_of_cv)
# n = 9
  
# avgResult = np.average(Radiusarray.reshape(-1, n), axis=1)

# pp.plot(Radiusarray)
# pp.show()

# pp.plot(avgResult)
# pp.show()

x = np.arange(0, RadiusArraysize, dtype=int)
y = Radiusarray
names = np.array(data['Vessel_gemotricAnalysis']['Points'])

fig,ax = pp.subplots()
sc = pp.scatter(x,y, s=10)

annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

def update_annot(ind):
    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text =  [names[n] for n in ind["ind"]]
    annot.set_text(text)
    # annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
    # annot.get_bbox_patch().set_alpha(0.4)


def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", hover)

pp.show()

  
f.close()