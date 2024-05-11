from predictions import predictor
from time_stamps import *
from power_exception import PowerException as PE
from common_imports import *
class PowerPredictor():
    '''Class to wrap lower-level modules to provide more and simple calculations
        and continous predictions
        provides a queue-like structure based on numpy array of shape (1 7 24)
        __frame numpy array of shape (24 7 1) representing 24 hrs * 7 varaibles
    '''
    frame_input_variables=['Load','Pressure_kpa','Cloud Cover(%)','Humidity(%)'
                                ,'Temperature(C)','Wind direction(deg)','Wind Speed(kmh)']
    __frame_size=24
    __in_variables_size=len(frame_input_variables)
    def __init__(self,starting_time:str = "2019/12/29 23"):
        '''starting_time string format "%Y/%m/%d %H" e.g:"2019/12/29 23"'''
        self.__predictor=predictor()
        self.__frame=self.__predictor.get_initial_frame().transpose()
        self.__r_ts=TIME_STAMP(starting_time)#left pointer timestamp,of last hour
        self.__l_ts=TIME_STAMP(starting_time)
        self.__l_ts.remove_hours(self.__frame_size-1)#right pointer timestamp of first hour in frame
    def get_next_hour_load(self):
        res=self.__predictor.predict_next_hour_load(self.__frame.transpose())
        return res
    def get_next_hour_inputs(self):
        res=self.__predictor.predict_next_hour_inputs(self.__frame.transpose())
        return res
    def get_next_cell(self):
        load=self.get_next_hour_load()
        new_inputs=self.get_next_hour_inputs()
       
        
        #write new_inputs to the end of the frame ,maintaining its size
        self.__frame=np.append(self.__frame,new_inputs.reshape((1,7,1)),axis=0)
        self.__frame=self.__frame[1:,:,:]
        #print(self.__frame.shape)
        #print(self.__frame[self.__frame_size-1],'||',np.expand_dims(new_inputs, axis=-1))
        #update l,r ts pointers
        self.__r_ts.add_hours(1)
        self.__l_ts.add_hours(1)
        #build result
        
        new_inputs[0][0]=load[0]#highet accuracy
        return (self.__r_ts,self.build_cell(new_inputs))
    def print_pointers(self):
        print(self.__l_ts,'to',self.__r_ts)
        
    def build_cell(self,cell_data):
        '''build more beautiful output cell , gotta think of better name soon'''
        
        res={}
        for i in range(self.__in_variables_size):
            res.update({self.frame_input_variables[i]:cell_data[0][i]})
        return res
if __name__=='__main__':
    wizard=PowerPredictor()
    #show current left,right pointers ,for testing..
    
    lst=[]
    for i in range(100):
        
        #get next
        res=wizard.get_next_cell()
        
        lst.append(res[1]['Load'])
    print(lst)
    