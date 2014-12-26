import traceback
import threading 
import random,ctypes
import math,time
from HackRFWebtools import settings
from pyhackrf import pylibhackrf 
from threading import Lock
import numpy as np
import pylab as pl

#default setting
class HackrfSettings():
    def __init__(self):
        self.modulation = 'NO'
        self.centre_frequency = 100 * 1000 * 1000
        self.sample_rate = 8 * 1000 * 1000
        self.rf_gain = 0
        self.if_gain = 16
        self.bb_gain = 20
        self.bb_bandwidth = 12* 1000 * 1000
        self.current_status = 0  #0 stop 1 rx 2 tx
        self.name = None
        self.version = None
        self.serial_num = None
        self.rx_thread = None

hackrf = pylibhackrf.HackRf()
hackrf_settings = HackrfSettings()
_funclist = {}
spectrum = []
spectrum_lock = Lock()

def reg_func(func,param_types,param_defaults):
    ret = False
    try:
        _funclist[func.__name__]=(func,param_types,param_defaults)
        ret = True
    except:
        traceback.print_exc()
    return ret

def get_func(name):
    if name in _funclist:
        return _funclist[name]
    else:
        return None
        
def call_func(name,params):
    ret = None
    try:
        ret = _funclist[name][0](params)
    except:
        traceback.print_exc()
    return ret

### api - program
# params:page as int ,count as int
# ret:total_page as int,total as int,programs as array

def test(params):
    ret = dict()
    ret['count'] = 100
    ret['retstr'] = "hello word"
    return ret
    
def get_board_data(params):
    ret = dict()
    ret['board_name'] = hackrf_settings.name
    ret['version'] = hackrf_settings.version
    ret['serial_nr'] = hackrf_settings.serial_num
    return ret

def set_centre_frequency(params):
    ret = dict()
    hackrf_settings.centre_frequency = int(params['centre_frequency'])
    hackrf.set_freq(hackrf_settings.centre_frequency)
    return ret

def waterfall(params):
    ret = dict()
    ret['centre_frequency'] = hackrf_settings.centre_frequency
    ret['sample_rate'] = hackrf_settings.sample_rate
    arr = list()
    spectrum_lock.acquire() 
    maxval = 0
    for i in range(len(spectrum)):
        if i % 100 == 1:
            if maxval < abs(spectrum[i]):
                maxval = abs(spectrum[i]);
            arr.append(abs(spectrum[i]))  # -1 ~1
        # arr.append(-10)
    spectrum_lock.release()
    ret['data'] = arr   #512  -50~-10
    print maxval
    return ret

def get_control_options(params):
    ret = dict()
    ret['centre_frequency'] =hackrf_settings.centre_frequency
    ret['rf_gain'] = hackrf_settings.rf_gain
    ret['if_gain'] = hackrf_settings.if_gain
    ret['bb_gain'] = hackrf_settings.bb_gain
    ret['demodulator'] = hackrf_settings.modulation
    ret['bb_bandwidth'] = hackrf_settings.bb_bandwidth
    ret['squelch_threshold'] = 10
    ret['current_status'] = hackrf_settings.current_status
    return ret

def demodulator(params):
    ret = dict()
    print params['demodulator']
    hackrf_settings.modulation = params['demodulator']
    return ret

def set_bb_bandwidth(params):
    ret = dict()
    hackrf_settings.bb_bandwidth = int(params['bb_bandwidth'])
    hackrf.set_baseband_filter_bandwidth(hackrf_settings.bb_bandwidth)    
    return ret

def set_rf_gain(params):
    ret = dict()
    hackrf_settings.rf_gain = int(params['value'])
    if hackrf_settings.rf_gain != 0:
        hackrf.set_amp_enable(True)
    else:
        hackrf.set_amp_enable(False)
    return ret

def set_if_gain(params):
    ret = dict()
    hackrf_settings.if_gain = int(params['value'])
    hackrf.set_lna_gain(hackrf_settings.if_gain)
    return ret

def set_bb_gain(params):
    ret = dict()
    hackrf_settings.bb_gain = int(params['value'])
    hackrf.set_vga_gain(hackrf_settings.bb_gain)  
    return ret

reg_func(test,{},{})
reg_func(get_board_data,{},{})
reg_func(set_centre_frequency,{},{})    
reg_func(get_control_options,{},{})    
reg_func(demodulator,{},{})    
reg_func(set_bb_bandwidth,{},{})    
reg_func(set_rf_gain,{},{}) 
reg_func(set_if_gain,{},{}) 
reg_func(set_bb_gain,{},{}) 
reg_func(waterfall,{},{})    

transfer_lock = Lock()
time1= time.time()
have_recv = False
all_cnt = 0
transfer_lbuf = []

class RxThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
    def run(self):
        global have_recv,transfer_lbuf,spectrum 
        #note: we don't set self.running to False anywhere...
        while self.running:
            transfer_lock.acquire()  
            if have_recv == True:
                iq = hackrf.packed_bytes_to_iq(transfer_lbuf)
                transfer_lock.release()  
                spectrum_lock.acquire() 
                spectrum = np.fft.fft(iq) / iq.size
                spectrum_lock.release()  
                have_recv = False    
            else:
                transfer_lock.release()  



def rx_callback_fun(hackrf_transfer):
    global have_recv,all_cnt,time1,transfer_lbuf 
    transfer_lock.acquire() 
    length = hackrf_transfer.contents.valid_length
    array_type = (ctypes.c_ubyte*length)
    values = ctypes.cast(hackrf_transfer.contents.buffer, ctypes.POINTER(array_type)).contents
    all_cnt += length
    if time.time() - time1 > 1:
        time1 = time.time()
        print all_cnt
        all_cnt = 0
    transfer_lbuf = values
    have_recv = True
    transfer_lock.release()          
    return 0

def  start_rx(params):
    ret = dict()
    if hackrf_settings.current_status == 1:
        return 
    hackrf_settings.rx_thread =  RxThread()
    hackrf_settings.rx_thread.start()
    if hackrf_settings.current_status == 0:
        hackrf.start_rx_mode(rx_callback_fun)
    hackrf_settings.current_status = 1
    return ret

def  start_tx(params):
    ret = dict()
    if hackrf_settings.current_status == 2:
        return 
    if hackrf_settings.current_status == 0:
        hackrf.start_tx_mode(rx_callback_fun)
    hackrf_settings.current_status = 2
    return ret

def  stop(params):
    ret = dict()
    if hackrf_settings.current_status == 1:
        hackrf_settings.rx_thread.running = False
        hackrf_settings.rx_thread .join()
        hackrf.stop_rx_mode()
        hackrf.reset()
    elif hackrf_settings.current_status == 2:
        hackrf.stop_tx_mode()
    hackrf_settings.current_status = 0
    return ret


reg_func(start_rx,{},{}) 
reg_func(start_tx,{},{}) 
reg_func(stop,{},{}) 