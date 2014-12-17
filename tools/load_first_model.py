import requests
import json

from codecs import open

original_file_name = 'normalized_15.json'


with open(original_file_name) as f:
	model_data = json.load(f)

cl_model = model_data.get('data')
cl_model['description'] = 'ng models'

res = requests.post('http://localhost:8000/models/', data={'data': json.dumps(cl_model), 'name': 'Protezionismo'})
print res.status_code
print res.content
