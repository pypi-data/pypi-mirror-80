import requests
import json

def get_information(data, product, verify_ssl):
    js = json.dumps(data, ensure_ascii=False)
    url = 'https://service.zipcode.com.br/api/'+product

    # call get service with headers and params
    response = requests.post(url, data=js, headers={"Content-Type": "application/json"},verify=verify_ssl)
    ret = response.json()
    return ret


