import threading
import math
from power_wizard import *
import queue
import time
from PyQt6 import QtCore


class PredictionDataThread(QtCore.QObject):
    predicted_p = QtCore.pyqtSignal(tuple)

    def __init__(self, connector, cool_down=0.01, stop_event=None, pause_event=None):

        super(PredictionDataThread, self).__init__()
        self.cool_down = cool_down
        self.connector = connector
        self.__stop_event = stop_event if stop_event is not None else threading.Event()
        self.__pause_event = stop_event if stop_event is not None else threading.Event()
        self.__wizard = PowerPredictor()
        self.__heatmap_event = threading.Event()
        # self.queue=queue.Queue(720)

    def start(self):
        threading.Thread(target=self.__run, daemon=True).start()

    def __run(self):
        """
        predicts and sends upcoming load data points until the stop event is set.
        """
        print('prediction data thread starting @', time.time())
        loads_lst = []
        strt = self.__wizard.get_r_datetime()
        while not self.stopped():
            while not self.is_running():
                time.sleep(0.1)
            data = self.__wizard.get_next_cell()
            data_point = data[1]['Load']/1000
            loads_lst.append(data_point)
            self.connector.cb_append_data_point(data_point, data[0].to_epoch())
            self.predicted_p.emit((data_point, data[2]/1000))
            if self.__heatmap_event.is_set():
                self.__heatmap_event.clear()
                plot_heat_array(strt, loads_lst)
            time.sleep(self.cool_down)
        print('prediction data thread ending @', time.time())

    def stop(self):
        self.__stop_event.set()

    def stopped(self):
        return self.__stop_event.is_set()

    def resume(self):
        self.__pause_event.clear()

    def pause(self):
        self.__pause_event.set()

    def is_running(self):
        return not self.__pause_event.is_set()

    def do_heat_map(self):
        self.__heatmap_event.set()


if __name__ == "__main__":
    PredictionDataThread(None)

    pass
