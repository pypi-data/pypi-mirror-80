# Oauth2 Flask Service

[![Build Status](https://travis-ci.org/datahq/auth.svg?branch=master)](https://travis-ci.org/dataspot/dgp-oauth2)

A generic OAuth2 authentication service and user permission manager.

Based off [OpenSpending auth service](https://github.com/openspending/os-conductor).

## Quick start

### Clone the repo and install

`make install`

### Run tests

`make test`

### Run server

`python server.py`

## Env Vars
- `PRIVATE_KEY` & `PUBLIC_KEY` an RSA key-pair in PEM format.
  See `tools/generate_key_pair.sh` for more info.
- `GOOGLE_KEY` & `GOOGLE_SECRET`: OAuth credentials for authenticating with Google
- `GITHUB_KEY` & `GITHUB_SECRET`: OAuth credentials for authenticating with Github
- `DATABASE_URL`: A SQLAlchemy compatible database connection string (where user data is stored)
- `EXTERNAL_ADDRESS`: The hostname where this service is located on
- `ALLOWED_SERVICES`:
    Which permissions providers are available. A `;` delimited list of provider identifiers.
    Each provider identifier takes the form of `[alias:]provider`, where `provider` is the name of a Python module
    which exports a `get_permissions(service, userid)` function.
- `INSTALLED_EXTENSIONS`:
    List of installed extensions. A `;` delimited list of `extension` - the name of a Python modules which exports one or all of these functions
    - `on_new_user(user_info)`
    - `on_user_login(user_info)`
    - `on_user_logout(user_info)`


## API

### Check an authentication token's validity
`/auth/check`

**Method:** `GET`

**Query Parameters:**

 - `jwt` - authentication token
 - `next` - URL to redirect to when finished authentication

**Returns:**

If authenticated:

```json
{
    "authenticated": true,
    "profile": {
        "id": "<user-id>",
        "name": "<user-name>",
        "email": "<user-email>",
        "avatar_url": "<url-for-user's-profile-photo>",
        "idhash": "<unique-id-of-the-user>",
        "username": "<user-selected-id>" # If user has a username
    }
}
```

If not:

```json
{
    "authenticated": false,
    "providers": {
        "google": {
            "url": "<url-for-logging-in-with-the-Google-provider>"
        },
        "github": {
            "url": "<url-for-logging-in-with-the-Github-provider>"
        },
    }
}
```

When the authentication flow is finished, the caller will be redirected to the `next` URL with an extra query parameter
`jwt` which contains the authentication token. The caller should cache this token for further interactions with the API.

### Get permission for a service
`/auth/authorize`

**Method:** `GET`

**Query Parameters:**

 - `jwt` - user token (received from `/user/check`)
 - `service` - the relevant service (e.g. `storage-service`)

**Returns:**

```json
{
    "token": "<token-for-the-relevant-service>"
    "userid": "<unique-id-of-the-user>",
    "permissions": {
        "permission-x": true,
        "permission-y": false
    },
    "service": "<relevant-service>"
}
```

### Change the username
`/auth/update`

**Method:** `POST`

**Query Parameters:**

 - `jwt` - authentication token (received from `/user/check`)
 - `username` - A new username for the user profile (this action is only allowed once)

**Returns:**

```json
{
    "success": true,
    "error": "<error-message-if-applicable>"
}
```

__Note__: trying to update other user profile fields like `email` will fail silently and return

```json
{
    "success": true
}
```

### Receive authorization public key
`/auth/public-key`

**Method:** `GET`

**Returns:**

The service's public key in PEM format.

Can be used by services to validate that the permission token is authentic.
