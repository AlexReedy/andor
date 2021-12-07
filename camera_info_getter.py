import platform
import time
from andorLib import *
import pandas as pd

# from astropy.io import fits

andor = Andor()
andor.loadLibrary()

connected_cams = (andor.GetAvailableCameras()[1]-1)
print(f'Number of Connected Cameras: {connected_cams}')

handle = andor.GetCameraHandle(connected_cams)[1]
print(f'Camera Handle: {handle}')

andor.SetCurrentCamera(handle[1])
andor.Initialize()

serial = andor.GetCameraSerialNumber()[1]
print(f'Camera Serial Number: {serial}')

detector_dim = [andor.GetDetector()[1], andor.GetDetector()[2]]
print(f'Detector Dimensions: [{detector_dim[0]}, {detector_dim[1]}]')

# Get the number of ADC Channels
num_adc_channels = andor.GetNumberADChannels()[1] - 1
print(f'Number of ADC Channels: {num_adc_channels}')

# Number of Available Vertical Shift Speeds
num_vss = (andor.GetNumberVSSpeeds()[1] - 1)
print(f'Number of Available Vertical Shift Speeds: {num_vss}')

# Get the value of the VSS based on the index
vs_speeds = []
print(f'Vertical Shift Speed Values')
for vss_index in range(num_vss):
    vs_speeds.append([andor.GetVSSpeed(vss_index)])
    print(f'Vertical Shift Speed [Index {vss_index}]: {andor.GetVSSpeed(vss_index)} Microseconds Per Pixel Shift')

# Get Number of Available Horizontal Shift Speeds Per AD Channel
output_amp_dict = {0: 'Electron Multiplied',
                   1: 'Conventional'}

for channel in range(num_adc_channels):
    print(f'ADC Channel: {channel}')
    for output_amp in range(2):
        num_hss = andor.GetNumberHSSpeed(channel, output_amp)[1]-1
        print(f' > Number of HS Speeds Available for Output Amp [{output_amp}]: {num_hss}')
        for hss_index in range(num_hss):
            hss_speed = andor.GetHSSpeed(channel, output_amp, hss_index)
            print(f'    > HSS Index {hss_index}: {hss_speed} MHz')








