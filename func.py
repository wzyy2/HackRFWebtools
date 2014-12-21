import traceback
import thread 
import random
import math
from HackRFWebtools import settings
from pyhackrf.core import HackRf 

hackrf = HackRf()
_funclist = {}

modulation = 'AM'
centre_frequency = 100000000
sample_rate =  10000000
rf_gain = 0
if_gain = 16
bb_gain = 20
bb_bandwidth = 0
current_status = 0  #0 stop 1 rx 2 tx

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
    ret['board_name'] = hackrf.name
    ret['version'] = hackrf.version
    ret['serial_nr'] = hackrf.serial_num
    return ret

def set_centre_frequency(params):
    global centre_frequency
    ret = dict()
    print params['centre_frequency']
    centre_frequency = int(params['centre_frequency'])
    hackrf.set_frequency(centre_frequency)
    return ret

def waterfall(params):
    global centre_frequency
    global sample_rate    
    ret = dict()
    ret['centre_frequency'] = centre_frequency
    ret['sample_rate'] = sample_rate
    i = 500.0
    arr = []
    while(i > 0):
        i -= 1
        arr.append((math.sin(i / 8) + 1) * 30 - 50 )  # -1 ~1
        # arr.append(-10)
    ret['data'] = arr   #512  -50~-10
    return ret

def get_control_options(params):
    global centre_frequency
    global rf_gain
    global if_gain
    global bb_gain
    ret = dict()
    ret['centre_frequency'] =centre_frequency
    ret['rf_gain'] = rf_gain
    ret['if_gain'] = if_gain
    ret['bb_gain'] = bb_gain
    ret['demodulator'] = modulation
    ret['bb_bandwidth'] = bb_bandwidth
    ret['squelch_threshold'] = 10
    ret['current_status'] = current_status
    return ret

def demodulator(params):
    global modulation
    ret = dict()
    print params['demodulator']
    modulation = params['demodulator']
    return ret

def set_bb_bandwidth(params):
    global bb_bandwidth
    ret = dict()
    bb_bandwidth = int(params['bb_bandwidth'])
    hackrf.set_baseband_filter_bandwidth(bb_bandwidth)    
    return ret

def set_rf_gain(params):
    global rf_gain
    ret = dict()
    rf_gain = int(params['value'])
    if rf_gain != 0:
        hackrf.enable_amp()
    else:
        hackrf.disable_amp()
    return ret

def set_if_gain(params):
    global if_gain
    ret = dict()
    if_gain = int(params['value'])
    hackrf.set_lna_gain(if_gain)
    return ret

def set_bb_gain(params):
    global bb_gain
    ret = dict()
    bb_gain = int(params['value'])
    hackrf.set_vga_gain(bb_gain)  
    return ret

reg_func(test,{},{})
reg_func(get_board_data,{},{})
reg_func(set_centre_frequency,{},{})    
reg_func(waterfall,{},{})    
reg_func(get_control_options,{},{})    
reg_func(demodulator,{},{})    
reg_func(set_bb_bandwidth,{},{})    
reg_func(set_rf_gain,{},{}) 
reg_func(set_if_gain,{},{}) 
reg_func(set_bb_gain,{},{}) 


def  start_rx(params):
    global current_status
    ret = dict()
    hackrf.set_rx_mode()
    current_status = 1
    return ret

def  start_tx(params):
    global current_status
    ret = dict()
    hackrf.set_tx_mode()
    current_status = 2
    return ret

def  stop(params):
    global current_status
    ret = dict()
    if current_status == 1:
        hackrf.stop_rx_mode()
    elif current_status == 2:
        hackrf.stop_rx_mode()
    current_status = 0
    return ret


reg_func(start_rx,{},{}) 
reg_func(start_tx,{},{}) 
reg_func(stop,{},{}) 