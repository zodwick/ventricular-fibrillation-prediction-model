import wfdb
import math
from wfdb import processing  # for xqrs detection
import statistics
import csv
import numpy as np


def writecsv(filename:str, data:dict):
    with open(filename , 'w') as f:
        for key, value in data.items():
            f.write(f'{key},{value}\n')


rmeans = {'filename': 'rmean'}
rstandard_deviation = {'filename': 'rstd'}
rinvalid = []
peak_areas_sum = {'filename': 'peak_areas_sum'}
peak_areas_std={'filename':'peak_areas_std'}




def mean_std(file_name, start, stop):
    peak_areas=[]

    file_destination = file_name
    sig, fields = wfdb.rdsamp(file_destination, channels=[
                              0], sampfrom=start, sampto=stop)
    xqrs = processing.XQRS(sig=sig[:, 0], fs=fields['fs'])
    xqrs.detect()
    
    # print(fields)
    wfdb.plot_items(signal=sig, ann_samp=[xqrs.qrs_inds]  )

    # sqrs.qrs_inds is array containing indexes of qrs ?

    rpeaksum = 0
    for i in xqrs.qrs_inds:
        rpeaksum += sig[i]
    try:
        rmean = (rpeaksum/len(xqrs.qrs_inds))
        rmeans[file_name] = float(rmean)
        rstdsum = 0
        for i in xqrs.qrs_inds:
            rstdsum += (sig[i]-rmean)**2
        rstd = math.sqrt(rstdsum/len(xqrs.qrs_inds))
        # print("standard deviation is",rstd)
        rstandard_deviation[file_name] = float(rstd)
        
        
        
#finding peak areas
        
        peak_areas = []
        for i in range(len(xqrs.qrs_inds)):
            peak_start = xqrs.qrs_inds[i]-10
            peak_end = xqrs.qrs_inds[i]+10
            # print(peak_start, peak_end)
            peak_signal = sig[peak_start:peak_end]
            # wfdb.plot_items(signal=peak_signal)
            # print(peak_signal.flatten())
            peak_area = np.trapz(peak_signal.flatten())
            peak_areas.append(abs(peak_area))
            # print("area", peak_area)
        peak_areas_sum[file_name]=sum(peak_areas)
        peak_areas_std[file_name]=statistics.stdev(peak_areas)
        

    except ZeroDivisionError:
        rinvalid.append(file_name)



    
    
    
    



def main():
    file_path =r"D:\vf predict\normal_ecg\16265"
    mean_std(file_path, 0, 375000)

        
    print(rmeans)
    print(rinvalid)
    print(rstandard_deviation)
    print(peak_areas_sum)
    print(peak_areas_std)

    
    


    

main()

