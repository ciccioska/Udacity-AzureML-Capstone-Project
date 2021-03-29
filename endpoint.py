import requests
import json

# URL for the web service, should be similar to:
# 'http://8530a665-66f3-49c8-a953-b82a2d312917.eastus.azurecontainer.io/score'
scoring_uri = 'http://localhost:9000/score'#'http://7c8b9eee-fd6f-42da-81df-3f422e6bac5d.eastus.azurecontainer.io/score'
# If the service is authenticated, set the key or token
key = ''

# Two sets of data to score, so we get two results back
data = {"data":
        [
          {
            'id': "0",
            'gender': "0",
            'age': "0",
            'hypertension': "0",
            'heart_disease': "0",
            'ever_married': False,
            'work_type': "0",
            'Residence_type': "0",
            'avg_glucose_level': "0",
            'bmi': "0",
            'smoking_status': "0",
        },
      ]
    }
# Convert to JSON string
input_data = json.dumps(data)
with open("data.json", "w") as _f:
    _f.write(input_data)

# Set the content type
headers = {'Content-Type': 'application/json'}
# If authentication is enabled, set the authorization header
headers['Authorization'] = f'Bearer {key}'

# Make the request and display the response
resp = requests.post(scoring_uri, input_data, headers=headers)
print(resp.json())


