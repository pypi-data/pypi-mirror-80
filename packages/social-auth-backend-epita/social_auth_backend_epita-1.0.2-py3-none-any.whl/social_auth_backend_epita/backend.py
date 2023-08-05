from social_core.backends.open_id_connect import OpenIdConnectAuth


class EpitaOpenIdConnect(OpenIdConnectAuth):
    name = "epita"
    OIDC_ENDPOINT = "https://cri.epita.fr"
