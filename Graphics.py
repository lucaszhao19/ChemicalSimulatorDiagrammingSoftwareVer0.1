from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QTextDocument ,QTextCursor ,QTextCharFormat ,QFont ,QPixmap, QCursor, QTransform, QColor
from PyQt5.uic import loadUiType
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsProxyWidget, QGraphicsObject, QGraphicsEllipseItem ,QGraphicsPixmapItem,QApplication, QGraphicsView, QGraphicsScene, QHBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QPolygonF, QBrush ,QTransform ,QMouseEvent
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer


from functools import partial
from collections import defaultdict
import sys
import math

class Graphics(QtWidgets.QGraphicsItem):
    flag = True

    def __init__(self):
        QtWidgets.QGraphicsItem.__init__(self)
        self.scene = QGraphicsScene()
        self.scene.setItemIndexMethod(QGraphicsScene.BspTreeIndex)
        self.pos = None
    
    def getScene(self):
        return self.scene

    def createNodeItem(self,unitOpType, graphicsView):
        return NodeItem(unitOpType, graphicsView)
    
class NodeLine(QtWidgets.QGraphicsPathItem):
    def __init__(self, pointA, pointB, upDownFlag): 
        super(NodeLine, self).__init__()
        self._pointA = pointA
        self._pointB = pointB
        self.upDownFlag = upDownFlag
        self.typee = 'Graphics.NodeLine'
        self._source = None
        self._target = None
        self.setZValue(-1)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        # Pen
        self.pen = QtGui.QPen()
        self.pen.setStyle(QtCore.Qt.SolidLine)
        self.pen.setWidth(1)
        self.pen.setColor(QtGui.QColor(0,0,0,255))

        # Pen when selected 
        self.selPen = QtGui.QPen()
        self.selPen.setStyle(QtCore.Qt.DashDotDotLine)
        self.selPen.setWidth(1)
        self.selPen.setColor(QtGui.QColor(0,0,0,255))

        # Brush.
        self.brush = QtGui.QBrush()
        self.brush.setStyle(QtCore.Qt.SolidPattern)
        self.brush.setColor(QtGui.QColor(0,0,0,255))


    def updatePath(self):
        
        if (self.upDownFlag):
            if abs(self._pointA.x()-self._pointB.x())>100:
                midpty = self.pointA.y()-80
                    
                path = QtGui.QPainterPath()
                path.moveTo(self.pointA)
                
                ctrl1_1 = QtCore.QPointF(self.pointA.x(), self.pointA.y())
                ctrl2_1 = QtCore.QPointF(self.pointA.x(), self.pointA.y())
                pt1 = QtCore.QPointF(self.pointA.x(), midpty)
                path.cubicTo(ctrl1_1, ctrl2_1, pt1)
                path.moveTo(pt1)

                ctrl1_2 = QtCore.QPointF(self.pointA.x(), midpty)
                ctrl2_2 = QtCore.QPointF(self.pointA.x(), midpty)
                pt2 = QtCore.QPointF(self.pointB.x(), midpty)
                path.cubicTo(ctrl1_2, ctrl2_2, pt2)
                path.moveTo(pt2)

                ctrl1_3 = QtCore.QPointF(self.pointB.x(), midpty)
                ctrl2_3 = QtCore.QPointF(self.pointB.x(), midpty)
                path.cubicTo(ctrl1_3, ctrl2_3, self.pointB)
                path.moveTo(self.pointB)

                if (self.pointB.y() > midpty):
                    c = -8
                else:
                    c = 8
                SMALL_ARROW_WIDTH = 8

                l_arrow = self.pointB - (QPointF(self.pointB.x(), self.pointB.y()+c))
                path.moveTo(QPointF(self.pointB.x(), self.pointB.y()+c))
                path.lineTo(self.pointB)

                length = math.sqrt(l_arrow.x() ** 2 + l_arrow.y() ** 2)
                sita = math.atan2(l_arrow.y(), l_arrow.x())

                p1 = self.pointB - QPointF(SMALL_ARROW_WIDTH * math.cos(sita),
                                        SMALL_ARROW_WIDTH * math.sin(sita))
                p2 = p1 - QPointF(-(SMALL_ARROW_WIDTH / 2) * math.sin(sita),
                                    (SMALL_ARROW_WIDTH / 2) * math.cos(sita))
                p3 = p1 + QPointF(-SMALL_ARROW_WIDTH / 2 * math.sin(sita),
                                    SMALL_ARROW_WIDTH / 2 * math.cos(sita))
                path.addPolygon(QPolygonF([p2, p3, self.pointB, p2]))

                self.setPath(path)
                return

            else:
                path = QtGui.QPainterPath()
                midpty = 0.5*(self.pointA.y() + self.pointB.y())
                path.moveTo(self.pointA)

                ctrl1_1 = QtCore.QPointF(self.pointA.x(), self.pointA.y())
                ctrl2_1 = QtCore.QPointF(self.pointA.x(), self.pointA.y())
                pt1 = QtCore.QPointF(self.pointA.x(), midpty)
                path.cubicTo(ctrl1_1, ctrl2_1, pt1)
                path.moveTo(pt1)

                ctrl1_2 = QtCore.QPointF(self.pointA.x(), midpty)
                ctrl2_2 = QtCore.QPointF(self.pointA.x(), midpty)
                pt2 = QtCore.QPointF(self.pointB.x(), midpty)
                path.cubicTo(ctrl1_2, ctrl2_2, pt2)
                path.moveTo(pt2)

                ctrl1_3 = QtCore.QPointF(self.pointB.x(), midpty)
                ctrl2_3 = QtCore.QPointF(self.pointB.x(), midpty)
                path.cubicTo(ctrl1_3, ctrl2_3, self.pointB)
                path.moveTo(self.pointB)

                if (self.pointB.y() > midpty):
                    c = -8
                else:
                    c = 8
                
                SMALL_ARROW_WIDTH = 8

                l_arrow = self.pointB - (QPointF(self.pointB.x(), self.pointB.y()+c))
                path.moveTo(QPointF(self.pointB.x(), self.pointB.y()+c))
                path.lineTo(self.pointB)

                length = math.sqrt(l_arrow.x() ** 2 + l_arrow.y() ** 2)
                sita = math.atan2(l_arrow.y(), l_arrow.x())

                p1 = self.pointB - QPointF(SMALL_ARROW_WIDTH * math.cos(sita),
                                        SMALL_ARROW_WIDTH * math.sin(sita))
                p2 = p1 - QPointF(-(SMALL_ARROW_WIDTH / 2) * math.sin(sita),
                                    (SMALL_ARROW_WIDTH / 2) * math.cos(sita))
                p3 = p1 + QPointF(-SMALL_ARROW_WIDTH / 2 * math.sin(sita),
                                    SMALL_ARROW_WIDTH / 2 * math.cos(sita))
                path.addPolygon(QPolygonF([p2, p3, self.pointB, p2]))

                self.setPath(path)
                return

        if (self._pointB.x() - self._pointA.x()) < 30 : 
            path = QtGui.QPainterPath()
            midptx = (self.pointA.x() + 13) 
            path.moveTo(self.pointA)

            ctrl1_1 = QtCore.QPointF(self.pointA.x(), self.pointA.y())
            ctrl2_1 = QtCore.QPointF(self.pointA.x(), self.pointA.y())
            pt1 = QtCore.QPointF(midptx , self.pointA.y())
            path.cubicTo(ctrl1_1, ctrl2_1, pt1)  
            path.moveTo(pt1)

            if abs(self.pointB.x()-midptx) > 150:  
                ctrl1_2 = QtCore.QPointF(midptx, self.pointB.y())
                ctrl2_2 = QtCore.QPointF(midptx, self.pointB.y())
                pt2 = QtCore.QPointF(midptx , self.pointA.y()+100)
                path.cubicTo(ctrl1_2, ctrl2_2, pt2)
                path.moveTo(pt2)

                ctrl1_3 = QtCore.QPointF(midptx, self.pointA.y()+100)
                ctrl2_3 = QtCore.QPointF(midptx, self.pointA.y()+100)
                pt3 = QtCore.QPointF(self.pointB.x()-13, self.pointA.y()+100)
                path.cubicTo(ctrl1_3, ctrl2_3, pt3)
                path.moveTo(pt3)

                ctrl1_4 = QtCore.QPointF(self.pointB.x()-13, max(self.pointB.y(), self.pointA.y())-(abs(self.pointA.y()-self.pointB.y())/2))
                ctrl2_4 = QtCore.QPointF(self.pointB.x()-13, max(self.pointB.y(), self.pointA.y())-(abs(self.pointA.y()-self.pointB.y())/2))
                pt4 = QtCore.QPointF(self.pointB.x()-13, self.pointB.y())
                path.cubicTo(ctrl1_4, ctrl2_4, pt4)
                path.moveTo(pt4)

                ctrl1_5 = QtCore.QPointF(self.pointB.x()-13, self.pointB.y())
                ctrl2_5 = QtCore.QPointF(self.pointB.x()-13, self.pointB.y())
                pt5 = QtCore.QPointF(self.pointB.x(), self.pointB.y())
                path.cubicTo(ctrl1_5, ctrl2_5, pt5)
                path.moveTo(pt5)

                SMALL_ARROW_WIDTH = 8

                l_arrow = self.pointB - (QPointF(self.pointB.x()-8, self.pointB.y()))
                path.moveTo(QPointF(self.pointB.x()-8, self.pointB.y()))
                path.lineTo(self.pointB)

                length = math.sqrt(l_arrow.x() ** 2 + l_arrow.y() ** 2)
                sita = math.atan2(l_arrow.y(), l_arrow.x())
                p1 = self.pointB - QPointF(SMALL_ARROW_WIDTH * math.cos(sita),
                                        SMALL_ARROW_WIDTH * math.sin(sita))
                p2 = p1 - QPointF(-(SMALL_ARROW_WIDTH / 2) * math.sin(sita),
                                (SMALL_ARROW_WIDTH / 2) * math.cos(sita))
                p3 = p1 + QPointF(-SMALL_ARROW_WIDTH / 2 * math.sin(sita),
                                SMALL_ARROW_WIDTH / 2 * math.cos(sita))
                path.addPolygon(QPolygonF([p2, p3, self.pointB, p2]))

                self.setPath(path)
                return
            elif abs(self.pointB.x()-midptx) < 150:
                ctrl1_2 = QtCore.QPointF(midptx, self.pointB.y())
                ctrl2_2 = QtCore.QPointF(midptx, self.pointB.y())
                pt2 = QtCore.QPointF(midptx , max(self.pointB.y(), self.pointA.y())-(abs(self.pointA.y()-self.pointB.y())/2))
                path.cubicTo(ctrl1_2, ctrl2_2, pt2)
                path.moveTo(pt2)

                ctrl1_3 = QtCore.QPointF(midptx, max(self.pointB.y(), self.pointA.y())-(abs(self.pointA.y()-self.pointB.y())/2))
                ctrl2_3 = QtCore.QPointF(midptx, max(self.pointB.y(), self.pointA.y())-(abs(self.pointA.y()-self.pointB.y())/2))
                pt3 = QtCore.QPointF(self.pointB.x()-13,  max(self.pointB.y(), self.pointA.y())-(abs(self.pointA.y()-self.pointB.y())/2))
                path.cubicTo(ctrl1_3, ctrl2_3, pt3)
                path.moveTo(pt3)

                ctrl1_4 = QtCore.QPointF(self.pointB.x()-13, max(self.pointB.y(), self.pointA.y())-(abs(self.pointA.y()-self.pointB.y())/2))
                ctrl2_4 = QtCore.QPointF(self.pointB.x()-13, max(self.pointB.y(), self.pointA.y())-(abs(self.pointA.y()-self.pointB.y())/2))
                pt4 = QtCore.QPointF(self.pointB.x()-13, self.pointB.y())
                path.cubicTo(ctrl1_4, ctrl2_4, pt4)
                path.moveTo(pt4)

                ctrl1_5 = QtCore.QPointF(self.pointB.x()-13, self.pointB.y())
                ctrl2_5 = QtCore.QPointF(self.pointB.x()-13, self.pointB.y())
                pt5 = QtCore.QPointF(self.pointB.x(), self.pointB.y())
                path.cubicTo(ctrl1_5, ctrl2_5, pt5)
                path.moveTo(pt5)

                SMALL_ARROW_WIDTH = 8

                l_arrow = self.pointB - (QPointF(self.pointB.x()-8, self.pointB.y()))
                path.moveTo(QPointF(self.pointB.x()-8, self.pointB.y()))
                path.lineTo(self.pointB)

                length = math.sqrt(l_arrow.x() ** 2 + l_arrow.y() ** 2)
                sita = math.atan2(l_arrow.y(), l_arrow.x())
                p1 = self.pointB - QPointF(SMALL_ARROW_WIDTH * math.cos(sita),
                                        SMALL_ARROW_WIDTH * math.sin(sita))
                p2 = p1 - QPointF(-(SMALL_ARROW_WIDTH / 2) * math.sin(sita),
                                (SMALL_ARROW_WIDTH / 2) * math.cos(sita))
                p3 = p1 + QPointF(-SMALL_ARROW_WIDTH / 2 * math.sin(sita),
                                SMALL_ARROW_WIDTH / 2 * math.cos(sita))
                path.addPolygon(QPolygonF([p2, p3, self.pointB, p2]))

                self.setPath(path)
                return

        path = QtGui.QPainterPath()
        path.moveTo(self.pointA)
        midptx = 0.5*(self.pointA.x() + self.pointB.x())
 
        ctrl1_1 = QtCore.QPointF(self.pointA.x(), self.pointA.y())
        ctrl2_1 = QtCore.QPointF(self.pointA.x(), self.pointA.y())
        pt1 = QtCore.QPointF(midptx , self.pointA.y())
        path.cubicTo(ctrl1_1, ctrl2_1, pt1) 
        path.moveTo(pt1)

        ctrl1_2 = QtCore.QPointF(midptx, self.pointB.y())
        ctrl2_2 = QtCore.QPointF(midptx, self.pointB.y())
        pt2 = QtCore.QPointF(midptx , self.pointB.y())
        path.cubicTo(ctrl1_2, ctrl2_2, pt2)
        path.moveTo(pt2)

        ctrl1_3 = QtCore.QPointF(midptx, self.pointB.y())
        ctrl2_3 = QtCore.QPointF(midptx, self.pointB.y())
        path.cubicTo(ctrl1_3, ctrl2_3, self.pointB)
        path.moveTo(self.pointB)


        SMALL_ARROW_WIDTH = 8

        l_arrow = self.pointB - (QPointF(self.pointB.x()-8, self.pointB.y()))
        path.moveTo(QPointF(self.pointB.x()-8, self.pointB.y()))
        path.lineTo(self.pointB)

        length = math.sqrt(l_arrow.x() ** 2 + l_arrow.y() ** 2)
        sita = math.atan2(l_arrow.y(), l_arrow.x())
        p1 = self.pointB - QPointF(SMALL_ARROW_WIDTH * math.cos(sita),
                                SMALL_ARROW_WIDTH * math.sin(sita))
        p2 = p1 - QPointF(-(SMALL_ARROW_WIDTH / 2) * math.sin(sita),
                          (SMALL_ARROW_WIDTH / 2) * math.cos(sita))
        p3 = p1 + QPointF(-SMALL_ARROW_WIDTH / 2 * math.sin(sita),
                          SMALL_ARROW_WIDTH / 2 * math.cos(sita))
        path.addPolygon(QPolygonF([p2, p3, self.pointB, p2]))

        self.setPath(path)

    def paint(self, painter, option, widget):
        if self.isSelected():
            painter.setPen(self.selPen)
            painter.setBrush(self.brush)
            painter.drawPath(self.path())
        else:
            painter.setPen(self.pen)
            painter.setBrush(self.brush)
            painter.drawPath(self.path())

    @property
    def pointA(self):
        return self._pointA
 
    @pointA.setter
    def pointA(self, point):
        self._pointA = point
        self.updatePath()
 
    @property
    def pointB(self):
        return self._pointB
 
    @pointB.setter
    def pointB(self, point):
        self._pointB = point
        self.updatePath()
 
    @property
    def source(self):
        return self._source
 
    @source.setter
    def source(self, widget):
        self._source = widget
 
    @property
    def target(self):
        return self._target
 
    @target.setter
    def target(self, widget):
        self._target = widget

    def __delete__(self,instance):
        del self._source
        del self._target
        del self._pointA
        del self._pointB

