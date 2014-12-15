from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson
from django.http import HttpResponseRedirect
from django.shortcuts import render
import threading
import traceback
from func import *
from common import js_handler
import os.path
import datetime 
  
htmldir = os.path.join(os.path.dirname(__file__), 'html').replace('\\','/')
def index(request):
    t = get_template('wui4hf/ui.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))


    ## js api handler

rk = threading.Lock()
wk = threading.Lock()
rc = 0

def readInc():
    global rc,rk,wk
    rk.acquire()
    rc = rc+1
    if rc==1:
        wk.acquire()
    rk.release()

def readDec():
    global rc,rk,wk
    rk.acquire()
    rc = rc-1
    if rc==0:
        wk.release()
    rk.release()

def _do(request,transfer_handler):
    params = dict()
    ret = None
    try:
        for k,v in request.GET.items():
            params[k] = v
        sm = params.pop('method')
        m = get_func(sm)
        assert(transfer_handler.parse(m[1],m[2],params))
        readInc()
        try:
            ret = call_func(sm,params)
        except:
            traceback.print_exc()
        readDec()
    except:
        traceback.print_exc()
    try:
        ret = transfer_handler.encode(ret)
    except:
        ret = transfer_handler.encode(None)
        traceback.print_exc()
    return ret
    
def do(request):
    jsret = _do(request,js_handler)
    return HttpResponse(jsret)
    