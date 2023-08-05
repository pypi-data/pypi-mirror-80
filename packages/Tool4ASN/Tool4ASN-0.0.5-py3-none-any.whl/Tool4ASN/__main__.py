#####################################################################
#Programm author: Carmelo Sammarco
#####################################################################

#< Tool4ASN - Software to compute cross correlations with different stacking methodologies. >
#Copyright (C) <2020>  <Carmelo Sammarco - sammarcocarmelo@gmail.com>

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################################################################

#########################
# IMPORT MODULES NEEDED #
#########################
import pkg_resources

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext

import os
import json

def main(args=None):
    
    window = Tk()
    window.title("Tool4ASN")

    sideFrame = Frame(window)
    rightFrame = Frame(window)
    sideFrame.grid(column=0, row=0)
    rightFrame.grid(column=1, row=0)
    
    #window.geometry('500x600')

    def inputfile1():
        inputfile1.file = filedialog.askopenfilename() 

    def inputfile2():
        inputfile2.file = filedialog.askopenfilename()

    def inputdir():
        inputdir.dir = filedialog.askdirectory()


    def DailyCC():

        #############
        # OUTput folder DailyCC
        #############
        currentpath = str(os.getcwd())
        output = os.path.join(currentpath, "Daily-CCs")
        if not os.path.exists(output):
            os.mkdir(output) 



    def StackCC():

        #############
        # OUTput folder StackCC
        #############
        currentpath = str(os.getcwd())
        output = os.path.join(currentpath, "Stack-CCs")
        if not os.path.exists(output):
            os.mkdir(output) 


    def PlotCCs():

        #############
        # OUTput folder PlotCCs
        #############
        currentpath = str(os.getcwd())
        output = os.path.join(currentpath, "Plot-CCs")
        if not os.path.exists(output):
            os.mkdir(output) 

        
        
    
    ###############
    #GUI interface
    ###############
   
    #Username = Label(window, text="Username")
    #Username.grid(column=0, row=0)
    #User = Entry(window, width=13)
    #User.grid(column=0, row=1)
    ##
    #Password = Label(window, text="Password")
    #Password.grid(column=1, row=0)
    #Pwd = Entry(window, width=13, show="*")
    #Pwd.grid(column=1, row=1)


    ##SideFrame
    Side1 = Button(sideFrame, text="Daily-CCs", bg="yellow", command=DailyCC)
    Side1.grid(column=0, row=0)
    ##
    Side2 = Button(sideFrame, text="Stack-CCs", bg="yellow", command=StackCC)
    Side2.grid(column=0, row=1)
    ##
    Side3 = Button(sideFrame, text="Plot-CCs", bg="yellow", command=PlotCCs)
    Side3.grid(column=0, row=2)
    

    ##RIGHTFRAME
    ##
    inputdirect = Button(rightFrame, text="Input-Dir", bg="green", command=inputdir)
    inputdirect.grid(column=1, row=1)
    ##
    
    
    

    #################################################################

    window.mainloop()

