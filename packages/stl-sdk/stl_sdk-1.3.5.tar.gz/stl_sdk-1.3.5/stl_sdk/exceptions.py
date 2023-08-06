from requests.exceptions import HTTPError


class CoreHttpError(HTTPError):
    def __init__(self, error):
        self.message = '{}: {}'.format(error.response.status_code, error.response.text)
        self.response = error.response

    def __str__(self):
        return self.message
