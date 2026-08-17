import minecraft_launcher_lib


REDIRECT_URI = "https://login.microsoftonline.com/common/oauth2/nativeclient"

DEFAULT_CLIENT_ID = "c44b4083-3bb0-49c1-b47d-974e53cbdf3c"


class MicrosoftAuth:

    def __init__(self, client_id=None):
        self.client_id = client_id or DEFAULT_CLIENT_ID

    def get_login_url(self):

        url, state, code_verifier = minecraft_launcher_lib.microsoft_account.get_secure_login_data(
            self.client_id,
            REDIRECT_URI
        )

        return url, state, code_verifier

    def complete_login(self, redirect_url, code_verifier):

        auth_code = minecraft_launcher_lib.microsoft_account.get_auth_code_from_url(
            redirect_url
        )

        return minecraft_launcher_lib.microsoft_account.complete_login(
            self.client_id,
            "",
            REDIRECT_URI,
            auth_code,
            code_verifier
        )