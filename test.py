from pyhackrf import pylibhackrf 
import sys,time,threading
from func import *
import numpy as np
import pylab as pl
from ctypes import *
# time1= time.time()
# cnt = 0
# def callback_fun(hackrf_transfer):
#     global time1,cnt
#     time2= time.time()
#     if time2 - time1 >= 1:
#         time1 = time.time()
#         print cnt
#         cnt = 0
#     cnt += hackrf_transfer.contents.valid_length
#     return 0
time1= time.time()
have_recv = False
lock = threading.Lock()
all_cnt = 0
buf = list()
buf2 = list()
cnt = 0

def callback_fun(hackrf_transfer):
    global have_recv,buf,buf2,cnt,time1,all_cnt 
    lock.acquire() 
    length = hackrf_transfer.contents.valid_length
    array_type = (c_ubyte*length)
    values = cast(hackrf_transfer.contents.buffer, POINTER(array_type)).contents
    all_cnt += length
    if time.time() - time1 > 1:
        time1 = time.time()
        print all_cnt
        all_cnt = 0
    buf2 = values
    have_recv = True
    lock.release()          
    return 0

if hackrf.is_open == False:
    hackrf.setup()
    hackrf.set_freq(hackrf_settings.centre_frequency)
    hackrf.set_sample_rate(hackrf_settings.sample_rate)
    hackrf.set_amp_enable(False)
    hackrf.set_lna_gain(hackrf_settings.if_gain)
    hackrf.set_vga_gain(hackrf_settings.bb_gain)    
    hackrf.set_baseband_filter_bandwidth(hackrf_settings.bb_bandwidth)  

hackrf.start_rx_mode(callback_fun)



while True:
    lock.acquire()  
    if have_recv == True:
        iq = hackrf.packed_bytes_to_iq(buf2)
        lock.release()  
        fy = np.fft.fft(iq) / iq.size
        print fy
        pl.figure()
        pl.plot(fy)
        pl.xlabel("frequency bin")
        pl.ylabel("power(dB)")
        pl.title("FFT result of triangle wave")
        pl.show()

        have_recv = False    
    else:
        lock.release()  


# print hackrf.hackrf_open()