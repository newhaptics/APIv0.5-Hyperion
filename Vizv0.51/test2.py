# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 15:09:05 2021

@author: Derek Joslin
"""

import NHAPI as nh


engine = nh.NHAPI()

engine.connect("COM10", 1)

engine.size()
    
engine.line((5,5), (10,10))

engine.desired()

engine.refresh()

engine.state()

engine.disconnect()
