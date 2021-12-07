import numpy as np
import pandas as pd
def GetNumberHSSpeed(channel, type):
    hss_speeds = np.random.randint(1, 3)
    return hss_speeds
def GetHSSpeed(channel, type, index):
    hss_speed = np.random.randint(1, 3)
    return hss_speed

num_adc_channels = 2

output_amp_dict = {0: 'Electron Multiplied',
                   1: 'Conventional'}
num_hss = 3


for channel in range(num_adc_channels):
    print(f'ADC Channel: {channel}')
    for output_amp in range(2):
        num_hss = GetNumberHSSpeed(channel, output_amp)
        print(f' > Number of HS Speeds Available for Output Amp [{output_amp}]: {num_hss}')
        for hss_index in range(num_hss):
            hss_speed = GetHSSpeed(channel, output_amp, hss_index)
            print(f'    > HSS Index {hss_index}: {hss_speed} MHz')





