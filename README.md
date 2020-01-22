# curesio
Source code for our medical tourism website

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

## Fields and allowed methods for API URLs:

### Doctor signup url

**Methods:** POST

**Required fields:** 'email', 'password', 'username', 'first_name', 'last_name', 'city', 'country', 'primary_language'

**Optional fields:** 'phone', 'date_of_birth', 'postal_code', 'address', 'secondary_language', 'tertiary_language'

**Format of application/json:**
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

**Response format after successful signup:**

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

**Validation errors format:**

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
