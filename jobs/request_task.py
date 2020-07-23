import requests


class Requesttask:
    def __init__(self, url):
        self.__url = url

    def run(self):
        r = requests.get(self.__url)
        if r.status_code != 200:
            print('Call with {} failed with status {} and content {}'.format(self.__url, r.status_code, r.text))
            exit(1)
        print('Task {} completed'.format(self.__url))
        exit(0)
