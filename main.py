from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from app import Ui_MainWindow
import collections
import pyqtgraph as pg
import numpy as np
import psutil
import sys


class Parsing():
    def cpu_count(self):
        self.result = psutil.cpu_count()
        return self.result
    
    def cpu_freq(self):
        self.result = psutil.cpu_freq().current
        return self.result

    def cpu_percent(self):
        self.result = psutil.cpu_percent()
        return self.result

    def memory_total(self):
        self.result = round((psutil.virtual_memory()[0])/1024/1024/1024,1)
        return self.result

    def memory_free(self):
        self.result = round((psutil.virtual_memory()[4])/1024/1024/1024,1)
        return self.result

    def memory_used(self):
        self.result = round((psutil.virtual_memory()[3])/1024/1024/1024,1)
        return self.result
    
    def memory_percent(self):
        self.result = psutil.virtual_memory()[2]
        return self.result

    def disk_usage(self):
        self.result = psutil.disk_usage('C:/')[3]
        return self.result

    def net_sent(self):
        self.result = (psutil.net_io_counters()[0])/1024/1024
        return self.result

    def net_recv(self):
        self.result = (psutil.net_io_counters()[1])/1024/1024
        return self.result


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def fill(self):
        self.data = Parsing()

        self.ui.label_cpu_percent.setNum(self.data.cpu_percent())
        self.ui.label_cpu_count.setNum(self.data.cpu_count())
        self.ui.label_cpu_freq.setNum(self.data.cpu_freq())
        self.ui.label_memory_percent.setNum(self.data.memory_percent())
        self.ui.label_memory_total.setNum(self.data.memory_total())
        self.ui.label_memory_free.setNum(self.data.memory_free())
        self.ui.label_memory_used.setNum(self.data.memory_used())
        self.ui.label_disk_usage.setNum(self.data.disk_usage())
        self.ui.label_net_sent.setNum(self.data.net_sent())
        self.ui.label_net_recv.setNum(self.data.net_recv())

    def initDraw(self):
        self.cpu_plot = self.ui.widget_cpu
        self.cpu_plot.getPlotItem().hideAxis('bottom')
        self.cpu_plot.getPlotItem().hideAxis('left')
        self.cpu_x = list(range(10))
        self.cpu_y = collections.deque(np.zeros(10))
        self.cpu_pen = pg.mkPen(color=(255, 0, 0), width=2)

        self.ram_plot = self.ui.widget_ram
        self.ram_plot.getPlotItem().hideAxis('bottom')
        self.ram_plot.getPlotItem().hideAxis('left')
        self.ram_x = list(range(10))
        self.ram_y = collections.deque(np.zeros(10))
        self.ram_pen = pg.mkPen(color=(255, 0, 0), width=2)

    def draw(self):
        self.cpu_y.popleft()
        self.cpu_y.append(self.data.cpu_percent())
        self.cpu_plot.clear()
        self.cpu_plot.showGrid(x=True, y=True)
        self.cpu_plot.setYRange(0, 200, padding=0)
        self.cpu_x = self.cpu_x[1:]
        self.cpu_x.append(self.cpu_x[-1] + 1)
        self.cpu_plot.plot(self.cpu_x, self.cpu_y, pen=self.cpu_pen)

        self.ram_y.popleft()
        self.ram_y.append(self.data.memory_percent())
        self.ram_plot.clear()
        self.ram_plot.showGrid(x=True, y=True)
        self.ram_plot.setYRange(0, 120, padding=0)
        self.ram_x = self.ram_x[1:]
        self.ram_x.append(self.ram_x[-1] + 1)
        self.ram_plot.plot(self.ram_x, self.ram_y, pen=self.ram_pen)

    def timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fill)
        self.timer.timeout.connect(self.draw)
        self.timer.start(1000)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = MyWindow()
    application.show()
 
    application.fill()
    application.initDraw()
    application.draw()
    application.timer()

    sys.exit(app.exec())