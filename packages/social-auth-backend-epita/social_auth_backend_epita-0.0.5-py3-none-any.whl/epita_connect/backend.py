"""
Epita OpenIdConnect:
"""
from social_core.backends.open_id_connect import OpenIdConnectAuth


class EpitaOpenIdConnect(OpenIdConnectAuth):
    name = 'epita'
    OIDC_ENDPOINT = 'https://cri.epita.fr'

    def oidc_config(self):
        endpoint = self.OIDC_ENDPOINT
        return self.get_json(endpoint + '/.well-known/openid-configuration')
