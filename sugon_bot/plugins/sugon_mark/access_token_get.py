import requests

access_token = ' '


def job():
    url = 'https://bots.qq.com/app/getAppAccessToken'
    headers = {'Content-Type': 'application/json'}
    data = {
        "appId": "102080600",
        "clientSecret": "RsJkBc3UvNpHjBd5XzSvOrKnGjDhBf9d"
    }
    response = requests.post(url, headers=headers, json=data)
    token = response.json()['access_token']
    return token


def get_access_token():
    global access_token
    access_token = job()