lst = []
socketLst = []
class NodeSocket(QtWidgets.QGraphicsItem):
    
    def __init__(self, rect, parent, upDownFlag):
        super(NodeSocket, self).__init__(parent)
        self.rect = rect
        self.upDownFlag = upDownFlag
        self.typee = 'Graphics.NodeSocket'
        self.parent=parent
        self.setAcceptHoverEvents(True)
        self.newLine=None
        self.otherLine=None
        socketLst.append(self)
        if (parent.type == 'none'):
            self.setFlag(QGraphicsItem.ItemIsMovable)
    
        # Brush.
        self.brush = QtGui.QBrush()
        self.brush.setStyle(QtCore.Qt.SolidPattern)
        self.brush.setColor(QtGui.QColor(255,255,255,0)) #  220,220,220,220
        # Pen.
        self.pen = QtGui.QPen()
        self.pen.setStyle(QtCore.Qt.SolidLine)
        self.pen.setWidth(1)
        self.pen.setColor(QtGui.QColor(255,255,255,0)) # 0,0,0,255
        # Lines.
        self.socketLines = []
        
    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(self.boundingRect())
        return path
 
    def boundingRect(self):
        return QtCore.QRectF(self.rect)
 
    def paint(self, painter, option, widget):
        
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.drawEllipse(self.rect)

    @staticmethod
    def restoreSockets(socket):
        socket.brush.setColor(QtGui.QColor(220,220,220,220)) # 255,255,255,0
        socket.pen.setColor(QtGui.QColor(0,0,0,255))
        socket.paint

    @staticmethod
    def removeSockets(socket):
        socket.brush.setColor(QtGui.QColor(255,255,255,0)) # 255,255,255,0
        socket.pen.setColor(QtGui.QColor(255,255,255,0))
        socket.paint

    def mousePressEvent(self, event):
        
        if Graphics.flag:
            cursor = QCursor( Qt.PointingHandCursor )
            QApplication.instance().setOverrideCursor(cursor)

            if self.typee == 'Graphics.NodeSocket':
                rect = self.boundingRect()
                pointA = QtCore.QPointF(rect.x() + rect.width()/2, rect.y() + rect.height()/2)
                pointA = self.mapToScene(pointA)
                pointB = self.mapToScene(event.pos())
                self.newLine = NodeLine(pointA, pointB, self.upDownFlag)
                self.socketLines.append(self.newLine)
                self.scene().addItem(self.newLine)    
            else:
                super(NodeSocket, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):

        pointB = self.mapToScene(event.pos())
        self.newLine.pointB = pointB
        if self.otherLine:
            self.otherLine.pointB=pointB
        
        super(NodeSocket, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):

        item = self.scene().itemAt(event.scenePos().toPoint(),QtGui.QTransform())
        item.otherLine=self.newLine
      
        if self.typee == item.typee:
            self.newLine.source = self
            self.newLine.target = item
            item.socketLines.append(self.newLine)
            self.newLine.pointB = item.getCenter()

            self.brush.setColor(QtGui.QColor(255,255,255,0)) 
            self.pen.setColor(QtGui.QColor(255,255,255,0))
            self.paint
            item.brush.setColor(QtGui.QColor(255,255,255,0))
            item.pen.setColor(QtGui.QColor(255,255,255,0))
            item.paint

            lst.append((self.newLine, self, item))
        else:
            self.scene().removeItem(self.newLine)
            if(self.newLine in self.socketLines):
                self.socketLines.remove(self.newLine)
            
            del self.newLine
            super(NodeSocket, self).mouseReleaseEvent(event) 

    def hoverEnterEvent(self, event):
        if Graphics.flag:
            cursor = QCursor( Qt.CrossCursor )
            QApplication.instance().setOverrideCursor(cursor)
    
    def hoverLeaveEvent(self, event):
        if Graphics.flag:
            cursor = QCursor( Qt.ArrowCursor )
            QApplication.instance().setOverrideCursor(cursor)

    def getCenter(self):
        rect = self.boundingRect()
        center = QtCore.QPointF(rect.x() + rect.width()/2, rect.y() + rect.height()/2)
        center = self.mapToScene(center)
        return center

