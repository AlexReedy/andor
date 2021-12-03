import platform
import time
from andorLib import *
from astropy.io import fits

andor = Andor()
andor.loadLibrary()

connected_cams = andor.GetAvailableCameras()
handle = andor.GetCameraHandle(connected_cams[1]-1)
andor.SetCurrentCamera(handle[1])

initialize = andor.Initialize()

serial = andor.GetCameraSerialNumber()[1]
detector_dim = [andor.GetDetector()[1], andor.GetDetector()[2]]
num_vss = andor.GetNumberVSSpeeds()[1]
num_hss = andor.GetNumberHSSpeeds()[1]

