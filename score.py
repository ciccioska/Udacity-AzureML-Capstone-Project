import json
import numpy as np
import joblib
from azureml.core.model import Model


def init():
    global model
#    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'hyper-drive-model.joblib')
    model_path = Model.get_model_path('best-hyper-drive')
    model = joblib.load(model_path)

def run(data):  
    try:
        data = np.array(json.loads(data))
        result = model.predict(data)
        # You can return any data type, as long as it is JSON serializable.
        return result.tolist()
    except Exception as e:
        error = str(e)
        return error