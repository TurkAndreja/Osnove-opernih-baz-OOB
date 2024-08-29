import os
import bottle
from bottle import *
from bottle import TEMPLATE_PATH


# Html datoteke bodo v pod mapi
TEMPLATE_PATH.append('./Presentation/views')

class Route(bottle.Route):
    """
    Nadomestni razred za poti s privzetimi imeni.
    """
    def __init__(self, app, rule, method, callback, name=None, plugins=None, skiplist=None, **config):
        if name is None:
            name = callback.__name__
        def decorator(*largs, **kwargs):
            bottle.request.environ['SCRIPT_NAME'] = os.environ.get('BOTTLE_ROOT', '')
            return callback(*largs, **kwargs)
        super().__init__(app, rule, method, decorator, name, plugins, skiplist, **config)


def template(*largs, **kwargs):
    """
    Izpis predloge s podajanjem funkcije url.
    """
    return bottle.template(*largs, **kwargs, url=bottle.url)

def template_user(*largs, **kwargs):
    """
    Izpis predloge s podajanjem funkcije url in dodanim uporabnikom ter njegovo operno hiso.
    """
    # Dodamo ime uporabnika, ki je prebran iz cookija direktno v vsak html, ki ga uporabimo kot template.
    usr_cookie = request.get_cookie("uporabnik")
    usr_id_operne_hise = request.get_cookie("rola")
    return bottle.template(*largs, **kwargs, uporabnik=usr_cookie, id_operne_hise=usr_id_operne_hise, url=bottle.url)



bottle.Route = Route