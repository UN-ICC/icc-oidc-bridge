# UN Digital ID - OIDC Bridge

- Bootstrap aca-py with --auto-verify-presentation

```
aca-py start --endpoint http://localhost:8090 --label OIDC --inbound-transport http 0.0.0.0 8090 --outbound-transport http --admin 0.0.0.0 4000 --admin-insecure-mode --wallet-type indy --wallet-name aca-oidc  --wallet-key '123456' --genesis-file pool_genesis_dev  --seed 1111111111111111111111111acaoidc --webhook-url http://localhost:8080/webhooks --auto-verify-presentation
```

- Create RSA key and update your settings with the key 'kid'

```
python manage.py creatersakey
```

- Create a presentation configuration using the admin

- Create a client with the admin: check https://django-oidc-provider.readthedocs.io/en/latest/sections/relyingparties.html

- With the presentation configuration id and the client id, visit the QR web page:

```
http://localhost:8080/vc/connect/authorize/?pres_req_conf_id=verified-email&scope=openid+profile+vc_authn&response_type=code&client_id=770241&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Foidc%2Fauth%2Fcb%2F&state=O8ALJmGFm5ByvYMyWhT7vkzdc3dc5Yds&nonce=vdoOCIrMvSRn2vYcgAV3vszUKb3ACJlD
```
