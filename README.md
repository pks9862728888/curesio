# curesio
Source code for our medical tourism website.

# API Endpoints
## URLs

*Admin view*

1. **Admin login:** https://www.curesio.com/admin/

*Related to user*

1. **User signup:** https://www.curesio.com/api/user/user-signup/

2. **User full profile view:** https://www.curesio.com/api/user/me/

3. **User token authentication:** https://www.curesio.com/api/user/token/

4. **User image upload:** https://www.curesio.com/api/user/upload-image/


*Related to doctor*

1. **Doctor signup:** https://www.curesio.com/api/doctor/doctor-signup/

2. **Doctor full profile view:** https://www.curesio.com/api/doctor/me/

3. **Doctor token authentication:** https://www.curesio.com/api/doctor/token/

4. **Doctor image upload:** https://www.curesio.com/api/doctor/upload-image/


*Related to staff*

1. **Procedure add and list:** https://www.curesio.com/api/procedure/
2. **Procedure edit, delete, and detail:** https://www.curesio.com/api/procedure/1/

> **GET** request can be done by any user, but **PUT, PATCH, POST, DELETE** can be done by authenticated staff only.

## Fields and allowed methods for API URLs:

### Doctor signup url

- **Methods:** POST

- **Required fields:** 'email', 'password', 'username', 'first_name', 'last_name', 'city', 'country', 'primary_language'

- **Optional fields:** 'phone', 'date_of_birth', 'postal_code', 'address', 'secondary_language', 'tertiary_language'

- **Format of application/json:**
```
{
    "email": "",
    "password": "",
    "username": "",
    "profile": {
        "first_name": "",
        "last_name": "",
        "phone": "",
        "date_of_birth": null,
        "city": "",
        "country": "",
        "postal_code": "",
        "address": "",
        "primary_language": null,
        "secondary_language": null,
        "tertiary_language": null
    },
    "doctor_profile": {
        "experience": null,
        "qualification": "",
        "highlights": ""
    }
}
```

- **Response format after successful signup:**

```
{
    "email": "",
    "username": "",
    "profile": {
        "first_name": "sdfsfs",
        "last_name": "sdfsfs",
        "phone": "",
        "date_of_birth": null,
        "city": "sdfs",
        "country": "IN",
        "postal_code": "",
        "address": "",
        "image": null,
        "primary_language": "EN",
        "secondary_language": null,
        "tertiary_language": null
    },
    "doctor_profile": {
        "experience": null,
        "qualification": "",
        "highlights": ""
    },
    "is_active": false,
    "is_doctor": true,
    "is_staff": false
}
```

- **Validation errors format:**

```
{
    "email": [
        "This field may not be blank."
    ],
    "password": [
        "This field may not be blank."
    ],
    "username": [
        "This field may not be blank."
    ],
    "profile": {
        "first_name": [
            "This field may not be blank."
        ],
        "last_name": [
            "This field may not be blank."
        ],
        "city": [
            "This field may not be blank."
        ],
        "country": [
            "This field may not be null."
        ],
        "primary_language": [
            "This field may not be null."
        ]
    }
}
```

### Doctor Token Authentication url

- **Allowed Methods:** POST

- **Inactive account error format:**

```
{
    "non_field_errors": [
        "Account is inactive. Please wait for activation."
    ]
}
```

- **Validation error format:**

```
{
    "non_field_errors": [
        "Unable to authenticate with provided credentials."
    ]
}
```

### Procedure add URL

- **Methods:** GET, POST

- **Required fields:** 'name', 'speciality', 'overview'

- **Optional fields:** 'image', 'days_in_hospital', 'days_in_destination', 'duration_minutes', 'other_details'

- **Read only fields:** 'id'

- **Response codes:** 
     - **GET:** 200 OK
     - **POST, DELETE, PATCH, PUT:**
             - **By Unauthenticated user:** 401 UNAUTHORIZED
             - **By Authenticated user:** 403 FORBIDDEN
     - **POST:**
             - **By Authenticated staff:** 201 CREATED
     - **DELETE:**
             - **By Authenticated staff:** 204 NO CONTENT
     - **POST, PATCH**
             - **IN CASE OF CONFLICT:** 400 BAD REQUEST

- **Format of application/json:**

```
{
    "name": "",
    "speciality": "",
    "image": null,
    "days_in_hospital": null,
    "days_in_destination": null,
    "duration_minutes": null,
    "overview": "",
    "other_details": ""
}
```

- **Validation Error format:**

```
{
    "name": [
        "This field may not be blank."
    ],
    "speciality": [
        "This field may not be blank."
    ],
    "overview": [
        "This field may not be blank."
    ]
}
```

In case of duplicate content conflict.

```
{
    "name": [
        "Procedure with this name already exists."
    ]
}
```

### Procedure add URL

- **Methods:** GET, PUT, PACTCH, DELETE
