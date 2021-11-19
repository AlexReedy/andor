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
andor.SetReadMode(mode=4)
andor.SetAcquisitionMode(mode=1)
andor.SetVSSpeed(index=1)
andor.SetHSSpeed(typ=0, index=2)
andor.SetPreAmpGain(index=0)

andor.SetExposureTime(0.1)
andor.SetShutter(1, 0, 20, 20)
detector_dimensions = andor.GetDetector()
andor.SetImage(hbin=1, vbin=1, hstart=1, hend=detector_dimensions[1], vstart=1, vend=detector_dimensions[2])

andor.StartAcquisition()
data = []
andor.GetAcquiredData16(data)
andor.saveFits()


