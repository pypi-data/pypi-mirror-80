import os

import hvac


def init_client():
    vault_url = os.getenv('VAULT_URL')
    vault_auth_token = os.getenv('VAULT_AUTH_TOKEN')
    client = hvac.Client(
        url=vault_url,
        token=vault_auth_token)
    return client


vault_client = init_client()


def getenv(env):
    try:
        vault_prefix = os.getenv('VAULT_PREFIX')
        vault_namespace = os.getenv('VAULT_NAMESPACE')
        vault_restriction = os.getenv('VAULT_RESTRICTION')
        vault_secret_name = os.getenv('VAULT_SECRET_NAME')
        path = '{vault_prefix}/{vault_namespace}/{restriction}/{secret_name}'.format(
            vault_prefix=vault_prefix,
            vault_namespace=vault_namespace,
            restriction=vault_restriction,
            secret_name=vault_secret_name
        )

        return vault_client.read(path)['data']['data'][env]
    except Exception as ex:
        return os.getenv(env)
