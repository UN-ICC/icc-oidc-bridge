# UN Digital ID - OIDC Bridge

- Bootstrap aca-py with --auto-verify-presentation

```
aca-py start --endpoint http://localhost:8090 --label OIDC --inbound-transport http 0.0.0.0 8090 --outbound-transport http --admin 0.0.0.0 4000 --admin-insecure-mode --wallet-type indy --wallet-name aca-oidc  --wallet-key '123456' --genesis-file pool_genesis_dev  --seed 1111111111111111111111111acaoidc --webhook-url http://localhost:8080/webhooks --auto-verify-presentation
```

To connect the aca-py to the unsjpf-dev blockchain, you'd need a user with role 'steward' (i.e.: aca-unicc2). The docker-compose
aca-py container should be then:

```
aca-py:
    image: bcgovimages/aries-cloudagent:py36-1.15-0_0.5.2
    command: start --endpoint http://localhost:8090 --label OIDC --inbound-transport http 0.0.0.0 8090 --outbound-transport http --admin 0.0.0.0 4000 --admin-insecure-mode --wallet-type indy --wallet-name aca-unicc2  --wallet-key '123456' --genesis-file /pool_genesis_dev  --seed 11111111111111111111111acaunicc2 --webhook-url http://localhost:8080/webhooks --auto-verify-presentation
    volumes:
      - ${PWD}/pool_genesis_dev:/pool_genesis_dev:ro
      - wallets-volume:/home/indy/.indy_client/wallet
    ports:
      - "8090:8090"
      - "4000:4000"
    networks:
      indy:
```

- Create RSA key and update your settings with the key 'kid'

```
python manage.py creatersakey
```

- Create a presentation configuration using the admin. Example:

    id: `verified-email`
    
    subject identifier: `email`
    
    configuration:
    ```
    {"name": "Basic Proof", "version": "1.0", "requested_attributes": [{"name": "email", "restrictions": []}], "requested_predicates": []}
    ```

- Create a client with the admin: check https://django-oidc-provider.readthedocs.io/en/latest/sections/relyingparties.html

- With the presentation configuration id and the client id, visit the QR web page:

```
http://localhost:8080/vc/connect/authorize/?pres_req_conf_id=verified-email&scope=openid+profile+vc_authn&response_type=code&client_id=770241&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Foidc%2Fauth%2Fcb%2F&state=O8ALJmGFm5ByvYMyWhT7vkzdc3dc5Yds&nonce=vdoOCIrMvSRn2vYcgAV3vszUKb3ACJlD
```
