from vmtk import vmtkscripts
import json
import numpy as np
from json import JSONEncoder
import matplotlib.pyplot as pp


# class NumpyArrayEncoder(JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, np.ndarray):
#             return obj.tolist()
#         if isinstance(obj, np.integer):
#             return int(obj)
#         if isinstance(obj, np.floating):
#             return float(obj)
#         return JSONEncoder.default(self, obj)

surfaceReader = vmtkscripts.vmtkSurfaceReader()
surfaceReader.InputFileName = "C:/Users/Ajay Pediredla/Documents/s5_centerlines.vtp"
surfaceReader.Execute()
clNumpyAdaptor = vmtkscripts.vmtkCenterlinesToNumpy()
clNumpyAdaptor.Centerlines = surfaceReader.Surface
clNumpyAdaptor.Execute()
numpyCenterlines = clNumpyAdaptor.ArrayDict


# jd.save(numpyCenterlines['PointData'],'vessel_geometry_data.json')
# json_str = json.dumps({"Vessel_gemotricAnalysis": numpyCenterlines},cls=NumpyArrayEncoder)
# print("check",numpyCenterlines['PointData'])
RadiusArray = numpyCenterlines['PointData']['MaximumInscribedSphereRadius']
RadiusArraysize=len(RadiusArray)
print("numberOfSpeheres: ",RadiusArraysize)


mean_value=np.mean(RadiusArray)
standard_deviation= np.std(RadiusArray)
ration_of_cv=(standard_deviation/mean_value)*100
print("std: ",standard_deviation)
print("cv: ",ration_of_cv)

# Relative Gradient
gradient = np.gradient(RadiusArray)
# print('Gradient',gradient)
rel_gradient = gradient / mean_value
max_idx = np.argmax(rel_gradient)
print('max_rel_gradient',rel_gradient[max_idx])
thresh = 0.03
if rel_gradient[max_idx] > thresh:
    print("Chances of Stenosis is present : Gradient Method ")
else:
    print("No stenosis is present")




# Relative Diameter Reduction
# min_idx = np.argmin(RadiusArray)
# normal_diam = np.mean(RadiusArray[np.array([min_idx-1, min_idx+1])])
# narrowed_diam = 2 * RadiusArray[min_idx]
# rel_diam_red = narrowed_diam / normal_diam
# thresh = 0.5 # Not known, in most of the cases
# print('Relative_Diameter_Reduction:',rel_diam_red)
# if rel_diam_red < thresh:
#     print("Chances of Stenosis is present : Relative Diameter Reduction")
# else:
#     print("No stenosis is present")


# x = np.arange(0, RadiusArraysize, dtype=int)
# y = RadiusArray
# names = np.array(numpyCenterlines['Points'])

# fig,ax = pp.subplots()
# sc = pp.scatter(x,y, s=10)

# annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot.set_visible(False)

# def update_annot(ind):
#     pos = sc.get_offsets()[ind["ind"][0]]
#     annot.xy = pos
#     text =  [names[n] for n in ind["ind"]]
#     annot.set_text(text)
#     # annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
#     # annot.get_bbox_patch().set_alpha(0.4)


# def hover(event):
#     vis = annot.get_visible()
#     if event.inaxes == ax:
#         cont, ind = sc.contains(event)
#         if cont:
#             update_annot(ind)
#             annot.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot.set_visible(False)
#                 fig.canvas.draw_idle()

# fig.canvas.mpl_connect("motion_notify_event", hover)

# pp.show()
      
