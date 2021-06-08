# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 11:39:32 2020

@author: Derek Joslin
"""

import serial


class BoardCom:
    
     #the Board Com object contains a serial port connection object and commands to communicate with hardware


    def __init__(self, port, *args):
        #115200 for the embedded board
        self.port = serial.Serial(port, 57600, timeout=5)
        
        # self.port = port #serial.Serial(port, 57600, timeout=1)
        
        if len(args) > 0:
            if args[0] == 1:
                self.__echo = 1
                
            else:
                self.__echo = 0
        else:
            self.__echo = 0
        self.__recieveBuffer = self.port.read_until(b'\xFF')
        
        if self.__echo:
            print(self.__recieveBuffer)
        else:
            pass

    #sets the echo of the com port onOff (0=Off, 1=On)
    def echo(self, onOff):
        if onOff:
            self.__echo = 1
        else:
            self.__echo = 0
    
    #opens the serial port
    def open(self):
        self.port.open()
        self.__print_rx()

    #closes the serial port
    def close(self):
        self.port.close()

    #if echo is on prints the recieve data
    def __print_rx(self):
        read = self.__read_rx()
        if self.__echo:
            print(read)
        else:
            pass
        
    #reads in data on the serial line
    def __read_rx(self):
        # self.port.flush()
        self.__recieveBuffer = self.port.read(1)
        return self.__recieveBuffer #.decode('utf-8')
    
    
    """ New functionality for the arduino """
    
    
    #sets a row on the chip
    def set_row(self, rowIndex, rowData):
        #create list with required parameters
        output = []
        
        #select the set Row Function (1)
        output.append(1)
        
        #add the row index to the list
        output.append(rowIndex)
        
        #take list of rowData and add it to the list, but concatenated with 8 elements as a byte
        row = list(map(int, rowData))
        fill = 0
        N = 8
        tempList = row + [fill] * N
        subList = [tempList[n:n+N] for n in range(0, len(row), N)]
        
        for lst in subList:
            s = '0b' + ''.join(map(str, lst))
            output.append(int(s, base=2))
        
        #send as bytearray with each parameter as a byte
        self.port.write(bytearray(output))
        
        #print the recieved bit if echo is on
        self.__print_rx()
        
        
    def clear_all(self):
        #create list of bytes to send
        output = []
        
        #select the second function
        output.append(2)
        
        #send the byte array
        self.port.write(bytearray(output))
        
        
        #print the recieved bit
        self.__print_rx()
        
        
        
        
            
    def is_idle(self):
        #create list to be the output
        output = []
        
        #select the fourth function
        output.append(4)
        
        #send the byte
        self.port.write(bytearray(output))
        
        #read whether the device is idle
        self.__print_rx()
        
        
    def turn_off(self):
        #create the list for output
        output = []
        
        #select the fifth function
        output.append(5)
        
        #send the byte
        self.port.write(bytearray(output))
        
        #read the output on the serial port
        self.__print_rx()
        
        
    def turn_on(self):
        #create a list for the output
        output = []
        
        #select the sixth function
        output.append(6)
        
        #send the command
        self.port.write(bytearray(output))
        
        
        
        #read the output on the serial port
        self.__print_rx()
        
    
        
        
        
    def set_matrix(self, mat):
        #create a list for the output
        output = []
        
        #select the seventh function
        output.append(7)
        
        #take list of rows and create byte arrays out of each row
        fill = 0
        N = 8
        for rowData in mat:
            row = list(map(int, rowData))[::-1]
            tempList = row + [fill] * N
            subList = [tempList[n:n+N] for n in range(0, len(row), N)]
            for lst in subList:
                s = '0b' + ''.join(map(str, lst))
                output.append(int(s, base=2))
    
        #send the command
        self.port.write(bytearray(output))
        
        #read the output on the serial port
        self.__print_rx()
        
        
        
    def set_dot(self, rowIndex, colIndex, data):
        #create output list
        output = []
        
        #select the eighth function
        output.append(8)
        
        #add the row index column index and state
        output.append(rowIndex)
        output.append(colIndex)
        output.append(data)
        
        #send the command
        self.port.write(bytearray(output))
        
        #read the output on the serial port
        self.__print_rx()
        
        
    def set_all(self, data):
        #create output list
        output = []
        
        #select function
        output.append(9)
        
        #add the desired data for the state to be set to
        output.append(data)
        
        #send the command
        self.port.write(bytearray(output))
        
        #read the output on the serial port
        self.__print_rx()
    
    def get_num_rows(self):
        #create output list
        output = []
        
        #select function
        output.append(10)
        
        #send the command
        self.port.write(bytearray(output))
        
        self.__recieveBuffer = self.port.read_until(b'\x0A')

        #read the output on the serial port
        if self.__echo:
            print(self.__recieveBuffer)
        else:
            pass
        #self.__print_rx() # Alex: read final byte reporting function number

        #print(self.__recieveBuffer)
        #return the recieve buffer
        return self.__recieveBuffer
        
    
    def get_num_cols(self):
        #create output list
        output = []
        
        #select function
        output.append(11)
        
        #send the command
        self.port.write(bytearray(output))
        
        self.__recieveBuffer = self.port.read_until(b'\x0B')

        #read the output on the serial port
        if self.__echo:
            print(self.__recieveBuffer)
        else:
            pass
        #self.__print_rx() # Alex: read final byte reporting function number

        #print(self.__recieveBuffer)
        #return the recieve buffer
        return self.__recieveBuffer
        
        
        
        
    def get_matrix(self):
        #create list of bytes to be sent
        output = []
        
        #select the twelve function
        output.append(3)
        
        #send the command
        self.port.write(bytearray(output))
        
        #read the current matrix state
        self.port.flush()
        self.__recieveBuffer = self.port.read_until(b'\x0C')
        
        
        if self.__echo:
            print(self.__recieveBuffer)
        else:
            pass
        
        
        #print(self.__recieveBuffer)
        #return the recieve buffer
        return self.__recieveBuffer
        


# =============================================================================
# startMatrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1,],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1,],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0,],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0,],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0,],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0,],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0,],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0,],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0,],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
#                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
#                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
#                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
#                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
#                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
#                [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
#                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
#                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
#                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]]
# 
# com = BoardCom("COM5")
# com.set_matrix(startMatrix)
# 
# =============================================================================
