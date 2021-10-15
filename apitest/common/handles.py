import requests

def request_handle(method, url, data, headers, files):
    method = method.lower()
    if method == 'get':
        response = requests.get(url=url, params=data, headers=headers, files=files)
    if method == 'post':
        response = requests.post(url=url, data=data, headers=headers, files=files)
    return response
