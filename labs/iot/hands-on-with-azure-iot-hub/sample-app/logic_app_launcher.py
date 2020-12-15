import requests

api_endpoint='https://prod-187.westeurope.logic.azure.com:443/workflows/fe1232f214a2848e68ee7826f47052568/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=UHBMqIGgoOJ7GdHiT3qKUCfQfDTQdoQyPcda1KZH1ug'

headers = {'Content-type': 'application/json'}
post_json={}

post_json=["to_address"] = "pepe.perez@gmail.com"
post_json=["subject_text"] = "testing email"
post_json=["body"] = "hello my friend"



response = requests.post(api_endpoint, json = post_json, headers=headers)
print(response)

