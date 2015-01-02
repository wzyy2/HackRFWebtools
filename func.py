import threading,signal ,traceback
import random,ctypes,math,time,copy,Queue
import numpy

from dsp import common
from GlobalData import *
from common import Rx,Tx

_funclist = {}

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
def hackrf_reconf():
        hackrf.set_freq(hackrf_settings.centre_frequency)
        hackrf.set_sample_rate(hackrf_settings.sample_rate)
        hackrf.set_amp_enable(cFalse)
        hackrf.set_lna_gain(hackrf_settings.if_gain)
        hackrf.set_vga_gain(hackrf_settings.bb_gain)    
        hackrf.set_baseband_filter_bandwidth(hackrf_settings.bb_bandwidth)  
        hackrf_settings.name =  hackrf.NAME_LIST[hackrf.board_id_read()]
        hackrf_settings.version = hackrf.version_string_read()    

def test(params):
    ret = dict()
    ret['count'] = 100
    ret['retstr'] = "hello word"
    return ret
 
def reset(params):
    ret = dict()
    try:
        stop(None)
        hackrf_settings.current_status = 0   
        hackrf.close()
        hackrf.open()
        hackrf_reconf()
        ret['ret'] = 'ok'
    except:
        ret['ret'] = 'fail'   
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
    ret['data'] = Rx.get_spectrum()
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
    ret['fft_rate'] = hackrf_settings.fft_rate
    ret['fft_size'] = hackrf_settings.fft_size
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


def set_fft_size(params):
    ret = dict()
    hackrf_settings.fft_size = int(params['value'])
    return ret

def set_fft_rate(params):
    ret = dict()
    hackrf_settings.fft_rate = int(params['value'])
    return ret

def  start_rx(params):
    ret = dict()
    if hackrf_settings.current_status == 1:
        return 
    hackrf_settings.rx_thread =  Rx.RxThread()
    hackrf_settings.rx_thread.setDaemon(True)
    hackrf_settings.rx_thread.start()
    if hackrf_settings.current_status == 0:
        hackrf.start_rx_mode(Rx.rx_callback_fun)
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
reg_func(set_fft_size,{},{}) 
reg_func(set_fft_rate,{},{}) 
reg_func(start_rx,{},{}) 
reg_func(start_tx,{},{}) 
reg_func(stop,{},{}) 