class NodeItem(QtWidgets.QGraphicsItem):

    pos = QPointF(0,0)

    def __init__(self,unitOpType, graphicsView):
        super(NodeItem, self).__init__()

        self.name = None
        self.type = unitOpType
        self.typee = 'Graphics.NodeItem'
        self.graphicsView = graphicsView
                
        #self.svg = QGraphicsSvgItem("svg/"+self.type+".svg")
        self.pic = QtGui.QPixmap("unitOp/type1/"+self.type+".png")
        #self.pic = QtGui.QPixmap("icons/"+self.type+".png")
        self.rect = QtCore.QRect(0,0,self.pic.width()*1,self.pic.height()*1)

        self.text = QGraphicsTextItem(self)
        f = QFont()
        f.setPointSize(8)
        self.text.setFont(f)
        self.text.setDefaultTextColor(QtGui.QColor(73,36,73,255))
        self.text.setParentItem(self)
        self.text.setPos(self.rect.width()-(self.rect.width()*0.85), self.rect.height())
        self.text.setPlainText(self.name) 
        
        self.setFlag(QtWidgets.QGraphicsPixmapItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsPixmapItem.ItemIsSelectable)
        self.initUi()
    
        # Brush
        self.brush = QtGui.QBrush()
        self.brush.setStyle(QtCore.Qt.SolidPattern)
        self.brush.setColor(QtGui.QColor(80,0,90,255))
        # Pen.
        self.pen = QtGui.QPen()
        self.pen.setStyle(QtCore.Qt.SolidLine)
        self.pen.setWidth(2)
        self.pen.setColor(QtGui.QColor(20,20,20,255))
    
        self.selPen = QtGui.QPen()
        self.selPen.setStyle(QtCore.Qt.SolidLine)
        self.selPen.setWidth(2)
        self.selPen.setColor(QtGui.QColor(222,192,222))

        if self.isUnderMouse:
            for socket in self.Sockets:
                socket.brush.setColor(QtGui.QColor(220,220,220,220)) 
                socket.pen.setColor(QtGui.QColor(0,0,0,255))
                socket.paint
        else:
            for socket in self.Sockets:
                socket.brush.setColor(QtGui.QColor(255,255,255,0)) 
                socket.pen.setColor(QtGui.QColor(255,255,255,0))
                socket.paint

    def initUi(self):
        if (self.type == 'none1'):
            #pass
            self.Sockets = [
                NodeSocket(QtCore.QRect(self.rect.height()/2, self.rect.height()/2, 4, 4), self, False)]
        elif (self.type == 'none'):
            self.Sockets = []
        else:
            self.Sockets = [
                NodeSocket(QtCore.QRect(-3,(self.rect.height()/2)-2, 4, 4), self, False),
                NodeSocket(QtCore.QRect(-3,-3, 4, 4), self, False),
                NodeSocket(QtCore.QRect(-3,self.rect.height(), 4, 4), self, False),

                NodeSocket(QtCore.QRect(self.rect.width()/2,-5, 4, 4), self, True),
                NodeSocket(QtCore.QRect(self.rect.width()/2,self.rect.height(),  4, 4), self, True),

                NodeSocket(QtCore.QRect(self.rect.width()-3,-3,  4, 4), self, False),
                NodeSocket(QtCore.QRect(self.rect.width()-3,self.rect.height(),  4, 4), self, False),
                NodeSocket(QtCore.QRect(self.rect.width()-3,(self.rect.height()/2)-2, 4, 4), self, False)
            ]

    def shape(self):
        path = QtGui.QPainterPath()
        path.addRect(self.boundingRect())
        return path
 
    def boundingRect(self):
        return QtCore.QRectF(self.rect)
 
    def paint(self, painter, option, widget):
        if self.isSelected():
            painter.setPen(self.selPen)
            painter.drawRect(QtCore.QRectF(self.rect))
        else:
            painter.setPen(self.pen)
        painter.drawPixmap(self.rect,self.pic)


    def mouseMoveEvent(self, event):
        super(NodeItem, self).mouseMoveEvent(event)

        for socket in self.Sockets:
            for line in socket.socketLines:
                line.pointA = line.source.getCenter()
                line.pointB = line.target.getCenter()      
        NodeItem.pos = event.scenePos()
    
              
                
    def mouseDoubleClickEvent(self, event):
        if Graphics.flag:
            text, ok = QInputDialog().getText(self.graphicsView, "Name Setter",
                                        "Enter name :", QLineEdit.Normal,
                                        QDir().home().dirName())
            if ok and text:
                self.name = text
                self.text.setPlainText(self.name)
      
    def hoverEnterEvent(self, event):
        for socket in self.Sockets:
            socket.brush.setColor(QtGui.QColor(220,220,220,220)) 
            socket.pen.setColor(QtGui.QColor(0,0,0,255))
            socket.paint
    
    def hoverLeaveEvent(self, event):
        for socket in self.Sockets:
            socket.brush.setColor(QtGui.QColor(255,255,255,0)) 
            socket.pen.setColor(QtGui.QColor(255,255,255,0))
            socket.paint
        
