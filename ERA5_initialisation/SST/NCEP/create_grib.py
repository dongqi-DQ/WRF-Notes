#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 15:10:00 2020
script to create empty files to store daily SST

@author: dli84
"""
# create empty files 
from datetime import timedelta, datetime
import numpy as np

def daterange(start_time, end_time):
    for n in range(int ((end_time - start_time).days)):
        yield start_time + timedelta(n)

start_time = datetime(2017, 1, 1)
end_time = datetime(2017, 12, 31)

# hour = timedelta(hours=3)
# fmt = "%Y-%m-%d_%H"
# def daterange(start_time, end_time):
#     now = start_time
#     while now<=end_time:
#        now+=hour
#        yield now.strftime(fmt)


for single_date in daterange(start_time, end_time):
    print('creating file '+str(single_date))
    np.savetxt('sst_files/ncep_daily_2017/'+str(single_date).replace(' 00:00:00','.grb'),np.zeros((2,2)))


