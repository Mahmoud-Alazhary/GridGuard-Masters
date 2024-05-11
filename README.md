# Smart Load Forecasting System with Interactive GUI

This project is a machine learning-based system that addresses the challenge of accurately predicting electrical loads, helping energy providers and facility managers:

Improve load forecasting accuracy: Reduce energy waste and optimize grid management by predicting upcoming electrical loads for days, months, or even years.
Data-driven load insights: Gain valuable insights into future energy requirements through accurate predictions.
Interactive visualization: Explore predicted load curves through an intuitive graphical user interface (GUI).

Key Features:

Machine learning-powered load forecasting: Leverages powerful machine learning techniques to predict future electrical loads with high accuracy.
Interactive GUI:
Start/Pause/Resume buttons: Control the visualization of the predicted load curve.
Interactive graph: Point and click on any part of the curve to view the corresponding time and expected load values.
Visualization: Generates clear and informative graphs of predicted load curves.
Getting Started

This system requires Python 3.11 or higher and several libraries. We recommend using a virtual environment for managing dependencies:

Bash
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install -r requirements.txt

Usage:

Run the following command to launch the GUI:

Bash
python main.py

This will open a window with the predicted load curve displayed.

Interactive Features:

Start Button: Initiates the visualization of the predicted load curve.
Pause Button: Temporarily pauses the animation of the load curve.
Resume Button: Resumes the animation after pausing.
Interactive Graph: Clicking on any point on the graph displays the corresponding time and expected load value.
Model Details (Optional)

Model Architecture: LSTM for time series forecasting
Evaluation Metrics: We used mean squared error for accuracy

Results and Visualization

[Will add some images]

Future Enhancements

Generator Recommendation: Integrate generator capabilities with load forecasts to recommend the most efficient configuration for power generation. (This functionality is planned for a future release.)
Advanced Visualization Features: Enhance visualization options for deeper insights into predicted loads (e.g., zooming, panning).
Real-time Integration: Explore the possibility of integrating with real-time data streams for more dynamic predictions.
