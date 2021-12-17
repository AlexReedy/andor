from andorLib import *
import time
import matplotlib.pyplot as plt
import timeit

andor = Andor()
andor.loadLibrary()

fig, ax = plt.subplots(nrows=1, ncols=1)
ax.set_ylabel('Detector Temperature [Celsius]')
ax.set_xlabel('Time [Sec]')
ax.set_ylim(ymin=-100, ymax=60)
plt.ioff()


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
    readtime_data = []
    for pag_index in range(3):
        for vs_index in range(2):
            for hs_index in range(4):
                andor.SetExposureTime(exp_time)
                andor.SetPreAmpGain(pag_index)
                andor.SetVSSpeed(vs_index)
                andor.SetHSSpeed(typ=0, index=hs_index)

                t_0 = timeit.default_timer()

                andor.StartAcquisition()

                t_1 = timeit.default_timer

                data = []
                andor.GetAcquiredData16(data)

                t_2 = timeit.default_timer

                andor.saveFits()

                t_3 = timeit.default_timer

                t_01 = np.round(t_1 - t_0, 4)
                t_02 = np.round(t_2 - t_0, 4)
                t_03 = np.round(t_3 - t_0, 4)

                t_12 = np.round(t_2 - t_1, 4)
                t_13 = np.round(t_3 - t_1, 4)

                t_23 = np.round(t_3 - t_2, 4)

                row = [pag_index, vs_index, hs_index, t_01, t_02, t_03, t_12, t_13, t_23]
                readtime_data.append(row)


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

    readout_time = andor.GetReadOutTime()
    print(f'GetReadOutTime Return: {readout_time[1]}')

    start_time = timeit.default_timer()

    andor.StartAcquisition()

    end_time = timeit.default_timer()
    read_time = end_time - start_time
    print(f'PAG_{pre_amp_gain_index}_VSS_{vs_index}_HSS_{hs_index}_runtime: {read_time}')

    data = []
    andor.GetAcquiredData16(data)
    # andor.SaveAsFITS(FileTitle='test.fits', typ=0)
    andor.saveFits()

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
