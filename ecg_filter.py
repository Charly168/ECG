# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 07:20:48 2022

@author: HP
"""

import numpy as np
import scipy.signal as ss

def highpass(data,fs,samperate):
    
    wn = 2*fs/samperate # 根据奈奎斯定理，且wn的取值范围0~1
    b,a = ss.butter(4, wn, 'hp', analog = False)
    data_filt = ss.filtfilt(b,a,data)
    
    return data_filt

def lowpass(data,fs,samperate):
    
    wn = 2*fs/samperate
    b,a = ss.butter(4, wn, 'low', analog = False)
    data_filt = ss.filtfilt(b,a,data)
    
    return data_filt

def bandstop(data,fs_vor,fs_nach,samperate):
    
    wn_vor =  2*fs_vor/samperate  
    wn_nach =  2*fs_nach/samperate 
    b,a = ss.butter(4, [wn_vor, wn_nach], 'low', analog = False)
    data_filt = ss.filtfilt(b,a,data)
    
    return data_filt


