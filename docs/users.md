# Users endpoints

## GET /users

List registered users


### Success Response

**Code** : `200 OK`

**Response**


```json
[
    {
        "user_id": "string"
    }
]
```

## POST /users

Register new user

**Request body:**
```json
{
    "user_name": "string"
}
```

### Success Response

**Code** : `200 OK`

**Response**


```json
[
    {
        "msg": "Ok"
    }
]
```

### Conflict Response

**Code** : `409 Conflict`

**Response**


```json
[
    {
        "msg": "User already exists"
    }
]
```