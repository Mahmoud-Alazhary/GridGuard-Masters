from tensorflow import keras # ML platform
import numpy as np # linear algebra
import os # operating system
import joblib # save and load preprocessing scalers

# Scaled inputs for the last 24 hours
__last24 = np.zeros((1,7,24))
__last24[0] = np.load(os.getcwd() + r'\Models\last24hours.npy')

# Load models
__model1 = keras.models.load_model(os.getcwd() + '\\Models\\model1.keras')
__model2 = keras.models.load_model(os.getcwd() + '\\Models\\model2.keras')
__model3 = keras.models.load_model(os.getcwd() + '\\Models\\model3.keras')

# Load scalers
__scalers = []
for file in os.listdir(os.getcwd() + '\\Models\\Scalers'):
	__scalers.append(joblib.load(os.getcwd() + '\\Models\\Scalers\\' + file))

# predict: method to predict the loads
# model_number: 1,2 or 3
# inputs: np.array inputs according to the model_number:
# shape -> (None, 7, 24)
# return: a np.array of outputs of the model according to the model_number:
# model1 -> the next hour load -> (None, 1)
# model2 -> the next 24 hours loads -> (None, 24)
# model3 -> the next hour inputs -> (None, 7)
def predict(model_number:int, inputs):
	for j in range(inputs.shape[0]):
		for i in range(7):
			inputs[j][i] = __scalers[i].transform(inputs[j][i].reshape(-1, 1)).reshape(inputs.shape[2])
	if (model_number == 1):
		return __scalers[0].inverse_transform(__model1.predict(inputs))
	if (model_number == 2):
		return __scalers[0].inverse_transform(__model2.predict(inputs))
	if (model_number == 3):
		predicted = __model3.predict(inputs).transpose()
		for i in range(7):
			predicted[i] = __scalers[i].inverse_transform(predicted[i].reshape(-1, 1)).reshape(predicted.shape[1])
		return predicted.transpose()

#Examples
# print(__last24[0].transpose())
print(predict(model_number=1, inputs=__last24))
print(predict(model_number=2, inputs=__last24))

predicted = predict(model_number=3, inputs=__last24)
print(predicted)
__last24[0,:,0:22] = __last24[0,:,1:23]
__last24[0,:,23] = predicted.reshape(7)
print(predict(model_number=3, inputs=__last24))
