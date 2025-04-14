from django.apps import apps
from django.conf import settings
import sys
import datetime
import json
import string
import random
import unicodedata


'''
    Exceptions
'''
def show_exc(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    return ("ERROR ===:> [%s in %s:%d]: %s" % (exc_type, exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_lineno, str(e)))

'''
    Users
'''
def user_in_group(user, group):
    return user.groups.filter(name=group).exists()

'''
    Common
'''
def get_or_none(model, value, field="pk"):
    try:
        return model.objects.get(**{field: value})
    except Exception as e:
        return None

def get_or_none_str(app_name, model_name, value, field="pk"):
    try:
        model = apps.get_model(app_name, model_name)
        obj = model.objects.get(**{field: value})
        return obj
    except Exception as e:
        #logger.error("(get_object): %s" % e)
        return None

def set_obj_field(obj, field, value):
    obj_field = obj._meta.get_field(field)
    if obj_field.get_internal_type() == "ManyToManyField":
        getattr(obj, field).clear()
        for item in value:
            getattr(obj, field).add(get_or_none_str(obj._meta.app_label, obj_field.remote_field.model.__name__, item))
    elif obj_field.get_internal_type() == "ForeignKey":
        setattr(obj, field, get_or_none_str(obj._meta.app_label, obj_field.remote_field.model.__name__, value))
    elif obj_field.get_internal_type() == "FloatField":
        setattr(obj, field, value.replace(",", "."))
    elif obj_field.get_internal_type() == "BooleanField":
        setattr(obj, field, (value == "True"))
    elif obj_field.get_internal_type() == "DateTimeField":
        if "T" in value:
            val = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M')
            setattr(obj, field, val)
        else:
            if "-" in value:
                date = datetime.datetime.strptime(value, '%Y-%m-%d')
                if date >= datetime.datetime(1970,1,1):
                    setattr(obj, field, date)
            if ":" in value:
                val = datetime.datetime.strptime("{} {}".format(getattr(obj, field).strftime('%Y-%m-%d'), value), '%Y-%m-%d %H:%M')
                setattr(obj, field, val)
    else:
        setattr(obj, field, value)
    obj.save()

def get_param(dic, param, default=""):
    return dic[param] if param in dic and dic[param] != "" else default

def get_float(val):
    try:
        return float(val)
    except:
        return 0.0

def get_bool(val):
    try:
        return bool(val)
    except:
        return False

def get_int(val):
    try:
        return int(val)
    except:
        return 0

def translate(request, json_str):
    try:
        lang = request.GET['lang'] if 'lang' in request.GET else request.LANGUAGE_CODE
        json_dict = json.loads(json_str)
        return json_dict[lang.upper()]
    except Exception as e:
        try:
            return json.loads(json_str)['ES']
        except Exception as e:
            return (json_str)

def normalize_str(string):
    try:
        return unicodedata.normalize('NFKD', unicode(string,"utf-8")).encode('ascii', 'ignore')
    except:
        return unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')

def get_items_per_page():
    try:
        return settings.ITEMS_PER_PAGE
    except:
        return 20

def set_session(request, key, default=""):
    request.session[key] = request.GET[key] if key in request.GET else default

def get_session(request, key, default=""):
    return request.session[key] if key in request.session else default

def get_random_str(n):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

