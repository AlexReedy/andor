from andorLib import *
import time
import timeit
import matplotlib.pyplot as plt

default = {"CameraIndex": 0,
           "Handle": 100,
           "Serial": 26265,
           "ReadMode": 4,
           "AcquisitionMode": 1,
           "VSS": 1,
           "OutputAmp": 0,
           "HSS": 3,
           "PreAmpGain": 0,
           "CoolTemp": -90,
           "ExpTime": 0.0,
           "ShutterTTL": 1,
           "ShutterMode": 0,
           "ClosingDelay": 20,
           "OpeningDelay": 20,
           "DetectorWidth": 2088,
           "DetectorHeight": 2048,
           "HorizontalBin": 1,
           "HorizontalStart": 1,
           "VerticalBin": 1,
           "VerticalStart": 1,
           }

config = {"CameraIndex": default["CameraIndex"],
          "Handle": default["Handle"],
          "Serial": default["Serial"],
          "ReadMode": default["ReadMode"],
          "AcquisitionMode": default["AcquisitionMode"],
          "VSS": default["VSS"],
          "OutputAmp": default["OutputAmp"],
          "HSS": default["HSS"],
          "PreAmpGain": default["PreAmpGain"],
          "CoolTemp": default["CoolTemp"],
          "ExpTime": default["ExpTime"],
          "ShutterTTL": default["ShutterTTL"],
          "ShutterMode": default["ShutterMode"],
          "ClosingDelay": default["ClosingDelay"],
          "OpeningDelay": default["OpeningDelay"],
          "DetectorWidth": default["DetectorWidth"],
          "DetectorHeight": default["DetectorHeight"],
          "HorizontalBin": default["HorizontalBin"],
          "HorizontalStart": default["HorizontalStart"],
          "VerticalBin": default["VerticalBin"],
          "VerticalStart": default["VerticalStart"],
          }

keys = ['CameraIndex',
        'Handle',
        'Serial',
        'ReadMode',
        'AcquisitionMode',
        'VSS',
        'OutputAmp',
        'HSS',
        'PreAmpGain',
        'CoolTemp',
        'ExpTime',
        'ShutterTTL',
        'ShutterMode',
        'ClosingDelay',
        'OpeningDelay',
        'DetectorWidth',
        'DetectorHeight',
        'HorizontalBin',
        'HorizontalStart',
        'VerticalBin',
        'VerticalStart']

def set_params():
    andor.SetReadMode(mode=config["ReadMode"])
    andor.SetAcquisitionMode(mode=config["AcquisitionMode"])
    andor.SetVSSpeed(index=config["VSS"])
    andor.SetHSSpeed(typ=config["OutputAmp"], index=config["HSS"])
    andor.SetPreAmpGain(index=config["PreAmpGain"])
    andor.SetShutter(config["ShutterTTL"],
                     config["ShutterMode"],
                     config["ClosingDelay"],
                     config["OpeningDelay"])
    detector_dimensions = andor.GetDetector()
    andor.SetImage(hbin=1, vbin=1, hstart=1, hend=detector_dimensions[1], vstart=1, vend=detector_dimensions[2])
    andor.SetExposureTime(config["ExpTime"])

def cooler_on():
    andor.SetTemperature(config["CoolTemp"])
    andor.CoolerON()

    get_temp = andor.GetTemperature()
    temp = get_temp[1]
    lock = get_temp[0]

    cooldown_counter = 0
    print(f'[COOLING DETECTOR TO {config["CoolTemp"]} C]')

    while lock != 'DRV_TEMP_STABILIZED':
        cooldown_counter = cooldown_counter + 1
        print(f'COOLING [{cooldown_counter}, {temp}, {lock}]')

        time.sleep(1)

        get_temp = andor.GetTemperature()
        temp = get_temp[1]
        lock = get_temp[0]

    get_temp = andor.GetTemperature()
    temp = get_temp[1]
    lock = get_temp[0]

    print(f'COOLING [{cooldown_counter}, {temp}, {lock}]')

def take_image():
    andor.StartAcquisition()
    data = []
    andor.GetAcquiredData16(data)
    andor.saveFits(data)


andor = Andor()
andor.loadLibrary()































