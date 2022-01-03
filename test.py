import time
import timeit
import numpy as np
import pandas as pd
import sys


def startacqu(index):
    if index == 0:
        time.sleep(1.5)
    if index == 1:
        time.sleep(3)
    if index == 2:
        time.sleep(6)
    if index == 3:
        time.sleep(89)


def getdat():
    time.sleep(np.random.randint(1,3))


def savefits():
    time.sleep(np.random.randint(1,3))


def getformattedtime():
    #formatted_time = float(f'{time.time():.1f}')
    formatted_time = np.round(time.time())
    return formatted_time


def format_output(val1, val2):
    output = float(f'{val2-val1:.3f}')
    return output


def printProgressBar(i,max,postText):
    n_bar =100 #size of progress bar
    j= i/max
    sys.stdout.write('\r')
    sys.stdout.write(f"[{'|' * int(n_bar * j):{n_bar}s}] {int(100 * j)}%  {postText}")
    sys.stdout.flush()


def getreadtimes():
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
                printProgressBar(0, steps, 'Starting Acquisition')
                t_0 = getformattedtime()
                startacqu(index=hs_index)

                printProgressBar(1, steps, 'Getting Acquired Data')
                t_1 = getformattedtime()
                getdat()
                t_2 = getformattedtime()

                printProgressBar(2, steps, 'Writing to FITS')
                savefits()
                t_3 = getformattedtime()

                printProgressBar(3, steps, 'Calculating Readout Times')
                t_01 = format_output(t_0, t_1)
                t_02 = format_output(t_0, t_2)
                t_03 = format_output(t_0, t_3)
                '''
                print(f't_01: {t_01}')
                print(f't_02: {t_02}')
                print(f't_03: {t_03}')
                '''
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

print('Beginning Cool Down')
for i in range(15):
    print(f'[time/temp/status]: {i+1} sec / {np.random.randint(25,35)} C / DRV_TEMP_NOT_REACHED')
    time.sleep(1)
print('Camera Cooled')



























