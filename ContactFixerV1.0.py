#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
import tkFileDialog

import re
import ttk
import linecache
import csv
import itertools
import os
import math
import csv
import collections
import numpy as np
from pprint import pprint

#Csv FileName
myFile = ""
myFilePath = ""
csvFilename = ""
csvFile = ""
startDedupeBool = False

#Start Tkinter
root = Tk()
root.title("ContactFixer")

#Define Frames inside window
FileSelectionFrame = Frame(root)
FileSelectionFrame.pack()

statusFrame = Frame(root)
statusFrame.pack()

consoleFrame = Frame(root)
consoleFrame.pack()

#Button Text Variable
startDedupeText = "Iniciar Deduplicador de Contactos"

#Create Functions to Execute

#Usefull Functions
def modified(self, event):
    self.txt.see(END)  # tkinter.END if you use namespaces
    
#Select File to Dedupe
def SelectCsv():
    global csvFile
    global myFilePath
    #Define File Extension
    csvFile = tkFileDialog.askopenfile("rb", filetypes=[("CSV Files","*.csv")])
    #Make String Copy to display
    myFilePath = str(csvFile)
    #Parse Path Information
    myFilePath = myFilePath.split("'", 1)[1].split("'")[0]
    #Print GUI Entry
    pathText.insert(END, myFilePath)
    #Print selected to console
    print "The file: " + myFilePath + " was succesfully added."
    consoleView.insert(END, "La agenda: \n" + myFilePath + "\nfue añadida exitosamente.\n")

def dedupeRoutine():
    try:
        #Loop Counter
        loopCounter = 0
        progressCounter = 0.0

        #Change text to STOP in GUI
        #startDedupeText = "Detener"
        
        #Define input file parameters
        data = []
        
        def unique():
            rows = list(csv.reader(csvFile, delimiter=',', quotechar='"'))
            
            result = collections.OrderedDict()
            for r in rows:
                key = (r[0],r[2] ,r[15]
                       )  ## The pair (r[1]:r[87]) must be unique
                if key not in result:
                    result[key] = r
                
            return result.values()
        
        data.append(unique())
        
        print len(data[0])
        consoleView.insert(END, "------------------------------------------------------\n")
        consoleView.insert(END, "Buscando Registros Unicos.\n")
        consoleView.insert(END, "------------------------------------------------------\n")
        consoleView.insert(END, "Registros Unicos Encontrados: " + str(len(data[0]) - 1) + "\n")
        consoleView.insert(END, "------------------------------------------------------\n")
        combinationCalculation = len(data[0])
        
        outputFile = os.path.dirname(myFilePath)
        print outputFile
        outputFile = outputFile + "/DedupedCSVFile.csv"
        print outputFile
        
        writer = csv.writer(open(outputFile, "wb"))
            
        rowNumber = 0
            
        for row in data:
            writer.writerows(row)
            for item in row:
                rowNumber = rowNumber + 1
                for i in item:
                    consoleView.insert(END, "Comparando Registro " + str(rowNumber) + " de " + str(len(data[0])) + " : " + str(i) + "\n")
                    
                    #Update Progress Bar
                    loopCounter = loopCounter + 1
                    #print loopCounter
                    
                    progressCounter = (float(rowNumber)/float(combinationCalculation)) * 100.0
                    print progressCounter
                    
                    progressbar["value"] = progressCounter
                
                consoleView.see("end")
                    
                root.update_idletasks()
                root.update()
                    
        consoleView.insert(END, "------------------------------------------------------\n")
        consoleView.insert(END, "Cerrando archivo CSV: OK! \n")
        consoleView.insert(END, "------------------------------------------------------\n")            
        consoleView.insert(END, "CSV Listo para importar\n")
        consoleView.insert(END, "------------------------------------------------------\n")         
        consoleView.insert(END, "Se encuentra en: " + outputFile + "\n")
        consoleView.insert(END, "------------------------------------------------------\n")
        consoleView.see("end")
        
                    
        #Close Deduped CSV File    
        csvFile.close()
        
    except IOError:
        
        print "No file was selected, please select a file."
        consoleView.insert(END, """No se eligio ninguna agenda, por favor seleccione una agenda con extension ".csv" \n""" )
        
#Create Buttons to Interact in GUI
#Select input file
fileSelectionSubFrame = LabelFrame(FileSelectionFrame, text="Selección de Agenda", padx = 5, pady= 5) 
selectCsvButton = Button(fileSelectionSubFrame, text="Selecciona el archivo CSV", command = SelectCsv) 
pathText = Entry(fileSelectionSubFrame, width = 106)
#Progress Bar
#LabelFrame
progressLabel = LabelFrame(statusFrame, text="Progreso", padx = 5, pady= 5)
#Label
progressLabelText = Label(progressLabel, text="Status:")
#Progress Bar
progressbar = ttk.Progressbar(progressLabel, orient=HORIZONTAL, length=557, mode='determinate')
progressbar["maximum"] = 100
#progressbar.start()
progressbar["value"] = 0
#Dedupe Button
startDedupeButton = Button(progressLabel, text= startDedupeText, command = dedupeRoutine )
#Dedupe Stop Button
#Console View
consoleLabel = LabelFrame(consoleFrame, text="Consola", padx = 5, pady= 5)
scrollConsole = Scrollbar(consoleLabel)
consoleView = Text(consoleLabel, width = 96, height = 10, yscrollcommand = scrollConsole.set)
#Greeting 
consoleView.insert(END, "¡Bienvenido a ContactFixer V1.0!\n")

#Pack windows
#File Selection
fileSelectionSubFrame.pack()
selectCsvButton.pack(side=RIGHT)
pathText.pack(side=LEFT)
#Progress And Start Button
progressLabel.pack()
progressLabelText.pack(side=LEFT)
progressbar.pack(side=LEFT)
startDedupeButton.pack(side=RIGHT)
#Console
consoleLabel.pack()
scrollConsole.pack(side=RIGHT, fill = Y)
scrollConsole.config( command = consoleView.yview )
consoleView.pack(side=LEFT, fill=BOTH)

root.mainloop()
