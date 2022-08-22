# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 07:20:48 2022

@author: HP
"""
import scipy.signal as ss

def highpass(data,fs,samplerate):
    """
    samplerate是采样频率，根据奈奎斯定理，最大的频率则为0.5*samplerate Hz，wn的取值范围是0~1
    fs是截止频率，那么wn的计算方式则是fs/(0.5*samplerate)
    """
    wn = 2*fs/samplerate 
    b,a = ss.butter(4, wn, 'hp', analog = False)
    data_filt = ss.filtfilt(b,a,data)
    
    return data_filt

def lowpass(data,fs,samplerate):
    
    wn = 2*fs/samplerate
    b,a = ss.butter(4, wn, 'low', analog = False)
    data_filt = ss.filtfilt(b,a,data)
    
    return data_filt

def bandstop(data,fs_vor,fs_nach,samplerate):
    
    wn_vor =  2*fs_vor/samplerate  
    wn_nach =  2*fs_nach/samplerate 
    b,a = ss.butter(4, [wn_vor, wn_nach], 'low', analog = False)
    data_filt = ss.filtfilt(b,a,data)
    
    return data_filt


