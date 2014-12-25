import types
import traceback
from django.db import models
from django.utils import simplejson as json
from django.core.serializers.json import DateTimeAwareJSONEncoder
from decimal import *

def encode(data):
    """
    The main issues with django's default json serializer is that properties that
    had been added to a object dynamically are being ignored (and it also has 
    problems with some models).
    """

    def _any(data):
        ret = None
        if type(data) is list:
            ret = _list(data)
        elif type(data) is dict:
            ret = _dict(data)
        elif isinstance(data, Decimal):
            # json.dumps() cant handle Decimal
            ret = str(data)
        elif isinstance(data, models.query.QuerySet):
            # Actually its the same as a list ...
            ret = _list(data)
        elif isinstance(data, models.Model):
            ret = _model(data)
        else:
            ret = data
        return ret
    
    def _model(data):
        ret = {}
        # If we only have a model, we only want to encode the fields.
        for f in data._meta.fields:
            ret[f.attname] = _any(getattr(data, f.attname))
        return ret
    
    def _list(data):
        ret = []
        for v in data:
            ret.append(_any(v))
        return ret
    
    def _dict(data):
        ret = {}
        for k,v in data.items():
            ret[k] = _any(v)
        return ret
    
    ret = _any(data)
    
    return json.dumps(ret)

def decode(jstr):
    ret = None
    try:
        ret = json.loads(jstr)
    except:
        traceback.print_exc()
    return ret
    
def parse(ptypes,pdefault,params):
    # print(ptypes,params)
    for k,v in ptypes.items():
        if (k not in params) and (k in pdefault):
            params[k] = pdefault[k]
        elif (k in params):
            params[k] = decode(params[k])
        else:
            print('!param',k,v)
            return False
    return True