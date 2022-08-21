# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 07:41:45 2022

@author: HP
"""
import matplotlib.pyplot as plt
import data_reading as dr
import Peak

filepath = 'rec-2022-07-12--16-43-31.mat'
df = dr.read(filepath)

# plt.plot(df['t'], df['ecg'])



t = list(df.loc[:,'t'])
ecg = list(df.loc[:,'ecg'])

# plt.plot(t, ecg)

timeSimple = 850 # 最大心率为250bmp，对应频率为4hz，大概是0.2s，采样频率为1000，因此相应采样点数为200
deadZone = 4 #为了最大值peak采样不重复，设置在maxPeak左/右的4个采样点为“死区”
thresholdFaktor = 0.7
Maximun = 0
threashold = thresholdFaktor * Maximun 

ecgPeak = Peak.Peak(thresholdFaktor = 0.7,deadZone = 4,timeSimple = 850)
ecgPeak_find = ecgPeak.findPeak(ecg)
plt.plot(t,ecg)

for i in ecgPeak_find:
    plt.plot(t[i],ecg[i],"x")




















      