from logging.handlers import QueueHandler
import sys  # We need sys so we can pass argv to QApplication
import os

from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 

from PyQt5 import QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import requests

class GUI(QMainWindow):

    def __init__(self):
 
        super().__init__()

        '''<----------------Central Widget---------------->'''
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        '''<----------------Layout---------------->'''
        self.mainLayout = QVBoxLayout() #main layout

        '''<----------------Horizontal Layout Box---------------->'''
        self.horizontalTop = QHBoxLayout()

        '''<----------------Calibration Data---------------->'''

        #calibration Frame
        self.calFrame = QFrame()
        self.calFrame.setStyleSheet(   """
                  background-color: white;
                  border-radius: 10px;
            """)
        #self.calFrame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.shadow1 = QGraphicsDropShadowEffect(blurRadius = 15, xOffset = 2, yOffset = 2)
        self.calFrame.setGraphicsEffect(self.shadow1)
            
        self.calGrid = QGridLayout(self.calFrame) #Grid layout for cal values
        
        '''CVA Labels'''
        self.cvaLabel = QLabel()
        self.cvaLabel.setFont(QFont('Times', 12))
        self.cvaLabel.setText("CVA Calibration")
        self.cvaLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.calCVASysLabel = QLabel()
        self.calCVASysLabel.setFont(QFont('Times', 12))
        self.calCVASysLabel.setText("System")
        self.calCVASysLabel.setAlignment(QtCore.Qt.AlignCenter)
    
        self.calCVAAccelLabel = QLabel()
        self.calCVAAccelLabel.setFont(QFont('Times', 12))
        self.calCVAAccelLabel.setText("Gyro")
        self.calCVAAccelLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.calCVAGyroLabel = QLabel()
        self.calCVAGyroLabel.setFont(QFont('Times', 12))
        self.calCVAGyroLabel.setText("Accel")
        self.calCVAGyroLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.cvaSLabel = QLabel()
        self.cvaSLabel.setFont(QFont('Times', 12))
        self.cvaSLabel.setText("0")
        self.cvaSLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.cvaALabel = QLabel()
        self.cvaALabel.setFont(QFont('Times', 12))
        self.cvaALabel.setText("0")
        self.cvaALabel.setAlignment(QtCore.Qt.AlignCenter)

        self.cvaGLabel = QLabel()
        self.cvaGLabel.setFont(QFont('Times', 12))
        self.cvaGLabel.setText("0")
        self.cvaGLabel.setAlignment(QtCore.Qt.AlignCenter)

        '''Thoracic Labels'''
        self.thLabel = QLabel()
        self.thLabel.setFont(QFont('Times', 12))
        self.thLabel.setText("Thoracic Calibration")
        self.thLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.calthSysLabel = QLabel()
        self.calthSysLabel.setFont(QFont('Times', 12))
        self.calthSysLabel.setText("System")
        self.calthSysLabel.setAlignment(QtCore.Qt.AlignCenter)
    
        self.calthAccelLabel = QLabel()
        self.calthAccelLabel.setFont(QFont('Times', 12))
        self.calthAccelLabel.setText("Gyro")
        self.calthAccelLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.calthGyroLabel = QLabel()
        self.calthGyroLabel.setFont(QFont('Times', 12))
        self.calthGyroLabel.setText("Accel")
        self.calthGyroLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.thSLabel = QLabel()
        self.thSLabel.setFont(QFont('Times', 12))
        self.thSLabel.setText("0")
        self.thSLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.thALabel = QLabel()
        self.thALabel.setFont(QFont('Times', 12))
        self.thALabel.setText("0")
        self.thALabel.setAlignment(QtCore.Qt.AlignCenter)

        self.thGLabel = QLabel()
        self.thGLabel.setFont(QFont('Times', 12))
        self.thGLabel.setText("0")
        self.thGLabel.setAlignment(QtCore.Qt.AlignCenter)

        '''Add Labels to Widget'''
        #CVA
        self.calGrid.addWidget(self.cvaLabel, 1, 1)

        self.calGrid.addWidget(self.calCVASysLabel, 2, 0)
        self.calGrid.addWidget(self.calCVAAccelLabel, 2, 1)
        self.calGrid.addWidget(self.calCVAGyroLabel, 2, 2)

        self.calGrid.addWidget(self.cvaSLabel, 3, 0)
        self.calGrid.addWidget(self.cvaALabel, 3, 1)
        self.calGrid.addWidget(self.cvaGLabel, 3, 2)

        #Thoracic
        self.calGrid.addWidget(self.thLabel, 4, 1)

        self.calGrid.addWidget(self.calthSysLabel, 5, 0)
        self.calGrid.addWidget(self.calthAccelLabel, 5, 1)
        self.calGrid.addWidget(self.calthGyroLabel, 5, 2)

        self.calGrid.addWidget(self.thSLabel, 6, 0)
        self.calGrid.addWidget(self.thALabel, 6, 1)
        self.calGrid.addWidget(self.thGLabel, 6, 2)

        '''Add Frame to Horizontal Widget'''
        self.horizontalTop.addWidget(self.calFrame)

        '''<----------------Data---------------->'''
        self.dataFrame = QFrame()
        self.dataFrame.setStyleSheet(
            """
                  background-color: white;
                  border-radius: 10px;
            """
        )
        #self.dataFrame.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.shadow2 = QGraphicsDropShadowEffect(blurRadius = 15, xOffset = 2, yOffset = 2)
        self.dataFrame.setGraphicsEffect(self.shadow2)
        
        
        self.dataGrid = QGridLayout(self.dataFrame)

        '''Data Labels'''
        self.dataLabel = QLabel()
        self.dataLabel.setFont(QFont('Helvetica', 12))
        self.dataLabel.setText("Data")
        #self.dataLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.cvaLabel = QLabel()
        self.cvaLabel.setFont(QFont('Times', 12))
        self.cvaLabel.setText("CVA Angle:")
        #self.cvaLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.thLabel = QLabel()
        self.thLabel.setFont(QFont('Times', 12))
        self.thLabel.setText("Upper Thoracic Angle:")
        #self.cvaLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.cvaDataLabel = QLabel()
        self.cvaDataLabel.setFont(QFont('Times', 12))
        self.cvaDataLabel.setText("0")
        #self.cvaDataLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.thDataLabel = QLabel()
        self.thDataLabel.setFont(QFont('Times', 12))
        self.thDataLabel.setText("0")
        #self.thDataLabel.setAlignment(QtCore.Qt.AlignCenter)
    
        '''Add Labels to Widget'''
        self.dataGrid.addWidget(self.dataLabel, 1, 1)

        self.dataGrid.addWidget(self.cvaLabel, 2, 0)
        self.dataGrid.addWidget(self.cvaDataLabel, 2, 1)

        self.dataGrid.addWidget(self.thLabel, 3, 0)
        self.dataGrid.addWidget(self.thDataLabel, 3, 1)

        '''Add Frame to Horizontal Widget'''
        self.horizontalTop.addWidget(self.dataFrame)

        
        '''<----------------Button---------------->'''
        self.btnFrame = QFrame()
        self.btnFrame.setStyleSheet(
            """
                  background-color: white;
                  border-radius: 10px;
            """
        )
        self.shadow3 = QGraphicsDropShadowEffect(blurRadius = 15, xOffset = 2, yOffset = 2)
        self.btnFrame.setGraphicsEffect(self.shadow3)
        
        self.btnVert = QVBoxLayout(self.btnFrame)

        self.dataBtn = QPushButton("Data Stop")
        self.dataBtn.setFixedSize(150, 50)
       
        self.dataBtn.setStyleSheet("QPushButton"
                             "{"
                             "background-color : lightblue;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : grey;"
                             "}"
                             )
        self.dataBtn.clicked.connect(self.dataBtnState)

        self.btnVert.addWidget(self.dataBtn)
        
        self.horizontalTop.addWidget(self.btnFrame, alignment= QtCore.Qt.AlignCenter)

        '''Add horizontal layout to main layout'''
        self.mainLayout.addLayout(self.horizontalTop)


        '''<----------------Variables---------------->'''
        self.angThoracic = [0]
        self.angCVA = [0]

        self.timeThoracic = [0]
        self.timeCVA = [0]
        self.counter = 0

        self.cvaFreq = 0.5
        self.thFreq = 0.5

        #CVA sensor
        self.cal1 = 0 #system
        self.cal2 = 0 #accel
        self.cal3 = 0 #gyro

        #UT sensor
        self.cal4 = 0 #system
        self.cal5 = 0 #accel
        self.cal6 = 0 #gryo

        '''<----------------Graphs---------------->'''
        self.graphWidget1 = pg.PlotWidget()
        self.graphWidget2 = pg.PlotWidget()

        #self.graphWidget1.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0)) #line colour
        self.data_line1 =  self.graphWidget1.plot(self.angCVA, self.timeCVA, pen=pen)
        self.data_line2 =  self.graphWidget2.plot(self.angThoracic, self.timeThoracic, pen=pen)

        self.graphWidget1.setLabel("left", "Angle (°)")
        self.graphWidget1.setLabel("bottom", "Time (s)")

        self.graphWidget2.setLabel("left", "Angle (°)")
        self.graphWidget2.setLabel("bottom", "Time (s)")

        self.graphWidget1.setTitle("CVA Angle")
        self.graphWidget2.setTitle("Upper Thoracic Angle")

        self.graphVert = QVBoxLayout()

        self.graphVert.addWidget(self.graphWidget1)
        self.graphVert.addWidget(self.graphWidget2)

        '''Add graph layout to main layout '''
        self.mainLayout.addLayout(self.graphVert)

        '''Add main layout to Central Widget'''
        self.centralWidget.setLayout(self.mainLayout)
        
        '''<----------------Timers---------------->'''
        '''Cal Timers'''
        self.timerCal = QtCore.QTimer() #checking if calibration is done or not
        self.timerCal.setInterval(1500)
        self.timerCal.timeout.connect(self.startTimers)
        self.timerCal.start()

        self.timerCVAFlask = QtCore.QTimer() #get cva cal values from flask
        self.timerCVAFlask.setInterval(850)
        self.timerCVAFlask.timeout.connect(self.getFromFlaskCVA)
        self.timerCVAFlask.start()

        self.timerThFlask = QtCore.QTimer() #get th cal values from flask
        self.timerThFlask.setInterval(850)
        self.timerThFlask.timeout.connect(self.getFromFlaskTH)
        self.timerThFlask.start()

        self.timerCalLabel = QtCore.QTimer() #update cal values on GUI
        self.timerCalLabel.setInterval(850)
        self.timerCalLabel.timeout.connect(self.updateLabelCal)
        self.timerCalLabel.start()

        '''Data Timers'''
        self.timerFire = QtCore.QTimer() #get data from firebase
        self.timerFire.setInterval(1000)
        self.timerFire.timeout.connect(self.getData)

        self.timerDataLabel = QtCore.QTimer() #update CVA and TH angles on GUI
        self.timerDataLabel.setInterval(850)
        self.timerDataLabel.timeout.connect(self.updateLabelData)

        self.timerPlotData = QtCore.QTimer() #plot data 
        self.timerPlotData.setInterval(1000)
        self.timerPlotData.timeout.connect(self.plotData)
    
    def startTimers(self):
        if(self.cal1 > 0 and self.cal2 == 3 and self.cal3 == 3 and self.cal4 > 0 and self.cal5 == 3 and self.cal6 == 3):
            #turn cal timers off 
            self.timerCal.stop()
            self.timerCVAFlask.stop()
            self.timerThFlask.stop()
            self.timerCalLabel.stop()

            #turn data timers on
            self.timerFire.start()
            self.timerDataLabel.start()
            self.timerPlotData.start()

    def getFromFlaskCVA(self):
        #attempt to make the GUi more robust LMAO
        try:
            self.serverAddress1 = "http://89c8-130-113-109-139.ngrok.io/getCalibrationStatus"
            self.calCVA = requests.get(self.serverAddress1)
            self.calCVATxt = self.calCVA.text
            self.calCVASplit = self.calCVATxt.split(',')

            self.cal1 = int(self.calCVASplit[0])
            self.cal2 = int(self.calCVASplit[1])
            self.cal3 = 3

        except:
            pass
    
    def getFromFlaskTH(self):
        try:
            self.serverAddress2 = "https://8076-130-113-109-97.ngrok.io/getCalibrationStatus"
            self.calTH = requests.get(self.serverAddress2)
            self.calTHTxt = self.calTH.text 
            self.calTHSplit = self.calTHTxt.split(',')

            self.cal4 = int(self.calTHSplit[0])
            self.cal5 = int(self.calTHSplit[1])
            self.cal6 = 3

        except:
            pass
    
    def updateLabelCal(self):
        #update calibration labels
        self.cvaSLabel.setText(str(self.cal1))
        self.cvaALabel.setText(str(self.cal2))
        self.cvaGLabel.setText(str(self.cal3))

        self.thSLabel.setText(str(self.cal4))
        self.thALabel.setText(str(self.cal5))
        self.thGLabel.setText(str(self.cal6))

    def getData(self):
        self.cvaSLabel.setText(str(self.cal1))
        self.cvaALabel.setText(str(self.cal2))
        self.cvaGLabel.setText(str(self.cal3))

        self.thSLabel.setText(str(self.cal4))
        self.thALabel.setText(str(self.cal5))
        self.thGLabel.setText(str(self.cal6))

        if not firebase_admin._apps:
            cred = credentials.Certificate(
                'neckangle-67211-firebase-adminsdk-xy324-15b8d262a0.json')
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://neckangle-67211-default-rtdb.firebaseio.com/'
            })
        else:
            firebase_admin._apps

        refCVA = db.reference('/users/test/Current CVA Angle')
        refTh = db.reference('/users/test/Current Thoracic Angle')

        self.getCVA = refCVA.get()
        self.getTh = refTh.get()

        self.angCVA.append(int(self.getCVA))
        self.angThoracic.append(int(self.getTh))

        self.counter += 0.5
        # self.cvaAngles = self.getCVA.strip('][').split(', ')
        # self.thAngles = self.getTh.strip('][').split(', ')

        # self.angCVA = [float(i) for i in self.cvaAngles]
        # self.angThoracic = [float(i) for i in self.thAngles]
        self.timeCVA.append(self.counter)

        self.timeThoracic.append(self.counter)
        
    
    def updateLabelData(self):
        self.cvaDataLabel.setText(str(self.angCVA[-1]) + "°")
        self.thDataLabel.setText(str(self.angThoracic[-1]) + "°")

    def plotData(self):

        if(len(self.angCVA) > 22):
            self.angThoracic = self.angThoracic[1:]  # Remove first element.

            self.timeThoracic = self.timeThoracic[1:]  # Remove first element. 
            
            self.angCVA = self.angCVA[1:]  # Remove first element.

            self.timeCVA = self.timeCVA[1:]  # Remove first element. 

        #ensure that each array is the same length so it plots properly - taking into account when one sensor calibrates before other sensor
        if(len(self.angThoracic) != len(self.angCVA)):
            self.minLength = min(len(self.angThoracic), len(self.angCVA))

            # print(self.minLength)
            self.angThoracic = self.angThoracic[:self.minLength]
            self.angCVA = self.angCVA[:self.minLength]

            self.timeThoracic = self.timeThoracic[:self.minLength]
            self.timeCVA = self.timeCVA[:self.minLength]

        self.data_line1.setData(self.timeCVA, self.angCVA) #CVA
        self.data_line2.setData(self.timeThoracic, self.angThoracic) #Thoracic

    def dataBtnState(self):
        if(self.timerDataLabel.isActive() and self.timerPlotData.isActive()):
            self.timerDataLabel.stop()
            self.timerPlotData.stop()
            self.dataBtn.setText("Data Start")
        else:
            self.timerDataLabel.start()
            self.timerPlotData.start()
            self.dataBtn.setText("Data Stop")

def main():
    # Create an instance of QApplication
    gui = QApplication(sys.argv)
    # Show GUI
    view = GUI()
    view.show()
    # Execute main loop
    sys.exit(gui.exec_())

if __name__ == '__main__':
    main()
