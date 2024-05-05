import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtCore, QtWidgets
import sys


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Create the matplotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=150)

        # Provided data
        data = {
            '2019/12/29 00': {'Load': 970.8093, 'Pressure_kpa': 341.60632, 'Cloud Cover(%)': -16.817415, 'Humidity(%)': -56.48735, 'Temperature(C)': 67.30821, 'Wind direction(deg)': 1097340.1, 'Wind Speed(kmh)': -14.656398},
            '2019/12/29 01': {'Load': 1077.8792, 'Pressure_kpa': 634.65344, 'Cloud Cover(%)': -27.12311, 'Humidity(%)': -22.622688, 'Temperature(C)': 79.40017, 'Wind direction(deg)': 1024685.9, 'Wind Speed(kmh)': -21.647018},
            '2019/12/29 02': {'Load': 1079.0724, 'Pressure_kpa': 634.3416, 'Cloud Cover(%)': -27.13038, 'Humidity(%)': -22.493174, 'Temperature(C)': 79.38534, 'Wind direction(deg)': 1024618.5, 'Wind Speed(kmh)': -21.61045},
            '2019/12/29 03': {'Load': 1079.071, 'Pressure_kpa': 634.34143, 'Cloud Cover(%)': -27.130392, 'Humidity(%)': -22.493124, 'Temperature(C)': 79.38534, 'Wind direction(deg)': 1024617.75, 'Wind Speed(kmh)': -21.610365},
            '2019/12/29 04': {'Load': 1079.071, 'Pressure_kpa': 634.34143, 'Cloud Cover(%)': -27.130388, 'Humidity(%)': -22.49312, 'Temperature(C)': 79.38533, 'Wind direction(deg)': 1024617.75, 'Wind Speed(kmh)': -21.610365},
            '2019/12/29 05': {'Load': 1079.071, 'Pressure_kpa': 634.34143, 'Cloud Cover(%)': -27.130388, 'Humidity(%)': -22.49312, 'Temperature(C)': 79.38533, 'Wind direction(deg)': 1024617.75, 'Wind Speed(kmh)': -21.610365},
            '2019/12/29 06': {'Load': 1079.071, 'Pressure_kpa': 634.34143, 'Cloud Cover(%)': -27.130388, 'Humidity(%)': -22.49312, 'Temperature(C)': 79.38533, 'Wind direction(deg)': 1024617.75, 'Wind Speed(kmh)': -21.610365},
            '2019/12/29 07': {'Load': 1079.071, 'Pressure_kpa': 634.34143, 'Cloud Cover(%)': -27.130388, 'Humidity(%)': -22.49312, 'Temperature(C)': 79.38533, 'Wind direction(deg)': 1024617.75, 'Wind Speed(kmh)': -21.610365},
            '2019/12/29 08': {'Load': 1079.071, 'Pressure_kpa': 634.34143, 'Cloud Cover(%)': -27.130388, 'Humidity(%)': -22.49312, 'Temperature(C)': 79.38533, 'Wind direction(deg)': 1024617.75, 'Wind Speed(kmh)': -21.610365}
        }

        # Extract time and keys from the dictionary
        times = list(data.keys())
        # Assuming all dictionaries in data have the same keys
        keys = list(data[times[0]].keys())

        # Create pandas DataFrame for Load, Pressure, and Temperature
        df_load = pd.DataFrame(index=times, columns=['Load'])
        df_pressure = pd.DataFrame(index=times, columns=['Pressure_kpa'])
        df_Cloud_Cover = pd.DataFrame(index=times, columns=['Cloud Cover(%)'])
        df_Humidity = pd.DataFrame(index=times, columns=['Humidity(%)'])
        df_temperature = pd.DataFrame(index=times, columns=['Temperature(C)'])
        df_Wind_direction = pd.DataFrame(
            index=times, columns=['Wind direction(deg)'])
        df_Wind_Speed = pd.DataFrame(index=times, columns=['Wind Speed(kmh)'])
        for time in times:
            df_load.loc[time] = data[time]['Load']
            df_pressure.loc[time] = data[time]['Pressure_kpa']
            df_Cloud_Cover.loc[time] = data[time]['Cloud Cover(%)']
            df_Humidity.loc[time] = data[time]['Humidity(%)']
            df_temperature.loc[time] = data[time]['Temperature(C)']
            df_Wind_direction.loc[time] = data[time]['Wind direction(deg)']
            df_Wind_Speed.loc[time] = data[time]['Wind Speed(kmh)']

        # Plot Load data initially
        current_data = df_load
        current_data.plot(ax=sc.axes, label='Load')

        # Add remaining data to the legend without plotting
        for key in keys:
            if key != 'Load':
                sc.axes.plot([], [], label=key)

        # Set x-axis label
        sc.axes.set_xlabel('Time')

        # Set title
        sc.axes.set_title('Load vs Time')

        # Add legend to the plot
        sc.axes.legend()

        # Create dropdown menu for selecting data type
        dropdown = QtWidgets.QComboBox()
        dropdown.addItems(
            ['Load', 'Pressure', 'Cloud Cover', 'Humidity', 'Temperature', 'Wind direction', 'Wind Speed'])

        # Function to update plot when dropdown item is changed
        def update_plot(index):
            nonlocal current_data
            sc.axes.clear()
            if index == 0:
                current_data = df_load
            elif index == 1:
                current_data = df_pressure
            elif index == 2:
                current_data = df_Cloud_Cover
            elif index == 3:
                current_data = df_Humidity
            elif index == 4:
                current_data = df_temperature
            elif index == 5:
                current_data = df_Wind_direction
            else:
                current_data = df_Wind_Speed
            current_data.plot(ax=sc.axes, label=dropdown.currentText())
            for key in keys:
                if key != dropdown.currentText():
                    sc.axes.plot([], [], label=key)
            sc.axes.set_xlabel('Time')
            sc.axes.set_ylabel('{}'.format(dropdown.currentText()))
            sc.axes.set_title('{} vs Time'.format(dropdown.currentText()))
            sc.axes.legend()
            sc.draw()

        dropdown.currentIndexChanged.connect(update_plot)

        # Create toolbar, passing canvas as first parameter, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(dropdown)
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
