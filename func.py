import traceback
from HackRFWebtools import settings
#from libhackrf import *

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

def test(params):
    ret=dict()
    ret['count']=100
    ret['retstr']="hello word"
    return ret
    
def get_board_data(params):
    ret=dict()
    ret['board_id']=100
    ret['version']="hello word"
    ret['serial_nr']="hello word"    
    return ret

def set_centre_frequency(params):
    ret=dict()
    print params['centre_frequency']
    return ret

reg_func(test,{},{})
reg_func(get_board_data,{},{})
reg_func(set_centre_frequency,{},{})    

