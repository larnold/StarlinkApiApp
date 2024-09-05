import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

class Tokens:

    def __init__(self):
        credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url="https://starlink-key-vault.vault.azure.net", credential=credential)

    def read(self):
        token = {
            "access_token": self.client.get_secret("starlink-access-token").value,
            "refresh_token": self.client.get_secret("starlink-refresh-token").value
        }

        return token

    def write(self, access_token, refresh_token):
        self.client.set_secret("starlink-access-token", access_token)
        self.client.set_secret("starlink-refresh-token", refresh_token)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }


