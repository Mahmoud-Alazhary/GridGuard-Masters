import threading
import math
from power_wizard import *
import queue
import time
class PredictionDataThread(threading.Thread):
    
    def __init__(self, connector,cool_down=0.01, stop_event=None):
        
        super(PredictionDataThread, self).__init__()
        self.cool_down=cool_down
        self.connector = connector
        self._stop_event = stop_event if stop_event is not None else threading.Event()
        self.__wizard=PowerPredictor()
        #self.queue=queue.Queue(720)
    def run(self):
        """
        Generates and sends sine wave data points until the stop event is set.
        """
        print('prediction data thread starting @',time.time())
        while not self.stopped():
            data=self.__wizard.get_next_cell()
            data_point=data[1]['Load']/1000
            print(data_point,' ==')
            self.connector.cb_append_data_point(data_point, data[0].to_epoch())
            time.sleep(self.cool_down)  
        print('prediction data thread ending @',time.time())
    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


if __name__ == "__main__":
    

    thread = PredictionDataThread(connector)
    thread.start()

    
    