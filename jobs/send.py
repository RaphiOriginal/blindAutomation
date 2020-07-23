import requests


def send(url):
    r = requests.get(url)
    if r.status_code != 200:
        print('Call with {} failed with status {} and content {}'.format(url, r.status_code, r.text))
    else:
        print('Task {} completed: {}'.format(url, r.text))
