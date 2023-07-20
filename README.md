# ICC OIDC Bridge

This repository contains Python/Django code for an implementation of Indy verifiable credential-based authentication using OpenID Connect

The project is a rewrite of [VC-AuthN OIDC](https://github.com/bcgov/vc-authn-oidc) that is written in .Net as we needed the implementation to be done in Python. We have tried to mimic the vc-authn-oidc workflows and endpoints so it can be used as replacement of the .Net project in their [Demo](https://github.com/bcgov/vc-authn-oidc/tree/master/demo)

## Dependencies

The project depends on a PostgreSQL database and a running instance of [ACA-PY](https://github.com/hyperledger/aries-cloudagent-python). Both are included in the docker-compose file found in the repository.

## Running the project

 Docker and docker-compose is used to start the project. The .env_example file has defaults for your project. Copy it to a .env file so they are used by the docker-compose. Review them to match your environment, but it should work as-is for a local test

```
$ cp .env_example .env
$ docker-compose up -d

```

## Non-interactive auth (for mobile)

Non-interactive authentication (from user perspective) can be achieved by adding prompt=none in the initial call to /vc/connect/authorize. This will return a JSON object instead of a website. The returned object definition is as follows:
```
{
  "url": short_url,
  "b64_presentation": b64_presentation,
  "poll_interval": settings.POLL_INTERVAL,
  "poll_max_tries": settings.POLL_MAX_TRIES,
  "poll_url": f"{settings.SITE_URL}/vc/connect/poll?pid={pres_req}",
  "resolution_url": f"{settings.SITE_URL}/vc/connect/callback?pid={pres_req}",
}
```
As this is an asyncronous authentication, the client (relying party) should be polling periodically /vc/connect/callback (the URL is returned in resolution_url in the JSON payload). A 403 HTTP error means the request has not been yet fullfilled. Any other 4XX error means a real problem so polling can stop. On success, a redirect will be returned with the code to obtain the token.

## Running the demo

To be able to use this project in the vc-authn-demo [Demo](https://github.com/bcgov/vc-authn-oidc/tree/master/demo) we need to follow this steps.

**Important**
You should run the demo in a workstation with direct access from Internet, using a cloud provider or ngrok

 - Start the agent

```
docker-compose up -d

```

 - Set superadmin password to be able to configure the bridge

```
 docker-compose exec oidc-django bash
 
 code$ python manage.py createsuperuser
```
 - Connect to the admin console: http://localhost:8084/admin

 - Add the following key in the model RSAKey so it matches the variable JWT_KEY_KID in oidc_controller/settings/local.py

```
 -----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAvIB54C9f5Q03NpQCSwdCwCTxvRdmMkIc2D/jwi8hyixpAFhe
ZpiRg3nr+oakjsQUiBAktaPSgVKuxM19dndI/zttbw4U52fDJHsltIbPfRcvNrGw
RdiPyvXyxnMJh+lVI/0hNSebZhX7QqzADPb9g8g6UbOXTDSAkparOPCNkS3fW4RS
WfPIJNg7IsMkMg00nnu8XmVSwuci05s1FA8M+AZnejy2exwWpgiJxu/JrF0cnmyf
KeFYY4oC94mVyCgD9t+QbP7x/QpnPbb3oUOT3pvB6fUwuLGK3QPKA759U4zkU8N+
CS3FvUoc8ekWNLWv8oeMe6OswKbPd7wpRGObmwIDAQABAoIBACaP5d7d8jEqffQV
XU66AobKSAXV5ps7eSkoENDl0XTJlwVyDoXQilwqMgNDTiDCriyTmN7rz6GTJ5ut
KhB1IKLOJnoEmHQqfvpUkwcWWRYPCyKWQShYwDnWDL9aQ0XhjwBYxVVZb+n3bzpZ
msRMNtqhuISER9xYFUFnv0lbtKpRLP4PAGEcR+Md68iJvC9Rio8T9yIkBs5dOj1f
7H14ga18mLCpPvuX6Nvpo/+bNczaWunUBPX2BN2W2n+vLVpHd8m7cGcF+UHVYYf0
tFIuiIuU7YTGlwnHmpC4LBbfIvDYRV2E3VPZB+fl2byLH8I3I6U4oqSliREh7nBt
FHFvEAkCgYEAzV9vS6LOpxJEe1LZ9VWlMzGIyfcnii8iKoiU8mvQIfKRojsuRDje
zzILh42V/IWq+d6nHzWq71IZLESzKcUaJoM/0tWC3IbdUKNJBxhmRAsmqixQ5U/5
CClK6a8aG2vBMEBwemAwTrSxSvZOWn9gsYWuvMFpTr5U79c0mUB/SF8CgYEA6vhb
28UNZQ98zLEyb1Kuz3GFjOn6dRHK4K5GSW2gLr/ooe+Hb5atZLWRgiIloJ8fNT+I
ud4ybEiSbJlo7u8pPsqnA1XK3MYTDjbdwHAQQtvPzw29u2Qp+4uDoBiMItFMYJRI
vpAG2Fcs7JfRuDoFi1XyfwJ1hwfH56PSrs4JJkUCgYEApOnnoyLfMsW2fBkxsJHP
kGZMY3G2LH5gvyriADCW90ujqlQ/eMT6FgMnwvfs4tQrUW57YNJlqruQPz4DaJ0/
vIFUdObCqHcbrK8R60KqjCUwLSJc62bmoKkX4MKdAjvq6+Yy6/HlmK38WCelD4KN
kL+6axQcjgDEj7uOHynti50CgYA8xVtMrdxXBPhsIHBA5oubz2qRFXrXiHCGR8yZ
9SZ2sN/D8iV/MONLpsIpfBdrQXxa00HTgKpd4y8rs0m2cliiittDO48qJniLNpmH
yfQKtrs6e/1UWAWbr2utnmuwHZ25ZOCjmLCMh49w6ZsuIKOKdAIx4zruX47OVEqL
N3KaWQKBgEqs5Z+g8mdVNC1hu9XCoW8g3VxQ8Y1OqTepOTlLqNc7BYpSSb3aXl+t
N7IgcwsvUCurZufUI5wuHf2zAEk8g9+2OVAkoIj0O4zm0p4JYfpWgDAI8z7R3yfu
t6UBCB+s1tVpoooQ1VCeSrLsB5GMS5uT6WsEfkAf3DQUhLxhDNH2
-----END RSA PRIVATE KEY-----
```

 If you need to generate your own key, you can use the following command:
 ```
 code$ python manage.py creatersakey
 RSA key successfully created with kid: 525786059b724b15b2d23033664342ff
 ```
 And update the local.py with the new key
 
- Head to http://localhost:8084/admin/ and login with the superuser you just created

- Create a presentation configuration using the admin interface. Example:

    id: `verified-email`
    
    subject identifier: `email`
    
    configuration:
    ```
    {"name": "Basic Proof", "version": "1.0", "requested_attributes": [{"name": "email", "restrictions": []}], "requested_predicates": []}
    ```

- Create a client with the admin: check [Add Client](https://django-oidc-provider.readthedocs.io/en/latest/sections/relyingparties.html#using-the-admin). When creating the client ensure that the client has the following parameters:
    - Name: Testing
    - Client Type: Public
    - Response types: code(Authorization Code Flow)
    - Redirect Uris: http://localhost:8084/oidc/auth/cb/ (This URL should match what it comes 
      from the RP in the demo)

- Note the client ID which was generated

- Generate the QR Code
	- Alternative A: run the vc-authn-oidc demo with instructions from the following repository
	   ```
	   git clone https://github.com/bcgov/vc-authn-oidc.git
	   ```
	   - After creating the client in the step above, get the client ID and update the [manage](https://github.com/bcgov/vc-authn-oidc/blob/master/demo/docker/manage) and modify the variable OIDC_RP_CLIENT_ID
	 
	- Alternative B: open link in browser
	  - invoke the following URL, replacing the IP address, the redirect URI and the client_id
		```
		 http://localhost:5000/vc/connect/authorize?pres_req_conf_id=verified-email&scope=openid+profile+vc_authn&response_type=code&client_id=310090&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Foidc%2Fauth%2Fcb%2F&state=O8ALJmGFm5ByvYMyWhT7vkzdc3dc5Yds&nonce=
		``` 
		
