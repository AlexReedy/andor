import platform
import time
from andorLib import *
from astropy.io import fits
import matplotlib.pyplot as plt

output_dir = os.path.abspath('/home/alex/fits_images/Andor_test_one.fits')

fig, ax = plt.subplots(nrows=1, ncols=1)
ax.set_ylabel('Detector Temperature [Celsius]')
ax.set_xlabel('Time [Sec]')
ax.set_ylim(ymin=-100, ymax=60)

run_command = input('[SYSTEM MESSAGE] Begin Initialization? [y/n]: ')
if run_command == 'y':
    andor = Andor()
    andor.loadLibrary()

    print('[DETECTING OPERATING SYSTEM]')
    print(f' -> OS INFO = {platform.platform()}')

    print('[DETERMINING NUMBER OF CONNECTED CAMERAS]')
    connected_cams = andor.GetAvailableCameras()
    print(f' -> STATUS: [{connected_cams[0]}]')
    print(f' -> CONNECTED CAMERAS: {connected_cams[1]}')

    print(f'[DETERMINING CAMERA HANDLE]')
    cam_handle = andor.GetCameraHandle(connected_cams[1]-1)
    print(f' -> STATUS: [{cam_handle[0]}]')
    print(f' -> CAMERA HANDLE: {cam_handle[1]}')

    print(f'[SETTING ACTIVE CAMERA TO HANDLE]')
    cam_set = andor.SetCurrentCamera(cam_handle[1])
    print(f' -> STATUS: [{cam_set}]')

    initialize_command = input('[SYSTEM MESSAGE] Initialize Camera? [y/n]: ')
    if initialize_command == 'y':
        cool_to_temp = -30
        print(f'[INITIALIZING CAMERA]')
        initialize = andor.Initialize()
        print(f' -> STATUS = [{initialize}]')

        andor.SetReadMode(mode=4)
        andor.SetAcquisitionMode(mode=1)

        andor.SetVSSpeed(index=1)
        andor.SetHSSpeed(typ=0, index=2)
        andor.SetPreAmpGain(index=0)

        andor.SetExposureTime(0.1)
        andor.SetShutter(1, 0, 20, 20)
        detector_dimensions = andor.GetDetector()
        andor.SetImage(hbin=1, vbin=1, hstart=1, hend=detector_dimensions[1], vstart=1, vend=detector_dimensions[2])

        andor.GetDetector()

        take_image_command = input('[SYSTEM MESSAGE] Take Image? [y/n]: ')
        if take_image_command == 'y':

            andor.StartAcquisition()

            data = []
            print(len(data))

            andor.GetAcquiredData16(data)
            andor.SaveAsFITS(FileTitle='test.fits', typ=0)

            #andor.saveFits(data)


        if take_image_command == 'n':
            print('Image Acquisition Cancelled: Shutting Down')

    if initialize_command == 'n':
        print('Initialization Cancelled: Shutting Down')

if run_command == 'n':
    print('Initialization Cancelled: Shutting Down')