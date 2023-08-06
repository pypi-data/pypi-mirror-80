# -*- coding: utf-8 -*-

"""
    Agstream Module
    ---------------
    Necessary stuff to connect and to use data from the Agriscope server
"""
from __future__ import absolute_import

__version__ = "0.0.13"


from .session import AgspSession
from .devices import Agribase, Sensor
