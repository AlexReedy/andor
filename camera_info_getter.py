import platform
import time
from andorLib import *
from astropy.io import fits

andor = Andor()
andor.loadLibrary()

connected_cams = andor.GetAvailableCameras()
cam_handle = andor.GetCameraHandle(connected_cams[1]-1)
andor.SetCurrentCamera(cam_handle[1])

initialize = andor.Initialize()

andor.GetCameraSerialNumber()
andor.GetDetector()