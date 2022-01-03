from andorLib import *
import time
import matplotlib.pyplot as plt
import timeit
import numpy as np
import pandas as pd
import sys

andor = Andor()
andor.loadLibrary()

fig, ax = plt.subplots(nrows=1, ncols=1)
ax.set_ylabel('Detector Temperature [Celsius]')
ax.set_xlabel('Time [Sec]')
ax.set_ylim(ymin=-100, ymax=60)
plt.ioff()

def getformattedtime():
    #formatted_time = float(f'{time.time():.1f}')
    formatted_time = np.round(time.time())
    return formatted_time

def format_output(val1, val2):
    output = float(f'{val2-val1:.3f}')
    return output

def printProgressBar(i,max,postText):
    n_bar =25 #size of progress bar
    j= i/max
    sys.stdout.write('\r')
    sys.stdout.write(f"[{'=' * int(n_bar * j):{n_bar}s}] {int(100 * j)}%  {postText}")
    sys.stdout.flush()

def user_input_prompt(prompt_message):
    prompt = input(f'[USER INPUT] {prompt_message}? (y/n): ')
    return prompt


def sys_message(message, next_op):
    print(f'[SYSTEM MESSAGE] {message}: {next_op}')


def pre_initialization():
    connected_cams = andor.GetAvailableCameras()
    print(f'Getting Number of Connected Cameras: [{connected_cams[0]}]')

    cam_handle = andor.GetCameraHandle(connected_cams[1]-1)
    print(f'Getting Camera Handle: [{cam_handle[0]}]')

    set_cam = andor.SetCurrentCamera(cam_handle[1])
    print(f'Setting Active Camera: [{set_cam}]')


def initialize_camera():
    andor.Initialize()
    andor.SetReadMode(mode=4)
    andor.SetAcquisitionMode(mode=1)
    andor.SetShutter(1, 0, 20, 20)
    andor.SetADChannel(0)
    detector_dimensions = andor.GetDetector()
    andor.SetImage(hbin=1, vbin=1, hstart=1, hend=detector_dimensions[1], vstart=1, vend=detector_dimensions[2])
    andor.GetDetector()
    andor.GetCameraSerialNumber()

def begin_cooling():
    cool_to_temp = -90
    andor.SetTemperature(cool_to_temp)
    cooling_data = [[], []]

    andor.CoolerON()

    get_temp = andor.GetTemperature()
    temp = get_temp[1]
    lock = get_temp[0]

    cooldown_counter = 0

    cooling_data[0].append(cooldown_counter)
    cooling_data[1].append(temp)

    print(f'[COOLING DETECTOR TO {cool_to_temp} C]')

    while lock != 'DRV_TEMP_STABILIZED':
        cooldown_counter = cooldown_counter + 1

        print(f'COOLING [{cooldown_counter}, {temp}, {lock}]')

        cooling_data[0].append(cooldown_counter)
        cooling_data[1].append(temp)

        time.sleep(1)

        get_temp = andor.GetTemperature()
        temp = get_temp[1]
        lock = get_temp[0]


    get_temp = andor.GetTemperature()
    temp = get_temp[1]
    lock = get_temp[0]

    cooling_data[0].append(cooldown_counter)
    cooling_data[1].append(temp)

    print(f'COOLING [{cooldown_counter}, {temp}, {lock}]')
    ax.errorbar(cooling_data[0], cooling_data[1], linestyle='none', marker='s', ms=2, color='black')
    ax.axhline(cool_to_temp, linewidth=1, color='red')
    plt.savefig(f'/home/alex/fits_images/savefits_tests/cooling_plot.png')

def take_images_for_readout_times():
    exp_time = 0.0
    pag_dict = {0: 1.00,
                1: 2.00,
                2: 4.00
                }

    vss_dict = {0: 38.0,
                1: 76.0
                }

    hss_dict = {0: 5.00,
                1: 3.00,
                2: 1.00,
                3: 0.05
                }

    d = {'Indices': [],
         'PAG': [],
         'VSS (um)': [],
         'HSS (MHz)': [],
         't_01': [],
         't_02': [],
         't_03': [],
         't_12': [],
         't_13': [],
         't_23': []
         }

    readtime_data = []
    counter = 1
    steps = 5
    for pag_index in range(3):
        for vs_index in range(2):
            for hs_index in range(4):
                print(f'{pag_index},{vs_index},{hs_index} [{counter} of 24]')
                andor.SetExposureTime(exp_time)
                andor.SetPreAmpGain(pag_index)
                andor.SetVSSpeed(vs_index)
                andor.SetHSSpeed(typ=0, index=hs_index)

                printProgressBar(0, steps, 'Starting Acquisition')
                t_0 = getformattedtime()
                andor.StartAcquisition()

                printProgressBar(1, steps, 'Getting Acquired Data')
                t_1 = getformattedtime()
                data = []
                andor.GetAcquiredData16(data)
                t_2 = getformattedtime()

                printProgressBar(2, steps, 'Writing to FITS')
                andor.saveFits()
                t_3 = getformattedtime()

                printProgressBar(3, steps, 'Calculating Readout Times')
                t_01 = format_output(t_0, t_1)
                t_02 = format_output(t_0, t_2)
                t_03 = format_output(t_0, t_3)


                t_12 = format_output(t_1, t_2)
                t_13 = format_output(t_1, t_3)
                '''
                print(f't_12: {t_12}')
                print(f't_13: {t_13}')
                '''
                t_23 = format_output(t_2, t_3)
                # print(f't_23: {t_23}')


                indicies = f'({pag_index},{vs_index},{hs_index})'

                printProgressBar(4, steps, 'Creating Data Frame')
                d['Indices'].append(indicies)
                d['PAG'].append(pag_dict[pag_index])
                d['VSS (um)'].append(vss_dict[vs_index])
                d['HSS (MHz)'].append(hss_dict[hs_index])
                d['t_01'].append(t_01)
                d['t_02'].append(t_02)
                d['t_03'].append(t_03)
                d['t_12'].append(t_12)
                d['t_13'].append(t_13)
                d['t_23'].append(t_23)
                printProgressBar(5, steps, 'Complete')
                counter = counter + 1

                print('\n')
    readtime_df = pd.DataFrame(data=d)
    print(readtime_df)


