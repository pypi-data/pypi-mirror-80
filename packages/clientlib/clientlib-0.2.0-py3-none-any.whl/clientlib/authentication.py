from requests.auth import AuthBase


class TokenAuthenticator(AuthBase):
    """Token bases authenticator

    This authenticator will add the token in the Authorization header of the
    request
    """

    def __init__(self, token, authentication_type=None):
        """Create a new TokenAuthenticator object

        :param str token: the token
        """
        self.token = token
        self.authentication_type = authentication_type

    def _create_authorization_value(self):
        if self.authentication_type is not None:
            return "{} {}".format(self.authentication_type, self.token)
        else:
            return self.token

    def __call__(self, request):
        request.headers["Authorization"] = self._create_authorization_value()

        return request


class RequestParameterAuthenticator(AuthBase):
    """Request parameter authentication

    This authenticator will put the api key in a url parameter of a request
    """

    def __init__(self, api_key, parameter_name):
        """Create a new RequestParameterAuthenticator object

        :param str api_key: the api key
        :param str parameter_name: the name of the parameter to put the key
        """
        self._api_key = api_key
        self._parameter_name = parameter_name

    def __call__(self, r):
        r.prepare_url(r.url, {self._parameter_name: self._api_key})

        return r
