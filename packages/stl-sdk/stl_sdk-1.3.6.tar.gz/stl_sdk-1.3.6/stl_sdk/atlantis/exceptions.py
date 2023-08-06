from stl_sdk.exceptions import CoreHttpError


class InvalidTokenError(RuntimeError):
    pass


class AtlantisClientHTTPError(CoreHttpError):
    pass
