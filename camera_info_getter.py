import platform
import time
from andorLib import *
from astropy.io import fits

andor = Andor()
andor.loadLibrary()

connected_cams = andor.GetAvailableCameras()[1]

handle = andor.GetCameraHandle(connected_cams[1])
andor.SetCurrentCamera(handle[1])

initialize = andor.Initialize()

serial = andor.GetCameraSerialNumber()[1]
detector_dim = [andor.GetDetector()[1], andor.GetDetector()[2]]

# Get the number of ADC Channels
num_adc_channels = andor.GetNumberADChannels()[1]

# Vertical Shift Speeds
num_vss = andor.GetNumberVSSpeeds()[1]

# Horizontal Shift Speeds



