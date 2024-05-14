

from hmd_ui import *


from threads import *
from time import sleep
from power_wizard import *
from PyQt6.QtWidgets import QApplication
from PyQt6 import QtCore
from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget
#from pglive.sources.live_axis_range import LiveAxisRange
from pglive.kwargs import LeadingLine
from pyqtgraph import mkPen

class MainEditorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.__ui=Ui_MainWindow()
        self.__ui.setupUi(self)
        self.__init_ui_signals()
        self.__init_plot()
        
        #self.init_ui_signals()
    
    def __init_plot(self):
        '''Initializes the Load live predictions Widget'''
        
        live_plot=self.__ui.live_load_plot_widget
        live_plot.x_range_controller.crop_left_offset_to_data = True
        
        plot_curve = LiveLinePlot()
        plot_curve.set_leading_line(LeadingLine.VERTICAL, pen=mkPen("red"), text_axis=LeadingLine.AXIS_Y)
        live_plot.addItem(plot_curve)
        # DataConnector holding 6000 points and plots @ 100Hz
        self.__plot_data_connector = DataConnector(plot_curve, max_points=6000, update_rate=100)
        self.__data_thread=PredictionDataThread(connector=self.__plot_data_connector,cool_down=0.1)
        self.__data_thread.predicted_p.connect(self.on_data_recieved)
        self.__data_thread.start()
    
    def __init_ui_signals(self):
        self.__ui.pushButton_9.clicked.connect(self.__resume_plotting)
        self.__ui.pushButton_8.clicked.connect(self.__pause_plotting)
        self.__ui.heatmap_button.clicked.connect(self.__do_heatmap)
    def __do_heatmap(self):
        self.__data_thread.do_heat_map()
    def __resume_plotting(self):
        self.__data_thread.resume()
    def __pause_plotting(self):
        self.__data_thread.pause()
    @QtCore.pyqtSlot(tuple)
    def on_data_recieved(self,data):
        predicted,actual=data
        err=100*abs(predicted-actual)/actual
        self.__ui.label_10.setText(str(round(actual,3))+" Kw")
        self.__ui.label_12.setText(str(round(err,2))+" %")
    def closeEvent(self, event):
        self.__data_thread.stop()
        

if __name__=='__main__':
    app = QtWidgets.QApplication([])
    
    MainWindow = MainEditorWindow()
    
    MainWindow.showMaximized()    
    app.exec()
 