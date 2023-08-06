from functools import wraps
from stl_sdk.atlantis.exceptions import AtlantisClientHTTPError


def retry(method):
    """Renova as configurações do openid caso o endpoint retorne 404 e refaz a chamada

    Isso é necessário quando o Atlantis altera o endereço de algum endpoint
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except AtlantisClientHTTPError as error:
            if error.response.status_code == 404:
                self._set_openid_configuration()
                return method(self, *args, **kwargs)
            raise error

    return wrapper
