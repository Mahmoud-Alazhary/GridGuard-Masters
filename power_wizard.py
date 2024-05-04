from predictions import predictor
from time_stamps import *
class PowerPredictor():
    '''Class to wrap lower-level modules to provide more and simple calculations
        and continous predictions
        provides a queue-like structure based on numpy array of shape (1 7 24)
        __frame numpy array of shape (24 7 1) representing 24 hrs * 7 varaibles
    '''
    self.frame_input_variables=['Load','Pressure_kpa','Cloud Cover(%)','Humidity(%)'
                                ,'Temperature(C)','Wind direction(deg)','Wind Speed(kmh)']
    def __init__(self,starting_time:str):
        '''starting_time string format "%Y/%m/%d %H" e.g:"2019/12/29 23"'''
        self.__predictor=predictor()
        self.__frame=self.__predictor.get_initial_frame().transpose()
        self.__r_ts=TIME_STAMP(starting_time)#left pointer timestamp,of last hour
        self.__l_ts=TIME_STAMP(starting_time).remove_hours(23)#right pointer timestamp of first hour in frame

    def get_next_hour_load(self):
        self.__predictor.predict()



if __name__=='__main__':
    from tensorflow import keras # ML platform
    import numpy as np # linear algebra
    import os # operating system
    import joblib # save and load preprocessing scalers

    
    
    
