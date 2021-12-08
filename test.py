import numpy as np
from andorLib import *

andor = Andor()
andor.loadLibrary()
connected_cams = (andor.GetAvailableCameras()[1])
handle = andor.GetCameraHandle(connected_cams-1)[1]
andor.SetCurrentCamera(handle)
andor.Initialize()

caps = andor.GetCapabilities()




