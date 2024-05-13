

from hmd_ui import *

from math import sin
from threads import *
from time import sleep
from power_wizard import *
from PyQt6.QtWidgets import QApplication

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
        self.__init_plot()
        
        #self.init_ui_signals()
    
    def __init_plot(self):
        '''Initializes the Load live predictions Widget'''
        print(1)
        live_plot=self.__ui.live_load_plot_widget
        live_plot.x_range_controller.crop_left_offset_to_data = True
        print(2)
        plot_curve = LiveLinePlot()
        plot_curve.set_leading_line(LeadingLine.VERTICAL, pen=mkPen("red"), text_axis=LeadingLine.AXIS_Y)
        live_plot.addItem(plot_curve)
        # DataConnector holding 6000 points and plots @ 100Hz
        self.__plot_data_connector = DataConnector(plot_curve, max_points=6000, update_rate=100)
        self.__data_thread=PredictionDataThread(connector=self.__plot_data_connector,cool_down=1)
        self.__data_thread.start()
    '''
    def init_ui_signals(self):
        self.ui.assembleBtn.clicked.connect(self._assemble_clicked)
        self.ui.simulateBtn.clicked.connect(self._simulate_clicked)
        self.ui.codeEditor.textChanged.connect(self._code_changed)
    def _assemble_clicked(self):
        print('Assemble button clicked!')
        self.ui.hex_PText.clear()
        self.ui.mc_PText.clear()
        mar=self.ui.codeEditor.toPlainText()#marie assembly code
        print('zz')
        try:
            self.mobj=self.engine.assemble(mar)
            
            self.ui.hex_PText.appendPlainText(self.mobj.to_hexstring())
            self.ui.mc_PText.appendPlainText(self.mobj.to_binarystring())
        except Exception as ex:
            self.alert(str(ex))
    '''
    def closeEvent(self, event):
        self.__data_thread.stop()
        

if __name__=='__main__':
    app = QtWidgets.QApplication([])
    
    MainWindow = MainEditorWindow()
    
    MainWindow.showMaximized()    
    app.exec()
 