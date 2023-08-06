Vault client

Pre-install

```sh
export VAULT_URL=[Vault URL]
export VAULT_AUTH_TOKEN=[auth token]
export VAULT_NAMESPACE=[namespace]
export VAULT_RESTRICTION=[restriction]
export VAULT_SECRET_NAME=[secret name]

cubbyhole/etl/[VAULT_NAMESPACE]/[VAULT_RESTRICTION]/[VAULT_SECRET_NAME]
```

Usage
```sh
pip3 install vault-talenttech-oss
```

```python
import vault.client as osv

#Вернёт DB_PASSWORD из переменных окружения, если не найдёт в Vault
osv.getenv("DB_PASSWORD")
```