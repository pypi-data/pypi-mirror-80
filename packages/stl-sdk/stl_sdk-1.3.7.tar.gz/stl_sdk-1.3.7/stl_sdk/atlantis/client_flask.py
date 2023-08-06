from stl_sdk.exceptions import InvalidInitParameters
from stl_sdk.atlantis.client import AtlantisClient


class AtlantisClientFlask(AtlantisClient):
    """Cliente Flask para comunicação com Atlantis.
        Ao iniciar o cliente ele irá buscar as variaveis de ambiente
        `ATLANTIS_URL`, `ATLANTIS_CLIENT_ID` e `ATLANTIS_CLIENT_SECRET`

    Exemplo:

        .. code-block:: python

            from stl_sdk.atlantis import AtlantisClientFlask

            atlantis = AtlantisClientFlask()

            def init_app(app):
                atlantis.init_app(app)

    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
        super().__init__()

    def init_app(self, app):
        self.atlantis_url = app.config['ATLANTIS_URL']
        self.client_id = app.config['ATLANTIS_CLIENT_ID']
        self.client_secret = app.config.get('ATLANTIS_CLIENT_SECRET')

        if self.atlantis_url is None:
            raise InvalidInitParameters('Missing ATLANTIS_URL on AtlantisClient initialization.')

        if self.client_id is None:
            raise InvalidInitParameters('Missing ATLANTIS_CLIENT_ID on AtlantisClient initialization.')