def findMainWindow(self):
    '''
        Global function to find the (open) QMainWindow in application
    ''' 
    app = QApplication.instance()
    for widget in app.topLevelWidgets():
        if isinstance(widget, QMainWindow):
            return widget
    return None

class TextItem(QGraphicsTextItem):

    def __init__(self,  graphicsView):
        super(TextItem, self).__init__()

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setDefaultTextColor(QColor(0, 0, 0, 225))
        self.graphicsView = graphicsView
        text, ok = QInputDialog().getText(self.graphicsView, "Text",
                                        "Enter text :", QLineEdit.Normal,
                                        QDir().home().dirName())
        if ok and text:
            self.name = text
            self.setPlainText(self.name)

class NumberItem(QGraphicsItem):
    def __init__(self, graphicsView):
        super(NumberItem, self).__init__()
        
        self.pic = QtGui.QPixmap("icons/circle.png")
        self.rect = QtCore.QRect(0,0,self.pic.width(),self.pic.height())
        #self.rect = QtCore.QRect(0,0,20,20)
        #self.number = number
        self.graphicsView = graphicsView
        self.text = QGraphicsTextItem(self)
        f = QFont()
        f.setPointSize(10)
        self.text.setFont(f)
        self.text.setDefaultTextColor(QtGui.QColor(255,255,255,255))
        text, ok = QInputDialog().getText(self.graphicsView, "Text",
                                        "Enter text :", QLineEdit.Normal,
                                        QDir().home().dirName())
        if ok and text:
            self.name = text
            self.text.setPlainText(self.name)
                
                
        self.text.setParentItem(self)

        if len(self.name) == 2:
            self.text.setPos(self.rect.width()/2-11, self.rect.height()/2-13)
        else:
            self.text.setPos(self.rect.width()/2-9, self.rect.height()/2-13)
        
        self.setFlag(QtWidgets.QGraphicsPixmapItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsPixmapItem.ItemIsSelectable)

    
        # Brush
        self.brush = QtGui.QBrush()
        self.brush.setStyle(QtCore.Qt.SolidPattern)
        self.brush.setColor(QtGui.QColor(80,0,90,255))

    def shape(self):
        path = QtGui.QPainterPath()
        path.addRect(self.boundingRect())
        return path
 
    def boundingRect(self):
        return QtCore.QRectF(self.rect)
 
    def paint(self, painter, option, widget):
        painter.setBrush(self.brush)
        painter.drawPixmap(self.rect,self.pic)



