# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 12:25:03 2020

@author: Derek Joslin
"""

import copy
import BoardCom as bc
import numpy as np


class HapticsEngine:

    #haptics engine takes in physics of a board and properly executes graphical commands based on the physics
    #take in the physics of the fluidic chip from matlab and use that to determine timing for actions
    #maybe have it take in an FC library class

    def __init__(self, rows, columns):
        self.__numRows = rows
        self.__numColumns = columns
        self.__currentState = [[False for i in range(0,columns)] for j in range(0,rows)]
        self.__desiredState = [[False for i in range(0,columns)] for j in range(0,rows)]
        self.__comLink = False

    def pull_displaySize(self):
        """ returns a tuple of rows and columns """
        
        rows = self.com.get_num_rows()
        #call the list on different line so 2 doesn't magically appear ahhhhh
        rows = list(rows)
        cols = self.com.get_num_cols()
        cols = list(cols)
        self.__numRows = rows[0]
        self.__numColumns = cols[0]
        #self.__currentState = [[False for i in range(0,self.__numColmuns)] for j in range(0,self.__numRows)]
        #self.__desiredState = [[False for i in range(0,self.__numRows)] for j in range(0,self.__numRows)]



    def return_displaySize(self):
        """ returns the current number of rows and columns """
        return (self.__numRows, self.__numColumns)


    def return_currentState(self):
        """ returns the current state of the chip """
        return self.__currentState
    
    
    def pull_currentState(self):
        """ grabs the state from the arduino and stores it in the currentState """
         
        ARDState = self.com.get_matrix()
        state = []
        for byte in ARDState:
            
            binary = list(bin(byte))
            del binary[0:2]
            binary = [int(i) for i in binary]
            
            while len(binary) != 8:
                binary.insert(0,0)
        
            binary = binary[::-1]
            
            state.append(binary)
        
        del state[-1]
        
        ARDState = []
        ARDState.append([])
        
        rowElem = 14
        rowIndex = 0
        
        for byte in state:
            
            rowElem = rowElem - 8
            
            
            if rowElem > 0:
                ARDState[rowIndex].extend(byte)
            else:
                ARDState[rowIndex].extend(byte[0:rowElem])
                ARDState.append([])
                rowIndex = rowIndex + 1
                rowElem = 14
                
        del ARDState[-1]
            
        
        ARDState = [[bool(i) for i in row] for row in ARDState]
        

        self.__currentState = ARDState

    def return_desiredState(self):
        """ returns the state that the chip wants to be in """
        return self.__desiredState

    def set_desiredState(self, newState):
        """ sets a desired state of the chip """
        for rowIndex,row in enumerate(newState):
            for elemIndex,elem in enumerate(row):
                self.__desiredState[rowIndex][elemIndex] = copy.deepcopy(elem)
                
    def push_desiredState(self):
        """ sends the desired state to the board which then updates the current state """                
        self.com.set_matrix(np.fliplr(np.array(self.__desiredState)).tolist())

    def comLink_on(self, COM, onOff):
        self.com = bc.BoardCom(COM, onOff)
        self.__comLink = True
        #t.sleep(3)
        #self.com.turn_on()
        #self.com.clear_all()

    def comLink_off(self):
        self.__comLink = False
        self.com.close()
        del self.com

    def comLink_check(self):
        return self.__comLink