def take_image():
    # exp_time = float(input('Input Exp Time: '))
    exp_time = 0.0
    pre_amp_gain_index = int(input('Input Pre Amp Gain Index: '))
    vs_index = int(input('Input Vertical Shift Speed Index: '))
    hs_index = int(input('Input Horizontal Shift Speed Index: '))


    andor.SetExposureTime(exp_time)
    andor.SetPreAmpGain(pre_amp_gain_index)
    andor.SetVSSpeed(vs_index)
    andor.SetHSSpeed(typ=0, index=hs_index)

    andor.StartAcquisition()

    start_time = timeit.default_timer()

    data = []

    andor.GetAcquiredData16(data)

    end_time_1 = timeit.default_timer()
    read_time_1 = end_time_1 - start_time
    print(f'PAG_{pre_amp_gain_index}_VSS_{vs_index}_HSS_{hs_index}_runtime_1: {read_time_1}')

    andor.saveFits()

    end_time_2 = timeit.default_timer()
    read_time_2 = end_time_2 - start_time
    print(f'PAG_{pre_amp_gain_index}_VSS_{vs_index}_HSS_{hs_index}_runtime_2: {read_time_2}')

def cool_up():
    get_temp = andor.GetTemperature()
    temp = get_temp[1]
    lock = get_temp[0]

    andor.CoolerOFF()
    coolup_counter = 0

    print(f'[Waiting for Detector to Warm Above -20 C]')

    while temp <= -20:
        coolup_counter = coolup_counter + 1
        print(f'COOLING [{coolup_counter}, {temp}, {lock}]')
        time.sleep(1)
        get_temp = andor.GetTemperature()
        temp = get_temp[1]
        lock = get_temp[0]


def shutdown():
    get_temp = andor.GetTemperature()
    temp = get_temp[1]

    if temp >= -20:
        andor.ShutDown()


pre_init_command = user_input_prompt('Begin Pre-Initialization')
if pre_init_command == 'y':
    # pre init functions go here
    pre_initialization()
    sys_message('Pre-Initialization Complete', 'Ready to Initialize Camera')

    init_camera_command = user_input_prompt('Initialize Camera')
    if init_camera_command == 'y':
        # camera init functions go here
        initialize_camera()
        sys_message('Initialization Complete', 'Ready to Begin Cooling')

        cooling_on_command = user_input_prompt('Turn Cooler ON')
        if cooling_on_command == 'y':
            # cooling on function goes here
            begin_cooling()
            sys_message('Cooling Complete', 'Ready to Begin Acquisition')

            start_acquisition_command = user_input_prompt('Start Acquisition')
            if start_acquisition_command == 'y':
                # start acquisition function goes here
                take_images_for_readout_times()
                sys_message('Acquisition Complete', 'Ready to Cool Up')

                cooling_off_command = user_input_prompt('Turn Cooler OFF')
                while cooling_off_command == 'n':
                    take_additional_acquisition_command = user_input_prompt('Begin Another Acquisition')
                    # start acquisition function goes here
                    take_image()
                    sys_message('Acquisition Complete', 'Ready to Cool Up')

                    cooling_off_command = user_input_prompt('Turn Cooler OFF')
                # Cool up function goes here
                cool_up()
                sys_message('Cool Up Completed', 'Shutting Down')
                # Shut down function goes here
                andor.ShutDown()

            if start_acquisition_command == 'n':
                sys_message('Acquisition Cancelled', 'Please Wait for Camera to Cool Up')
                # Cool up function goes here
                cool_up()
                sys_message('Cool Up Completed', 'Shutting Down')
                # Shut down function goes here
                andor.ShutDown()

        if cooling_on_command == 'n':
            sys_message('Cooling Cancelled', 'Shutting Down')
            andor.ShutDown()

    if init_camera_command == 'n':
        sys_message('Camera Initialization Cancelled', 'Shutting Down')
        andor.ShutDown()

if pre_init_command == 'n':
    sys_message('Pre-Initialization Cancelled', 'Shutting Down')