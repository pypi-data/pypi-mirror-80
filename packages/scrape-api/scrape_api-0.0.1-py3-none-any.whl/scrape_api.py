import requests


class Scrape:
    """ This class is used to encapsulate all attributes and methods pertaining to CNN Classifiers. """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        super().__init__()

    def new_search(self, keyword):
        # data to be sent to api
        API_ENDPOINT = 'http://15.207.73.113/new_search_api'
        request_data = {'username': self.username,
                        'password': self.password,
                        'keywords': keyword,
                        'reddit': True
                        }

        # sending post request and saving response as response object
        r = requests.post(url=API_ENDPOINT, data=request_data)
        return r.json()

    def get_previous_results(self):
        # data to be sent to api
        API_ENDPOINT = 'http://15.207.73.113/pevious_search_api'
        request_data = {'username': self.username,
                        'password': self.password
                        }

        # sending post request and saving response as response object
        r = requests.post(url=API_ENDPOINT, data=request_data)
        return r.json()
