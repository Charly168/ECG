# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 09:45:31 2022

@author: HP
"""

import h5py
import pandas as pd

def read(filepath):
    
    with h5py.File(filepath) as f:
        data_all = list(f['data'])
        ecg_t,ecg = data_all[0],data_all[1]
        df = pd.DataFrame(
            {
                't': ecg_t,
                'ecg': ecg
                }
            )
        
        return df