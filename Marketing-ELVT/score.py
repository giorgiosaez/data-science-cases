
import pickle
import json
import numpy as np
import pandas as pd
from azureml.core.model import Model
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import MinMaxScaler

MODEL = 'model'

def init():
    # read in the model file
    global model
    global normalization_dict

    model_path = Model.get_model_path(model_name = MODEL)
    
    # load model
    with open(MODEL_FILE, 'rb') as handle:
        model = pickle.load(handle)
    print("Model Loaded")
    
    # Load normalization values
    with open(NORMALIZATION_DICT, 'rb') as handle:
        normalization_dict = pickle.load(handle)
    print('Loaded')
        
def run(raw_data):
    try:
        data = json.loads(raw_data)['data']
        data = pd.read_json(data, orient='records')
        
        for column in normalization_dict:
            normalization_dict[column].fit_transform(data[column].values)
            name = data[column].name
            dfOneHot = pd.DataFrame(transformed, 
                                    columns =[name+"_"+str(list(set(data[column].values))[i]) for i in range(transformed.shape[1])])
            data = pd.concat([data, dfOneHot], axis=1)

        pred = model.predict(data)
        print(pred)
        
        # Send results
        pred = pred.as_data_frame().values.tolist()
        return json.dumps({"result": pred})

    except Exception as e:
        result = str(e)
        return json.dumps({"error": result})