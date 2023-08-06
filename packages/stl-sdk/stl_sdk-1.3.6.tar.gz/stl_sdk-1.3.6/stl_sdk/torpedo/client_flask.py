from stl_sdk.torpedo.client import TorpedoClient
from stl_sdk.exceptions import InvalidInitParameters


class TorpedoClientFlask(TorpedoClient):
    """Cliente Flask para comunicação com Torpedo.
        Ao iniciar o cliente ele irá buscar as variaveis de ambiente
        `TORPEDO_URL` e `CLIENT_NAME`

    Exemplo:

        .. code-block:: python

            from stl_sdk.torpedo import TorpedoClientFlask

            torpedo = TorpedoClientFlask()

            def init_app(app):
                torpedo.init_app(app)

    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
        super().__init__()

    def init_app(self, app):
        self.torpedo_url = app.config['TORPEDO_URL']
        self.client_name = app.config['CLIENT_NAME']

        if self.client_name is None:
            raise InvalidInitParameters('Missing CLIENT_NAME on TorpedoClient initialization.')
