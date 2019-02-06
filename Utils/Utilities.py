class AccessToken():
    access_token = None

    @staticmethod
    def set_access_token(token):
        AccessToken.access_token = token

    @staticmethod
    def get_access_token():
        return AccessToken.access_token
