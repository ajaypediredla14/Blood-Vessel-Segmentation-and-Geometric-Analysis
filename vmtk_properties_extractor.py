from vmtk import vmtkscripts
import jdata as jd
import json
import numpy as np
from json import JSONEncoder


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        return JSONEncoder.default(self, obj)

surfaceReader = vmtkscripts.vmtkSurfaceReader()
surfaceReader.InputFileName = 'foo_centerlines5.vtp'
surfaceReader.Execute()
clNumpyAdaptor = vmtkscripts.vmtkCenterlinesToNumpy()
clNumpyAdaptor.Centerlines = surfaceReader.Surface
clNumpyAdaptor.Execute()
numpyCenterlines = clNumpyAdaptor.ArrayDict


# jd.save(numpyCenterlines['PointData'],'vessel_geometry_data.json')
json_str = json.dumps({"Vessel_gemotricAnalysis": numpyCenterlines},cls=NumpyArrayEncoder)
# print('Point Data Keys: ', json_str)
      
with open("vessel_geometry_data_no_stenosis.json", "w") as outfile:
    outfile.write(json_str)