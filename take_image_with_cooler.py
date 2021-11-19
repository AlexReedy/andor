from andorLib import *
import time
import matplotlib.pyplot as plt

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
    init = andor.Initialize()
    print(f'Camera Initialization: [{init}]')

    read_mode = andor.SetReadMode(mode=4)
    print(f'Setting Readout Mode: [{read_mode}]')

    andor.SetAcquisitionMode(mode=1)
    andor.SetVSSpeed(index=1)
    andor.SetHSSpeed(typ=0, index=2)
    andor.SetPreAmpGain(index=0)


    andor.SetShutter(1, 0, 20, 20)
    detector_dimensions = andor.GetDetector()
    andor.SetImage(hbin=1, vbin=1, hstart=1, hend=detector_dimensions[1], vstart=1, vend=detector_dimensions[2])
    andor.GetDetector()
    andor.GetCameraSerialNumber()

def begin_cooling():
    cool_to_temp = -90
    andor.SetTemperature(cool_to_temp)

    andor.CoolerON()

    get_temp = andor.GetTemperature()
    temp = get_temp[1]
    lock = get_temp[0]

    cooldown_counter = 0

    print(f'[COOLING DETECTOR TO {cool_to_temp} C]')

    while lock != 'DRV_TEMP_STABILIZED':
        cooldown_counter = cooldown_counter + 1
        print(f'COOLING [{cooldown_counter}, {temp}, {lock}]')
        ax.errorbar(cooldown_counter, temp, linestyle='none', marker='s', ms=2, color='black')
        ax.axhline(cool_to_temp, linewidth=1, color='red')
        plt.pause(1)
        get_temp = andor.GetTemperature()
        temp = get_temp[1]
        lock = get_temp[0]

    plt.ion()
    get_temp = andor.GetTemperature()
    temp = get_temp[1]
    lock = get_temp[0]
    print(f'COOLING [{cooldown_counter}, {temp}, {lock}]')


def take_image():
    exp_time = float(input('Input Exp Time: '))
    andor.SetExposureTime(exp_time)
    andor.StartAcquisition()
    data = []
    andor.GetAcquiredData16(data)
    # andor.SaveAsFITS(FileTitle='test.fits', typ=0)
    andor.saveFits(data)

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
                take_image()
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
