# Usage

## General

All requests **must** have a valid `Content-Type` header with the type defined in each endpoint documention.

## Protected Routes

Endpoints that are marked as protected must also provide an API key of the current logged in user. The API key goes in the `Authorization` **header** of the request with the `Bearer` prefix.

- Example

  ```
  Authorization: Bearer kp.7BJPEPEf.hWZqh99la6HM3v8_g61cgU3JEX82jjKk1r3XUH_SqbM
  ```

API Keys can be acquired either by creating a new user or logging-in with username/password pair (see below).

On failed authorization, these routes return a `403 Forbidden` response.

## Response Structure

Currently all the endpoints return a JSON response with the same schema shown below

| Property Name | Type  | Explanation |
| --- | --- | --- |
| `type` | `string` | Either `success` or `error` |
| `message` | `string` | A human-friendly message relating the response |
| `payload` | Any valid JSON object (e.g array, `null`, etc) | Additional data associated with the response |

The **Response Payload Schema** info field for each of the responses (defined in **Response** section of an endpoint) provides more description related to the `payload` field of its response.

### Common Payload Schemas

- **ErrorDescriptionSchema**: This schema is used when the request contains invalid input. This represents a JSON object whose keys map to a target key in the request input. Each key's value is an array containing the human-readable error messages for that field.

  - Example

    ```json
    {
      "email": [
         "Invalid email format",
         "This email is already taken" 
      ],
      "password": [
        "Ensure this field has at least 3 characters."
      ]
    }
    ```

# Available Endpoints

| Action | Endpoint |
| --- | --- |
| Create Account | `/auth/signup/` |
| Upload Profile Picture | `/user/upload-picture/` |
| Login | `/auth/login/` |
| Read User Profile | `/user/profile/` |
| Update User Profile | `/user/profile/update/` |
| Update User Credentials | `/user/creds/update/` |
| Update User Password | `/user/password/update/` |

---

## Create Account

### Request

| Method | Protected | Content-type |
| :---: | :---: | :---: |
| POST | No | `application/json` |

**Body Schema**

| Property Name | Type | Required | Explanation |
| --- | --- | --- | --- |
| `username` | `string` | Yes | Username |
| `email` | `string` | Yes | User's email |
| `password` | `string` | Yes | Password. Must be atleast 3 characters |
| `first_name` | `string` | Yes | First name |
| `last_name` | `string` | Yes | Last name |
| `profile_pic_handle` | `string \| null` | No | The generated handle of the user's profile picture uploaded beforehand. See endpoint **Upload Profile Picture** for more information |
| `phone_number` | `string` | Yes | Phone number |
| `post_code` | `string` | Yes | Post Code |
| `address_line_1` | `string` | Yes | Address Line 1 |
| `address_line_2` | `string` | Yes | Address Line 2 |
| `age` | `number` | Yes | Age. Must be greater than 0 |
| `about_me` | `string` | Yes | User's "About Me". Can be empty an string (but it must be present in body). |

### Responses

1. **200 OK**. User created successfully

   - Response Payload Schema:

     ```json
     { "api_key": "<user-api-key>" }
     ```
2. **422 Unprocessable Entity**. Invalid input

   - Response Payload Schema: _ErrorDescriptionSchema_


## Upload Profile Picture

### Request

| Method | Protected | Content-type |
| :---: | :---: | :---: |
| POST | No | `multipart/form-data` |

**Body Schema**

| Property Name | Type | Required | Explanation |
| --- | --- | --- | --- |
| `image` | file | Yes | The profile picture to upload |

### Responses

1. **200 OK**. User created successfully

   - Response Payload Schema:

     ```json
     { "handle": "<profile-picture-handle>" }
     ```

## Login

### Request

| Method | Protected | Content-type |
| :---: | :---: | :---: |
| POST | No | `application/json` |

**Body Schema**

| Property Name | Type | Required | Explanation |
| --- | --- | --- | --- |
| `username` | `string` | Yes | Username |
| `password` | `string` | Yes | Password |

### Responses

1. **200 OK**. User logged-in successfully

   - Response Payload Schema:

     ```json
     { "api_key": "<user-api-key>" }
     ```
2. **401 Unauthorized**. Failed to log in

   - Response Payload Schema: `null`


## Read User Profile

### Request

| Method | Protected | Content-type |
| :---: | :---: | :---: |
| GET | Yes | - |

### Responses

1. **200 OK**

   - Response Payload Schema:

     ```
     {
       "username": "<username>",
       "email": "<email>",
       "first_name": "<first-name>",
       "last_name": "<last-name>",
       "phone_number": "<phone-number>",
       "post_code": "<post-code>",
       "address_line_1": "<address-line-1>",
       "address_line_2": "<address-line-2>",
       "age": <age>,
       "about_me": "<user-about-me>",
       "profile_pic_handle": "<profile-pic-handle>",
       "profile_pic_location": "<profile-pic-location>"
     }
     ```
     **Note**: `profile_pic_location` specifies only the basename (filename + extension) of the profile picture. The absolute URL depends on the application network configuration.
     _Example value:_ `946748f2-42ec-4e66-9cc7-e50a7daccd4b.jpg`


## Update User Profile

### Request

| Method | Protected | Content-type |
| :---: | :---: | :---: |
| POST | Yes | `application/json` |

**Body Schema**

| Property Name | Type | Required | Explanation |
| --- | --- | --- | --- |
| `first_name` | `string` | Yes | First name |
| `last_name` | `string` | Yes | Last name |
| `profile_pic_handle` | `string \| null` | No | The generated handle of the user's profile picture uploaded beforehand. See endpoint **Upload Profile Picture** for more information |
| `phone_number` | `string` | Yes | Phone number |
| `post_code` | `string` | Yes | Post Code |
| `address_line_1` | `string` | Yes | Address Line 1 |
| `address_line_2` | `string` | Yes | Address Line 2 |
| `age` | `number` | Yes | Age. Must be greater than 0 |
| `about_me` | `string` | Yes | User's "About Me". Can be empty an string (but it must be present in body). |


### Responses

1. **200 OK**. User profile updated successfully

   - Response Payload Schema: It echoes back the request body (with a few values normalized if necessary)

2. **422 Unprocessable Entity**. Invalid input

   - Response Payload Schema: _ErrorDescriptionSchema_


## Update User Credentials

### Request

| Method | Protected | Content-type |
| :---: | :---: | :---: |
| POST | Yes | `application/json` |

**Body Schema**

| Property Name | Type | Required | Explanation |
| --- | --- | --- | --- |
| `username` | `string \| null` | Yes | Username. Set to null to keep the existing value. |
| `email` | `string \| null` | Yes | User's email. Set to null to keep the existing value. |

### Responses

1. **200 OK**. User credentials updated successfully

   - Response Payload Schema: It echoes back the request body (with a few values normalized if necessary)

2. **422 Unprocessable Entity**. Invalid input

   - Response Payload Schema: _ErrorDescriptionSchema_

## Update User Password

### Request

| Method | Protected | Content-type |
| :---: | :---: | :---: |
| POST | Yes | `application/json` |

**Body Schema**

| Property Name | Type | Required | Explanation |
| --- | --- | --- | --- |
| `password` | `string` | Yes | Password. Must be atleast 3 characters |

### Responses

1. **200 OK**. User password updated successfully

   - Response Payload Schema: `null`

2. **422 Unprocessable Entity**. Invalid input

   - Response Payload Schema: _ErrorDescriptionSchema_

