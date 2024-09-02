import requests

url = 'http://aa56951c3f816722525a7.playat.flagyard.com/'

s = requests.Session()

headers = {
    'Content-Type': 'application/json'
}

def register(username: str, password: str):
    resp = s.post(url + 'register', json={
        'username': username,
        'password': password,
    }, headers=headers)
    print('REGISTER', resp.text)

def login(username: str, password: str):
    resp = s.post(url + 'login', json={
        'username': username,
        'password': password,
    }, headers=headers)
    print('LOGIN', resp.text)

def upload(name, file):
    resp = s.post(url + 'upload', files=[
        ('file', (name, file))
    ])
    print('upload', resp.text)
    return resp.json()
def read(id: int):
    resp = s.get(url + f'file/{id}')
    print(resp.text)


register('zzzz', '1234')
login('zzzz', '1234')
resp = upload('/zzzz.txt', 'zzzz')
#read(resp['file_path'])


