# -*- coding: utf-8 -*-
"""
Created on Thu May 20 14:10:58 2021

@author: Derek Joslin
"""


from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
#import pyqtgraph as pg

import qrc_resources
import numpy as np

from pyqtconsole.console import PythonConsole
import pyqtconsole.highlighter as hl

#override close event
class guiConsole(PythonConsole):
    def __init__(self, api):
        
        
        
        self.api = api

        super().__init__(formats={
            'keyword':    hl.format('blue', 'bold'),
            'operator':   hl.format('red'),
            'brace':      hl.format('darkGray'),
            'defclass':   hl.format('black', 'bold'),
            'string':     hl.format('magenta'),
            'string2':    hl.format('darkMagenta'),
            'comment':    hl.format('darkGreen', 'italic'),
            'self':       hl.format('black', 'italic'),
            'numbers':    hl.format('brown'),
            'inprompt':   hl.format('darkBlue', 'bold'),
            'outprompt':  hl.format('darkRed', 'bold'),
            })

        #add all the api functions to the gui console
        super().push_local_ns('erase', self.api.erase)
        super().push_local_ns('fill', self.api.fill)
        super().push_local_ns('stroke', self.api.stroke)
        super().push_local_ns('direct', self.api.direct)
        super().push_local_ns('dot', self.api.dot)
        super().push_local_ns('line', self.api.line)
        super().push_local_ns('curve', self.api.curve)
        super().push_local_ns('circle', self.api.circle)
        super().push_local_ns('rect', self.api.rect)
        super().push_local_ns('triangle', self.api.triangle)
        super().push_local_ns('polygon', self.api.polygon)
        super().push_local_ns('latin', self.api.latin)
        super().push_local_ns('braille', self.api.braille)
        super().push_local_ns('clear', self.api.clear)
        super().push_local_ns('Fclear', self.api.Fclear)
        super().push_local_ns('state', self.api.state)
        super().push_local_ns('desired', self.api.desired)
        super().push_local_ns('refresh', self.api.refresh)
        super().push_local_ns('setMat', self.api.setMat)
        super().push_local_ns('connect', self.api.connect)
        super().push_local_ns('disconnect', self.api.disconnect)
        super().push_local_ns('settings', self.api.settings)

    def closeEvent(self,event):
        if self.api.comLink_check():
            self.api.comLink_check()
            event.accept()
        else:
            event.accept()
        
        
        
        
        
# =============================================================================
# #my custom plot widget to display a visual of the board
# class deviceDisplay(pg.PlotWidget):
#     
#     """
#     Will recieve the state data and generate a scatter plot of icons that looks similar to the device display
#     uses pin icons for the scatter plot icons. Automatically creates the board of the right size.
#     """
# 
#     def __init__(self, state):
#         
#         super().__init__()
#         
#         
#         #clear pen
#         self.pen = pg.mkPen(color=(0, 0, 0))
#         
#         self.state = state
#         newMat = np.array(state)
#         dim = newMat.shape
#         self.__columns = dim[1]
#         self.__rows = dim[0]
#         self.__numElem = self.__columns*self.__rows
#         self.createDisplay()
#         
#         
#         
#     def symbolLocater(self, row,column):
#         
#         if self.state[row][column] is False:
#             return 'x'
#         else:
#             return 'o'
#     
#     
#     def coordToIndex(self, row, column):
#         
#         return row*self.__columns + column
#     
#     def createDisplay(self):
#         
#         #clear the widget
#         self.clear()
#         
# =============================================================================
        
        #put the current state into a form that is plottable
        columnIndices = [i for i in range(0,self.__columns)]*self.__rows
        rowIndices = []
        for i in range(0,self.__rows):    
            rowIndices = rowIndices + [i]*self.__columns
            
        self.display = self.plot(columnIndices, rowIndices, pen=self.pen, symbol = 'o')
        self.setXRange(0,self.__columns)
        self.setYRange(0,self.__rows)
        self.invertY()
        
        
    def updateDisplay(self):
        columnIndices = []
        rowIndices = []
        
        
        for rowIndex,row in enumerate(self.state):
            for colIndex,val in enumerate(row):
                if val:
                    #print(colIndex)
                    columnIndices.append(colIndex)
                    rowIndices.append(rowIndex)
                else:
                    pass
        
        #print(columnIndices)
        #print(rowIndices)
        
        self.display.setData(columnIndices,rowIndices)
        
        
# =============================================================================
#         
#         #plot the current state
#         for index,row in enumerate(self.state):
#             rowIndex = rowIndex + [index] * self.__columns
# =============================================================================
            
            
        
    

