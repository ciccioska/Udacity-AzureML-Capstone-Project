import json
import pandas as pd
import joblib
from azureml.core.model import Model
import os

def init():
    global model
    
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'hyper-drive-model.pkl')
    model = joblib.load(model_path)

def run(data):  
    try:
        test_data = json.loads(data)
        data_frame = pd.DataFrame(test_data['data'])
        result = model.predict(data_frame)
        return json.dumps({"result": result.tolist()})
    except Exception as e:
        error = str(e)
        return error