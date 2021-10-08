# -*- coding: utf-8 -*-
"""
Interfaz gráfica de usuario
"""

import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QDialog, QHBoxLayout,QComboBox, 
                             QLabel, QPushButton, QGridLayout)
from PyQt5.QtGui import (QPalette, QFont, QColor)

import sounddevice as sd
import soundfile as sf
import pickle

from recording import recording
from identifier import identifier
from database import database_function


try:
    with open('database.pickle', 'rb') as f:
        database = pickle.load(f)
except:
    database_function()
    with open('database.pickle', 'rb') as f:
        database = pickle.load(f)

class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, windowTitle='UNTREF - DSP - Trabajo práctico Nº3')

        mainLayout = QGridLayout()

        app.setStyle("Fusion")        
        qp = QPalette()
        qp.setColor(QPalette.ButtonText, Qt.black)
        qp.setColor(QPalette.Window, QColor(200,200,200))
        qp.setColor(QPalette.WindowText, Qt.black)  
        qp.setColor(QPalette.Button, QColor(76,0,153))
        qp.setColor(QPalette.Highlight, QColor(76,0,153))
        qp.setColor(QPalette.Base, QColor(42,42,42))
        app.setPalette(qp)

        
        info1_label = QLabel("\n"+'   IDENTIFICADOR DE SEÑALES' +"\n"+ '                MUSICALES '+"\n" )
        info1_label.setFont(QFont('Helvetica', 12, QFont.Bold))
        self.setLayout(mainLayout)
        
        input_label = QLabel('    Input')
        input_label.setFont(QFont('Helvetica', 11))
        self.setLayout(mainLayout)
        
        output_label = QLabel('    Output')
        output_label.setFont(QFont('Helvetica', 11))
        self.setLayout(mainLayout)
          
        grabar_pb = QPushButton("Grabar")
        grabar_pb.clicked.connect(self.rec)
        grabar_pb.setChecked(False)
        grabar_pb.setFont(QFont('Helvetica', 32))
        grabar_pb.setStyleSheet
        
        info_pb = QPushButton("Info")
        info_pb.clicked.connect(self.info)
        info_pb.setChecked(False)
        info_pb.setFont(QFont('Helvetica', 11))
        info_pb.setStyleSheet
        
        import numpy as np
        import sounddevice as sd
                      
        devices = sd.query_devices()
        devices_str = [0]*len(devices)
        
        for i in np.arange(len(devices)):
            device_i = devices[i]
            devices_str[i] = device_i['name']
        
        devices_str.append('Seleccione el dispositivo')
                 
        self.in_cb = QComboBox(self)
        self.in_cb.activated[str].connect(self.default_input_audio) 
        self.in_cb.addItems(devices_str)
        self.in_cb.setCurrentIndex(len(devices_str)-1)
        self.in_cb.setFont(QFont('Helvetica', 11))
        self.in_cb.setStyleSheet
        
        self.out_cb = QComboBox(self)
        self.out_cb.activated[str].connect(self.default_output_audio) 
        self.out_cb.addItems(devices_str)
        self.out_cb.setCurrentIndex(len(devices_str)-1)
        self.out_cb.setFont(QFont('Helvetica', 11))
        self.out_cb.setStyleSheet
        
        mainLayout.addWidget(info1_label,0,0,1,2)       
        mainLayout.addWidget(info_pb,0,2,1,1)
        mainLayout.addWidget(input_label,2,0,1,1)
        mainLayout.addWidget(output_label,3,0,1,1)
        mainLayout.addWidget(self.in_cb,2,1,1,2)
        mainLayout.addWidget(self.out_cb,3,1,1,2)
        mainLayout.addWidget(grabar_pb,5,0,1,3)
                
        
    def info(self):
        from PyQt5.QtWidgets import QMessageBox
        
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('DOCENTES: Mieza, Ignacio - Greco, Antonio -' +"\n" + '                      Leguizamón, Diego - Marzik, Guillermo' +"\n" + "\n" +'ESTUDIANTES: Castelli, Corina - Passano, Nahuel' )
        msgBox.setWindowTitle("Información")
        msgBox.setStandardButtons(QMessageBox.Ok)        
        returnValue = msgBox.exec()        
        
        
    def rec(self):
        try:        
            audio_muestra = recording(3)
            global result
            result = identifier(audio_muestra,1)
            
            if result[0] !='no_match':
                from PyQt5.QtWidgets import QMessageBox
                title = result[0]
                
                msgBox = QMessageBox()
                msgBox.setText(str(title))
                msgBox.setWindowTitle("I's a match!")
                msgBox.setStandardButtons(QMessageBox.Ok)
                
                play = msgBox.addButton('Play', QtWidgets.QMessageBox.ActionRole)
                play.disconnect()
                play.clicked.connect(self.play_song)
    
                stop = msgBox.addButton('Stop', QtWidgets.QMessageBox.ActionRole)
                stop.disconnect()
                stop.clicked.connect(self.stop_song)
                returnValue = msgBox.exec()
                       
            else: 
                from PyQt5.QtWidgets import QMessageBox
                msgBox = QMessageBox()
                msgBox.setText('No se pudo identificar la canción.')
                msgBox.setWindowTitle("No match :(")
                msgBox.setStandardButtons(QMessageBox.Ok)
                returnValue = msgBox.exec()
        except:
            msgbox_alert = QMessageBox()
            msgbox_alert.setIcon(QMessageBox.Warning)
            msgbox_alert.setText('Error en la ejecución, asegurese de configurar la entrada y salida de audio')
            
    def play_song(self):        
        data, fs = sf.read(result[1], dtype='float32')   
        sd.default.device = (input_index,output_index)
        sd.play(data, fs)

    def stop_song(self):
        sd.stop()      
        
    def default_input_audio(self):
        global input_index
        input_index = self.in_cb.currentIndex()
        
        
    def default_output_audio(self):
        global output_index
        output_index = self.out_cb.currentIndex()
        
    
                
if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_())
