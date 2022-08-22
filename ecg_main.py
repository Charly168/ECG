# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 07:41:45 2022

@author: HP
"""
import matplotlib.pyplot as plt
import data_reading as dr
import Peak
import ecg_filter
filepath = 'rec-2022-07-12--16-43-31.mat'
df = dr.read(filepath)

# plt.plot(df['t'], df['ecg'])



t = list(df.loc[:,'t'])
ecg = list(df.loc[:,'ecg'])

"""
在这个实验里，我提供的数据是我们当时在在实验室里测量得的数据，实在是因为我们的analog滤波器太完美了
所以得出来数据很干净，同时也没有工频信号50Hz，因为我们的USB-Isolator很完美的屏蔽了它
一般的正常流程都是高通-低通-带阻（或者Notchfilter）
"""
ecg = list(ecg_filter.highpass(ecg,0.3, 2000))
ecg = list(ecg_filter.lowpass(ecg,100, 2000))

# ecg = ecg_filter.bandstop(ecg,49,51, 1000)



# plt.plot(t, ecg)

timeSimple = 1700 
# deadZone = 4 #为了最大值peak采样不重复，设置在maxPeak左/右的4个采样点为“死区”
thresholdFaktor = 0.7
Maximun = 0
threashold = thresholdFaktor * Maximun 

ecgPeak = Peak.Peak(thresholdFaktor = 0.7,timeSimple = 1750)
ecgPeak_find = ecgPeak.findPeak(ecg)
plt.plot(t,ecg)

for i in ecgPeak_find:    
    plt.plot(t[i],ecg[i],"x")
        
    
plt.xlabel('Time [s]')
plt.ylabel('Ecg [Implitude]')
plt.title('peaks of ECG')




















      