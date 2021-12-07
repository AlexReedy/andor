import platform
import time
from andorLib import *


# from astropy.io import fits

andor = Andor()
andor.loadLibrary()

connected_cams = (andor.GetAvailableCameras()[1])
print(f'Number of Connected Cameras: {connected_cams}')

handle = andor.GetCameraHandle(connected_cams-1)[1]
print(f'Camera Handle: {handle}')

andor.SetCurrentCamera(handle)
andor.Initialize()

serial = andor.GetCameraSerialNumber()[1]
print(f'Camera Serial Number: {serial}')

detector_dim = [andor.GetDetector()[1], andor.GetDetector()[2]]
print(f'Detector Dimensions: [{detector_dim[0]}, {detector_dim[1]}]')

# Get the number of ADC Channels
num_adc_channels = andor.GetNumberADChannels()[1]
print(f'Number of ADC Channels: {num_adc_channels}')

num_amps = andor.GetNumberAmp()[1]
print(f'Number of Output Amplifiers: {num_amps}')

num_preamp_gains = andor.GetNumberPreAmpGains()[1]
print(f'Number of Pre Amp Gains: {num_preamp_gains}')

for i in range(num_preamp_gains):
    print(f'For Gain Index {i} Gain Factor is: {andor.GetPreAmpGain(i)[1]}')
# Number of Available Vertical Shift Speeds
num_vss = (andor.GetNumberVSSpeeds()[1])
num_vss_idx = num_vss
print(f'Number of Available Vertical Shift Speeds: {num_vss}')

# Get the value of the VSS based on the index
print(f'Vertical Shift Speed Values')
for vss_index in range(num_vss):
    print(f'    > Vertical Shift Speed [Index {vss_index}]: {andor.GetVSSpeed(vss_index)[1]} Microseconds Per Pixel Shift')

# Get Number of Available Horizontal Shift Speeds Per AD Channel
output_amp_dict = {0: 'Electron Multiplied',
                   1: 'Conventional'}

print(f'Horizontal Shift Speed Information')

for output_amp in range(num_amps):
    for channel in range(num_adc_channels):
        print(f'ADC Channel: {channel}')
        num_hss = andor.GetNumberHSSpeeds(channel, output_amp)[1]
        print(f' > Number of HS Speeds Available for Output Amp [{output_amp}]: {num_hss}')
        for hss_index in range(num_hss):
            hss_speed = andor.GetHSSpeed(channel, output_amp, hss_index)
            print(f'    > Horizontal Shift Speed [Index {hss_index}]: {hss_speed[1]} MHz')










