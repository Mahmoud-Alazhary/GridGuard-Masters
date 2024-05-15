from predictions import predictor
from time_stamps import *
from power_exception import PowerException as PE
from common_imports import *
import pandas as pd


class PowerPredictor():
    '''Class to wrap lower-level modules to provide more and simple calculations
        and continous predictions
        provides a queue-like structure based on numpy array of shape (1 7 24)
        __frame numpy array of shape (24 7 1) representing 24 hrs * 7 varaibles
    '''
    frame_input_variables = ['Load', 'Pressure_kpa',
                             'Cloud Cover(%)', 'Humidity(%)', 'Temperature(C)', 'Wind direction(deg)', 'Wind Speed(kmh)']
    __frame_size = 24
    __in_variables_size = len(frame_input_variables)

    def __init__(self, starting_time: str = "2019/1/5 14"):
        '''starting_time string format "%Y/%m/%d %H" e.g:"2019/12/29 23"'''
        self.__predictor = predictor()
        # self.__frame=self.__predictor.get_initial_frame().transpose()

        # left pointer timestamp,of last hour
        self.__r_ts = TIME_STAMP(starting_time)
        self.__l_ts = TIME_STAMP(starting_time)
        # right pointer timestamp of first hour in frame
        self.__l_ts.remove_hours(self.__frame_size-1)
        self.__actual_row = 15806
        self.__actual_file = pd.read_excel(
            "D:/programming/GridMasters/GridGuard-Masters/Files/Actuals.xlsx")
        self.__frame = self.__actual_file.iloc[15783:15806+1, 1:]
        self.__frame = self.__frame.to_numpy(dtype=float).reshape(24, 7, 1)

    def get_next_hour_load(self):
        res = self.__predictor.predict_next_hour_load(self.__frame.transpose())
        return res

    def get_next_hour_inputs(self):
        res = self.__predictor.predict_next_hour_inputs(
            self.__frame.transpose())
        return res

    def get_next_cell(self):
        load = self.get_next_hour_load()
        self.__actual_row += 1
        new_inputs = self.__actual_file.iloc[self.__actual_row][1:].to_numpy(
            dtype=float).reshape(7, 1)
        actual_load = new_inputs[0][0]

        # write new_inputs to the end of the frame ,maintaining its size
        self.__frame = np.append(
            self.__frame, new_inputs.reshape((1, 7, 1)), axis=0)
        self.__frame = self.__frame[1:, :, :]
        # print(self.__frame.shape)
        # print(self.__frame[self.__frame_size-1],'||',np.expand_dims(new_inputs, axis=-1))
        # update l,r ts pointers
        self.__r_ts.add_hours(1)
        self.__l_ts.add_hours(1)
        # build result

        new_inputs[0][0] = load[0]  # highet accuracy
        return (self.__r_ts, self.build_cell(new_inputs), actual_load)

    def print_pointers(self):
        print(self.__l_ts, 'to', self.__r_ts)

    def build_cell(self, cell_data):
        '''build more beautiful output cell , gotta think of better name soon'''

        res = {}
        for i in range(self.__in_variables_size):
            res.update({self.frame_input_variables[i]: cell_data[i][0]})
        return res

    def get_r_datetime(self):
        return self.__r_ts.get_datetime()


def build_heat_array(data: list) -> list:
    '''Builds array of (24 hrs,(number of days)dates) '''

    days_num = int(len(data)/24)
    result_arr = [[]*days_num]*24
    # print(result_arr)
    for i in range(len(data)):
        if i//24 >= days_num:
            break

        result_arr[i % 24].append(data[i])
    print(result_arr)
    return result_arr


def plot_heat_array(start_date, data, offset=1, color_scale='Reds'):
    import plotly.graph_objects as go
    arr = build_heat_array(data)
    hours = [str((start_date.hour+i) % 24) for i in range(1, 25)]
    zako = start_date+datetime.timedelta(hours=1)
    dates = zako+np.arange(len(data)//24)*datetime.timedelta(days=1)
    fig = go.Figure(data=go.Heatmap(
        z=arr,
        x=dates,
        y=hours,
        colorscale=color_scale))

    fig.update_layout(
        title='Predicted Load Demand in Mw',
        xaxis_nticks=36)

    fig.show()


if __name__ == '__main__':
    wizard = PowerPredictor()
    from pprint import pprint

    start_date = wizard.get_r_datetime()

    lst = []
    for i in range(48):

        # get next
        res = wizard.get_next_cell()

        lst.append(res[1]['Load'])
    res = build_heat_array(lst)
    print(len(res))
    # pprint(res)
    # plot_heat_array(start_date,lst)
