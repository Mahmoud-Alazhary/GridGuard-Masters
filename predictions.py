
class predictor:
    def __init__(self):
        # Scaled inputs for the last 24 hours
        self.__last24_frame = np.zeros((1,7,24))
        self.__last24_frame[0] = np.load(os.getcwd() + r'\Models\last24hours.npy')
        
        # Load models
        self.__model1 = keras.models.load_model(os.getcwd() + '\\Models\\model1.keras')
        self.__model2 = keras.models.load_model(os.getcwd() + '\\Models\\model2.keras')
        self.__model3 = keras.models.load_model(os.getcwd() + '\\Models\\model3.keras')

        # Load scalers
        self.__scalers = []
        for file in os.listdir(os.getcwd() + '\\Models\\Scalers'):
                self.__scalers.append(joblib.load(os.getcwd() + '\\Models\\Scalers\\' + file))

    '''
    #predict: method to predict the loads
    # model_number: 1,2 or 3
    # inputs: np.array inputs according to the model_number:
    # shape -> (None, 7, 24)
    # return: a np.array of outputs of the model according to the model_number:
    # model1 -> the next hour load -> (None, 1)
    # model2 -> the next 24 hours loads -> (None, 24)
    # model3 -> the next hour inputs -> (None, 7)
    '''
    def predict(self,model_number:int, inputs):
            for j in range(inputs.shape[0]):
                    for i in range(7):
                            inputs[j][i] = self.__scalers[i].transform(inputs[j][i].reshape(-1, 1)).reshape(inputs.shape[2])
            if (model_number == 1):
                    return self.__scalers[0].inverse_transform(self.__model1.predict(inputs))
            elif (model_number == 2):
                    return self.__scalers[0].inverse_transform(self.__model2.predict(inputs))
            elif (model_number == 3):
                    predicted = self.__model3.predict(inputs).transpose()
                    for i in range(7):
                            predicted[i] = self.__scalers[i].inverse_transform(predicted[i].reshape(-1, 1)).reshape(predicted.shape[1])
                    return predicted.transpose()
    
    def predict_next_hour_load(self,inputs):
        '''Predicts the Next Hour Load according to given last 24 inputs=>shape:(1 7 24)
            returns np array of shape(1) float32 load value
        '''
        return self.predict(1,inputs)[0]
    
    def predict_next_hour_inputs(self,inputs):
        '''Predicts the Next Hour input variables according to given last 24 inputs=>shape:(1 7 24)
            returns float32 (7) inputs np array
        '''
        return self.predict(3,inputs)
    
    def get_initial_frame(self):
        return self.__last24_frame

if __name__=='__main__':
    from tensorflow import keras # ML platform
    import numpy as np # linear algebra
    import os # operating system
    import joblib # save and load preprocessing scalers

    wizard=predictor()
    frame=wizard.get_initial_frame()
    
    