class displayMat(qw.QTableView):
    def __init__(self, state, dim):
        
        """
        reads in a list of the current FC state. displays that state of 1s and 0s in a matrix of png images
        if val is a one, that element in the table reads in the raised image png. If the element is a zero that element reads in the
        lowered image png.
        """
        
        super().__init__()
        self.state = stateMat(state)
        self.setModel(self.state)
        
        
        delegate = pinDelegate(state, dim, self)
        self.setItemDelegate(delegate)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        
    def resizeEvent(self, event):
        #check for the smaller dimension
        if self.width() < self.height():
            self.resizeContents(self.width() * 0.9,self.width() * 0.9)
        else:
            self.resizeContents(self.height() * 0.9,self.height() * 0.9)
        
        
    def resizeContents(self, dockWidth, dockHeight):
        
        #grab width and height of view
        width = dockWidth
        height = dockHeight
        #resize to appropriate width and height
        elemWidth = width/self.state.getColumns()
        elemHeight = height/self.state.getRows()
        
        dim = (elemWidth, elemHeight)
        delegate = pinDelegate(self.state.state, dim, self)
        self.setItemDelegate(delegate)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
# =============================================================================
#     def data(self, index, role):
#         """
#         Returns the text or formatting for a particular cell, depending on the 
#         role supplied.
#         """
#         if role == qc.Qt.DRole:
#             if self.state[index.row()][index.column()] == 1:
#                 return qc.QVariant(self.filledIcon)
#             else:
#                 return qc.QVariant(self.emptyIcon)
#             
#         #Note that it is first cast as a QIcon before
#         #being cast as a QVariant.
# =============================================================================

# =============================================================================
# 
#     def itemDelegate(self, index):
#         if self.state[index.row()][index.column()] == 1:
#             return qw.QAbstractItemDelegate()
#         else:
#             return qw.QAbstractItemDelegate()
# 
# =============================================================================



class stateMat(qc.QAbstractTableModel):
    def __init__(self, state):
        """
        Qt friendly container to hold the data of a state in a haptics engine
        state will be a list of lists
        """
        super().__init__()

        #store the list and the number of rows and columns
        self.state = state
        newMat = np.array(state)
        dim = newMat.shape
        self.__columns = dim[1]
        self.__rows = dim[0]

    def getRows(self):
        return self.__rows
    
    def getColumns(self):
        return self.__columns

    def rowCount(self, parent):
        return self.__rows

    def columnCount(self, parent):
        return self.__columns

    def data(self, index, role):
        """
        take in a list and parse the data inside the list and
        store inside the model container
        """
        if role == qc.Qt.DisplayRole:    
            return self.state[index.row()][index.column()]



    def setData(self, index, value):
        
        """ directly sets the data in the matrix """
        
        self.state[index.row()][index.column()] = value
        return value
    
    
    def flags(self, index):
        return qc.Qt.ItemIsEnabled|qc.Qt.ItemIsEditable|qc.Qt.ItemIsSelectable
        
# =============================================================================
#     def setData(self, index, value, role):
#         """
#         sets the value of the state equal to the new state of the engine
#         """
#         self.__state = value
# =============================================================================

# =============================================================================
#     def flags():
#
#     def insertRows():
#
#     def removeRows():
#
#     def insertColumns():
#
#     def removeColumns():
# =============================================================================

class pinDelegate(qw.QStyledItemDelegate):
    def __init__(self, state, dim, parent = None):
        super().__init__(parent)
        self.__state = state
        self.__size = qc.QSize(dim[0], dim[1])
        self.filledIcon = qg.QIcon(":filledPin")
        self.emptyIcon = qg.QIcon(":emptyPin")
        
    def get_icon(self, index):
        # get the icon according to the condition:
        # In this case, for example, 
        # the icon will be repeated periodically
        if self.__state[index.row()][index.column()] == 1:
            return self.filledIcon
        else:
            return self.emptyIcon

    def paint(self, painter, option, index):
        icon = self.get_icon(index)
        icon.paint(painter, option.rect, qc.Qt.AlignCenter)


    def sizeHint(self, option, index):
        return self.__size
    
    
class MySwitch(qw.QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setMaximumWidth(150)
        self.setMaximumHeight(150)

    def paintEvent(self, event):
        label = "ON" if self.isChecked() else "OFF"
        bg_color = qc.Qt.green if self.isChecked() else qc.Qt.red

        radius = 13
        width = 34
        center = self.rect().center()

        painter = qg.QPainter(self)
        painter.setRenderHint(qg.QPainter.Antialiasing)
        painter.setBrush(qg.QColor(0,0,0))

        pen = qg.QPen(qc.Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)
        
        painter.drawText(self.rect(), qc.Qt.AlignTop, "{0}".format(self.text()))
        painter.translate(center)
        painter.drawRoundedRect(qc.QRect(-width, -radius, 2*width, 2*radius), radius, radius)
        painter.setBrush(qg.QBrush(bg_color))
        sw_rect = qc.QRect(-radius, -radius, width + radius, 2*radius)
        if not self.isChecked():
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.drawText(sw_rect, qc.Qt.AlignCenter, label)
        
        
        
# =============================================================================
# def comPort(port):
#     return str(port)
# =============================================================================

class ComAction(qw.QAction):
    def __init__(self, port, func, parent):
        super().__init__(port, parent)
        self.triggered.connect(func)
