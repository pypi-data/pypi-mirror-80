import requests
import json
#http://pythonclub.com.br/como-distribuir-sua-aplicacao-python-com-pypi.html
#https://packaging.python.org/tutorials/packaging-projects/#create-an-account

data = {
    "Token": "",
    "CPF": "01234567890"
}

js = json.dumps(data, ensure_ascii=False)
url = 'https://service.zipcode.com.br/api/PF/ConsultaPerfil3D'

# call get service with headers and params
response = requests.post(url, data=js, headers={"Content-Type": "application/json"},verify=False)
ret = response.json()



