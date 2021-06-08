# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 10:43:20 2020

@author: Derek Joslin
"""

import HapticsEngine as he
import GraphicsEngine as ge



class NHAPI(he.HapticsEngine):
    
    
    def __init__(self):
        
        
        #create the backend haptics engine
        super(NHAPI, self).__init__(15,14)
        self.graphics = ge.GraphicsEngine(self.return_desiredState())

        
        self.full = 0
        self.width = 1
        self.autoRefresh = 0


    def display_matrix(self, matrix, num):
        print("num: {}".format(num))
        print('---------------------------\n')
        print('\n'.join([' '.join(['{:4}'.format(item) for item in row])
                         for row in matrix]))
        print('---------------------------\n')


    def erase(self, onOff):
        if onOff == "on":
            self.graphics.set_output(False)
            print("erase on")
        else:
            self.graphics.set_output(True)
            print("erase off")

    def fill(self, onOff):
            if onOff == "on":
                self.full = 1
                print("fill on")
            else:
                self.full = 0
                print("fill off")
    
    def direct(self, onOff):
        if onOff == "on":
            self.autoRefresh = 1
            print("direct on")
        else:
            self.autoRefresh = 0
            print("direct off")
    
    def stroke(self, size):
        print("stroke is {0}".format(size))
        self.width = size
    
    def settings(self):
        print("fill setting {0}".format(self.full))
        print("stroke setting {0}".format(self.width))
        print("direct setting {0}".format(self.autoRefresh))
        print("connection setting {0}".format(self.comLink_check()))
    
    
    def dot(self, coord):
        self.graphics.select_element(coord)
        print("desired state \n")
        self.display_matrix(self.return_desiredState(), 0)
        if self.autoRefresh:
            self.refresh()
    
    def line(self, start, end):
        self.graphics.make_line(start, end, self.width)
        print("desired state \n")
        self.display_matrix(self.return_desiredState(), 0)
        if self.autoRefresh:
            self.refresh()

    def curve(self, start, control1, control2, end):
        self.graphics.make_bezierCurve(start, control1, control2, end, self.width)
        print("desired state \n")
        self.display_matrix(self.return_desiredState(), 0)
        if self.autoRefresh:
            self.refresh()
    
    def circle(self, center, radius):
        self.graphics.make_circle(center, radius, self.width, self.full)
        print("desired state \n")
        self.display_matrix(self.return_desiredState(), 0)
        if self.autoRefresh:
            self.refresh()
    
    def rect(self, corner1, corner2):
        self.graphics.make_rectangle(corner1, corner2, self.width, self.full)
        print("desired state \n")
        self.display_matrix(self.return_desiredState(), 0)
        if self.autoRefresh:
            self.refresh()
    
    def triangle(self, point1, point2, point3):
        self.graphics.make_polygon(point1, [point2, point3], self.width, self.full)
        print("desired state \n")
        self.display_matrix(self.return_desiredState(), 0)
        if self.autoRefresh:
            self.refresh()
    
    def polygon(self, points):
        self.graphics.make_polygon(points[0], points[1:-1], self.width, self.full)
        print("desired state \n")
        self.display_matrix(self.return_desiredState(), 0)
        if self.autoRefresh:
            self.refresh()
    
    def braille(self, point, text):
        self.graphics.write_braille(point, text)
        print("desired state \n")
        self.display_matrix(self.return_desiredState(), 0)
        if self.autoRefresh:
            self.refresh()
    
    def latin(self, point, text, font, size):
        self.graphics.write_latin(point, text, font, size)
        print("desired state \n")
        self.display_matrix(self.return_desiredState(), 0)
        if self.autoRefresh:
            self.refresh()
    
    def clear(self):
        self.graphics.clear()
        print("desired state \n")
        self.display_matrix(self.return_desiredState(), 0)
        if self.autoRefresh:
            self.refresh()
        
    ### added at alex request
    def Fclear(self):
        if self.comLink_check():
            self.com.clear_all()
        self.clear()
    ###
    
    #gets size of the chip and displays
    def size(self):
        self.pull_displaySize()
        print("The size of the matrix is {}".format(self.return_displaySize()))
        
    #gets the current state and displays it 
    def state(self):
        print("current state \n")
        self.pull_currentState()
        self.display_matrix(self.return_currentState(), 0)
        return self.return_currentState
    
    #gets the desired state and displays it 
    def desired(self):
        print("desired state \n")
        self.display_matrix(self.return_desiredState(), 0)
        return self.return_desiredState()
    
    def setMat(self, mat):
        self.set_desiredState(mat)
        if self.autoRefresh:
            self.refresh()
    
    def refresh(self):
        self.push_desiredState()
        print("refreshed")
    
    def connect(self, COM, *args):
        if len(args) > 0:
            if args[0] == 1:
                self.comLink_on(COM, 1)
            print("comLink check is {}".format(self.comLink_check()))
        else:
            self.comLink_on(COM, 0)
    
    def disconnect(self):
        self.comLink_off()
        print("comLink check is {}".format(self.comLink_check()))
