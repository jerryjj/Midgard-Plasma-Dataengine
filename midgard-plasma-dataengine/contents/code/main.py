from PyQt4.QtCore import *
from PyKDE4.kdecore import *
from PyKDE4 import plasmascript

import _midgard as midgard

mgd_conn = midgard.connection()
mgd_conf = midgard.config()
_available_schemas = []

class PyMidgardEngine(plasmascript.DataEngine):
    def __init__(self,parent,args=None):
        plasmascript.DataEngine.__init__(self,parent)
        init_midgard()

    def init(self):
        self.setMinimumPollingInterval(333)

    def sources(self):
        sources = get_available_schemas()
        return sources

    def sourceRequestEvent(self, name):
        return self.updateSourceEvent(name)

    def updateSourceEvent(self, source):
        self.setData(source, "Name", QVariant("Default Schema"))

        return True

def CreateDataEngine(parent):
    return PyMidgardEngine(parent)


def init_midgard():
    global mgd_conn, mgd_conf

    setattr(mgd_conf, "database", "plasma-dataengine")

    return mgd_conn.open_config(mgd_conf)

def get_available_schemas(force_reload=False):
    global _available_schemas

    if len(_available_schemas) > 0 and not force_reload:
        return _available_schemas

    for name in dir(midgard.mgdschema):
        if not name in ["__doc__", "__name__", "__package__", "midgard_object", "metadata"]:
            _available_schemas.append(name)

    return _available_schemas
