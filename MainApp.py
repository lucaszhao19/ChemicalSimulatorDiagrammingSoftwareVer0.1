from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtGui import QBrush ,QTransform ,QMouseEvent, QPaintDevice
from PyQt5.QtCore import pyqtSignal

import sys
import pickle
from functools import partial
from Graphics import *
from SwitchButton import *

ui,_ = loadUiType('main1.ui')

'''
    MainApp class is responsible for all the main App Ui operations
'''
class MainApp(QMainWindow,ui):


    flag = True

    def __init__(self):
        '''
            Initializing the application
        '''
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.zoomcount = 0
        
        self.graphics = Graphics()
        self.scene = self.graphics.getScene()
        Graphics.flag = MainApp.flag

        self.previewBtn.setChecked(True)
        self.editingBtn.toggled.connect(lambda:self.btnState(self.previewBtn))
        self.previewBtn.toggled.connect(lambda:self.btnState(self.editingBtn))

        self.graphicsView.setScene(self.scene)
        self.graphicsView.setMouseTracking(True)
        self.graphicsView.keyPressEvent=self.deleteCall
    
        self.menuBar()
        self.unitOperationListInit()

    def unitOperationListInit(self):
        self.gl1.addWidget(self.createCellWidget("Air-blownCooler"), 1, 0)
        self.gl1.addWidget(self.createCellWidget("Bag"), 1, 1)
        self.gl1.addWidget(self.createCellWidget("Boiler"), 1, 2)
        self.gl1.addWidget(self.createCellWidget("Tank"), 2, 0)
        self.gl1.addWidget(self.createCellWidget("Breaker"), 2, 1)
        self.gl1.addWidget(self.createCellWidget("BriquettingMachine"), 2, 2)
        self.gl1.addWidget(self.createCellWidget("Centrifugal"), 3, 0)
        self.gl1.addWidget(self.createCellWidget("CentrifugalCompressor"), 3, 1)
        self.gl1.addWidget(self.createCellWidget("CentrifugalPump"), 3, 2)
        self.gl1.addWidget(self.createCellWidget("CentrifugalPump2"), 4, 0)
        self.gl1.addWidget(self.createCellWidget("CentrifugalPump3"), 4, 1)
        self.gl1.addWidget(self.createCellWidget("Column"), 4, 2)
        self.gl1.addWidget(self.createCellWidget("Compressor"), 5, 0)
        self.gl1.addWidget(self.createCellWidget("CompressorSilencers"), 5, 1)
        self.gl1.addWidget(self.createCellWidget("Condenser"), 5, 2)
        self.gl1.addWidget(self.createCellWidget("Cooler"), 6, 0)
        self.gl1.addWidget(self.createCellWidget("CoolingTower2"), 6, 1)
        self.gl1.addWidget(self.createCellWidget("CoolingTower3"), 6, 2)
        self.gl1.addWidget(self.createCellWidget("Crusher"), 7, 0)
        self.gl1.addWidget(self.createCellWidget("DoublePipeHeat"), 7, 1)
        self.gl1.addWidget(self.createCellWidget("ExtractorHood"), 7, 2)
        self.gl1.addWidget(self.createCellWidget("FiredHeater"), 8, 0)
        self.gl1.addWidget(self.createCellWidget("Forced-draftCooling"), 8, 1)
        self.gl1.addWidget(self.createCellWidget("Forced-draftCoolingTower"), 8, 2)
        self.gl1.addWidget(self.createCellWidget("Furnance"), 9, 0)
        self.gl1.addWidget(self.createCellWidget("GasBottle"), 9, 1)
        self.gl1.addWidget(self.createCellWidget("HalfPipeMixingVessel"), 9, 2)
        self.gl1.addWidget(self.createCellWidget("Heater"), 10, 0)
        self.gl1.addWidget(self.createCellWidget("HeatExchanger"), 10, 1)
        self.gl1.addWidget(self.createCellWidget("HeatExchanger2"), 10, 2)
        self.gl1.addWidget(self.createCellWidget("HorizontalVessel"), 11, 0)
        self.gl1.addWidget(self.createCellWidget("JacketedMixingVessel"), 11, 1)
        self.gl1.addWidget(self.createCellWidget("LiquidRingCompressor"), 11, 2)
        self.gl1.addWidget(self.createCellWidget("Mixing"),12 , 0)
        self.gl1.addWidget(self.createCellWidget("MixingReactor"), 12, 1)
        self.gl1.addWidget(self.createCellWidget("OilBurner"), 12, 2)
        self.gl1.addWidget(self.createCellWidget("OpenTank"), 13, 0)
        self.gl1.addWidget(self.createCellWidget("ProportioningPump"), 13, 1)
        self.gl1.addWidget(self.createCellWidget("Pump"), 13, 2)
        self.gl1.addWidget(self.createCellWidget("Pump2"), 14, 0)
        self.gl1.addWidget(self.createCellWidget("ReboilerHeatExchanger"), 14, 1)
        self.gl1.addWidget(self.createCellWidget("ReciprocativeCompressor"), 14, 2)
        self.gl1.addWidget(self.createCellWidget("RotaryCompressor"), 15, 0)
        self.gl1.addWidget(self.createCellWidget("RotaryGearPump"), 15, 1)
        self.gl1.addWidget(self.createCellWidget("ScrewPump"),15 , 2)
        self.gl1.addWidget(self.createCellWidget("SelectableCompressor"), 16, 0)
        self.gl1.addWidget(self.createCellWidget("SelectableFan"), 16, 1)
        self.gl1.addWidget(self.createCellWidget("SinglePassHeat"), 16, 2)
        self.gl1.addWidget(self.createCellWidget("SpiralHeatExchanger"), 17, 0)
        self.gl1.addWidget(self.createCellWidget("StraightTubesHeat"), 17, 1)
        self.gl1.addWidget(self.createCellWidget("Tank"), 17, 2)
        self.gl1.addWidget(self.createCellWidget("TurbinePump"), 18, 0)
        self.gl1.addWidget(self.createCellWidget("U-TubeHeatExchanger"), 18, 1)
        self.gl1.addWidget(self.createCellWidget("VacuumPump"), 18, 2)
        self.gl1.addWidget(self.createCellWidget("VerticalPump"), 19, 0)
        self.gl1.addWidget(self.createCellWidget("VerticalVessel"), 19, 1)
        self.gl1.addWidget(self.createCellWidget("WastewaterTreatment"), 19, 2)
        
        self.gl2.addWidget(self.createCellWidget("Air-blownCooler"), 1, 0)
        self.gl2.addWidget(self.createCellWidget("Bag"), 1, 1)
        self.gl2.addWidget(self.createCellWidget("Boiler"), 1, 2)
        self.gl2.addWidget(self.createCellWidget("Tank"), 2, 0)
        self.gl2.addWidget(self.createCellWidget("Breaker"), 2, 1)
        self.gl2.addWidget(self.createCellWidget("BriquettingMachine"), 2, 2)
        self.gl2.addWidget(self.createCellWidget("Centrifugal"), 3, 0)
        self.gl2.addWidget(self.createCellWidget("CentrifugalCompressor"), 3, 1)
        self.gl2.addWidget(self.createCellWidget("CentrifugalPump"), 3, 2)
        self.gl2.addWidget(self.createCellWidget("CentrifugalPump2"), 4, 0)
        self.gl2.addWidget(self.createCellWidget("CentrifugalPump3"), 4, 1)
        self.gl2.addWidget(self.createCellWidget("Column"), 4, 2)
        self.gl2.addWidget(self.createCellWidget("Compressor"), 5, 0)
        self.gl2.addWidget(self.createCellWidget("CompressorSilencers"), 5, 1)
        self.gl2.addWidget(self.createCellWidget("Condenser"), 5, 2)
        self.gl2.addWidget(self.createCellWidget("Cooler"), 6, 0)
        self.gl2.addWidget(self.createCellWidget("CoolingTower2"), 6, 1)
        self.gl2.addWidget(self.createCellWidget("CoolingTower3"), 6, 2)
        self.gl2.addWidget(self.createCellWidget("Crusher"), 7, 0)
        self.gl2.addWidget(self.createCellWidget("DoublePipeHeat"), 7, 1)
        self.gl2.addWidget(self.createCellWidget("ExtractorHood"), 7, 2)
        self.gl2.addWidget(self.createCellWidget("FiredHeater"), 8, 0)
        self.gl2.addWidget(self.createCellWidget("Forced-draftCooling"), 8, 1)
        self.gl2.addWidget(self.createCellWidget("Forced-draftCoolingTower"), 8, 2)
        self.gl2.addWidget(self.createCellWidget("Furnance"), 9, 0)
        self.gl2.addWidget(self.createCellWidget("GasBottle"), 9, 1)
        self.gl2.addWidget(self.createCellWidget("HalfPipeMixingVessel"), 9, 2)
        self.gl2.addWidget(self.createCellWidget("Heater"), 10, 0)
        self.gl2.addWidget(self.createCellWidget("HeatExchanger"), 10, 1)
        self.gl2.addWidget(self.createCellWidget("HeatExchanger2"), 10, 2)
        self.gl2.addWidget(self.createCellWidget("HorizontalVessel"), 11, 0)
        self.gl2.addWidget(self.createCellWidget("JacketedMixingVessel"), 11, 1)
        self.gl2.addWidget(self.createCellWidget("LiquidRingCompressor"), 11, 2)
        self.gl2.addWidget(self.createCellWidget("Mixing"),12 , 0)
        self.gl2.addWidget(self.createCellWidget("MixingReactor"), 12, 1)
        self.gl2.addWidget(self.createCellWidget("OilBurner"), 12, 2)
        self.gl2.addWidget(self.createCellWidget("OpenTank"), 13, 0)
        self.gl2.addWidget(self.createCellWidget("ProportioningPump"), 13, 1)
        self.gl2.addWidget(self.createCellWidget("Pump"), 13, 2)
        self.gl2.addWidget(self.createCellWidget("Pump2"), 14, 0)
        self.gl2.addWidget(self.createCellWidget("ReboilerHeatExchanger"), 14, 1)
        self.gl2.addWidget(self.createCellWidget("ReciprocativeCompressor"), 14, 2)
        self.gl2.addWidget(self.createCellWidget("RotaryCompressor"), 15, 0)
        self.gl2.addWidget(self.createCellWidget("RotaryGearPump"), 15, 1)
        self.gl2.addWidget(self.createCellWidget("ScrewPump"),15 , 2)
        self.gl2.addWidget(self.createCellWidget("SelectableCompressor"), 16, 0)
        self.gl2.addWidget(self.createCellWidget("SelectableFan"), 16, 1)
        self.gl2.addWidget(self.createCellWidget("SinglePassHeat"), 16, 2)
        self.gl2.addWidget(self.createCellWidget("SpiralHeatExchanger"), 17, 0)
        self.gl2.addWidget(self.createCellWidget("StraightTubesHeat"), 17, 1)
        self.gl2.addWidget(self.createCellWidget("Tank"), 17, 2)
        self.gl2.addWidget(self.createCellWidget("TurbinePump"), 18, 0)
        self.gl2.addWidget(self.createCellWidget("U-TubeHeatExchanger"), 18, 1)
        self.gl2.addWidget(self.createCellWidget("VacuumPump"), 18, 2)
        self.gl2.addWidget(self.createCellWidget("VerticalPump"), 19, 0)
        self.gl2.addWidget(self.createCellWidget("VerticalVessel"), 19, 1)
        self.gl2.addWidget(self.createCellWidget("WastewaterTreatment"), 19, 2)

    def createCellWidget(self, text):
        pic=QtGui.QPixmap("unitOp/type1/"+text+".png")
        icon = QIcon(pic)
        button = QToolButton()
        button.setText(text)
        button.setIcon(icon)
        button.setIconSize(QSize(44, 44))
        button.setToolTip(text) 
        layout = QGridLayout()
        layout.addWidget(button, 0, 0, Qt.AlignHCenter)
        #layout.addWidget(QLabel(text), 1, 0, Qt.AlignCenter)
        widget = QWidget()
        widget.setLayout(layout)

        button.pressed.connect(lambda:self.component(text))
        
        return widget

    def btnState(self, b): 
        
        item = QGraphicsLineItem(QLineF(0,0,0,0))
        self.scene.addItem(item)
        #item.setPos(QPointF(2500,2500))
        item.setPos(NodeItem.pos)
        if b.text() == "Editing":
            if b.isChecked() == True:
                MainApp.flag = not MainApp.flag
                Graphics.flag = MainApp.flag
                for socket in socketLst:
                    NodeSocket.restoreSockets(socket)
                for i in lst:
                    NodeSocket.removeSockets(i[1])
                    NodeSocket.removeSockets(i[2])
        else:
            if b.isChecked() == True:
                MainApp.flag = not MainApp.flag
                Graphics.flag = MainApp.flag
                for socket in socketLst:               
                    NodeSocket.removeSockets(socket)
		   
    def menuBar(self):
        '''
            MenuBar function handels all the all the operations of 
            menu bar like new,zoom,comounds selector, simulation options.
        '''
        self.actionNew.triggered.connect(self.new)
        self.actionZoomIn.triggered.connect(self.zoomIn)
        self.actionZoomOut.triggered.connect(self.zoomOut)
        self.actionZoomReset.triggered.connect(self.zoomReset)
        self.actionSave.triggered.connect(self.save)
        self.actionInsertText.triggered.connect(self.insertText)
        self.actionSocket.triggered.connect(self.socket)
        self.actionNumber.triggered.connect(self.number)

    def zoomReset(self):
        '''
            Resets the zoom level to default scaling
        '''
        if(self.zoomcount>0):
            for i in range(self.zoomcount):
                self.zoomOut()
        elif(self.zoomcount<0): 
            for i in range(abs(self.zoomcount)):
                self.zoomIn()

    def zoomOut(self):
        '''
            ZoomOut the canvas
        '''
        self.graphicsView.scale(1.0/1.15,1.0/1.15)
        self.zoomcount -=1
 
    def zoomIn(self):
        '''
            ZoomIn the canvas
        '''
        if self.zoomcount < 0:
            self.graphicsView.scale(1.15,1.15)
            self.zoomcount +=1
  
    def component(self,unitOpType):
        '''
            Instantiate a NodeItem object for selected type of
            component and added that on canvas/flowsheeting area.
        ''' 
        if MainApp.flag == True:
            self.type = unitOpType
            self.obj = self.graphics.createNodeItem(self.type, self.graphicsView)
            self.scene.addItem(self.obj)
            self.obj.setPos(QPointF(2500-30, 2500-30))
          
    def new(self):
        '''
            New is used to delete all the existing work.
        ''' 
        if MainApp.flag: 
            del self.graphics
            self.graphics = Graphics()
            self.scene = self.graphics.getScene()
            self.graphicsView.setScene(self.scene)
            self.graphicsView.setMouseTracking(True)
            self.graphicsView.keyPressEvent=self.deleteCall
    
    def deleteCall(self,event):
        '''
            Handels all the operations which will happen when delete button is pressed.
        '''
        try:
            if event.key() == QtCore.Qt.Key_Delete:
                l=self.scene.selectedItems()
                self.delete(l)
        except Exception as e:
            print(e)
    
    def delete(self,l): 
        '''
            Deletes the selected item from the canvas and also the objects 
            created for that type.
        '''      
        if MainApp.flag:
            for item in l:
                self.scene.removeItem(item)
                if (item.typee == 'Graphics.NodeLine'):
                    for i in lst:
                        if i[0] == item:                
                            NodeSocket.restoreSockets(i[1])
                            NodeSocket.restoreSockets(i[2])
                            lst.remove(i) 
                del item

    def socket(self):
        if MainApp.flag:
            item = self.graphics.createNodeItem('none1',self.graphicsView)
            self.scene.addItem(item)  
            item.setPos(QPointF(2020, 2200))

    def number(self):
        if MainApp.flag:
            self.numberItem = NumberItem(self.graphicsView)
            self.scene.addItem(self.numberItem)  
            self.numberItem.setPos(QPointF(2020, 2200))

    def insertText(self):
        if MainApp.flag:
            self.textItem = TextItem(self.graphicsView)
            self.scene.addItem(self.textItem)  
            self.textItem.setPos(QPointF(2020, 2200))
            
    def save(self):
        '''
            Function for saving the current canvas items and compound_selected
        '''
        '''# Get region of scene to capture from somewhere.
        #area = get_QRect_to_capture_from_somewhere()
        area = QRectF(QPointF(0,0), QPointF(1500, 1500))

        # Create a QImage to render to and fix up a QPainter for it.
        image = QImage(area.width() , area.height(), QImage.Format_ARGB32_Premultiplied)

        painter = QPainter(image)

        # Render the region of interest to the QImage.
        self.scene.render(painter)
        painter.end()
       
        fileFormat = 'png'
        initialPath = QDir.currentPath() + 'image.' + fileFormat
        fileName, _ = QFileDialog.getSaveFileName(self, "Save As",
                                                  initialPath, "%s Files (*.%s);; All Files (*)" %
                                                  (fileFormat.upper(), fileFormat))
        if fileName != "":
            with open(fileName, 'wb') as f: 
                image.save(fileName+fileFormat)
        
        '''
        fileFormat = 'png'
        initialPath = QDir.currentPath() + 'untitled.' + fileFormat
        fileName, _ = QFileDialog.getSaveFileName(self, "Save As",
                                                  initialPath, "%s Files (*.%s);; All Files (*)" %
                                                  (fileFormat.upper(), fileFormat))
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(self.graphicsView.winId())
        screenshot.save(fileName, fileFormat)


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.showMaximized()
    app.exec()

if __name__ == '__main__':
    main()
