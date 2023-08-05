=======
remauth
=======

Login to a Django website remotely.

Prerequisites
-------------

Setup django-rest-framework. This app requires auth tokens.

Quick start
-----------

1. Installation

    pip install django-remauth

2. Add to INSTALLED_APPS

    INSTALLED_APPS = [
        ...,
        'remauth',
    ]

3. Add important constants to settings.py

    REMAUTH_DEFAULT_AUTH_BACKEND="dotted.path.to.your.backend" (Default: "django.contrib.auth.backends.ModelBackend")

    REMAUTH_SUCCESS_URL="your-url/"

    REMAUTH_GET_DATA={'key', 'value'}

4. Hook up urls.

    path('your-path/', include('remauth.urls'))

5. Generate rest framework auth token from django admin.

6. POST to https://yourwebsite.io/your-path/api/generate/ to generate a login token.

    The POST request must contain an object with a key 'email' that contains a value corresponding to the email address of a valid user.

    The response will be an object:

    {"token": token}

7. Visit https://yourwebsite.io/your-path/verify/email@example.com/the-token-previously-generated/ to login.

    This will redirect to REMAUTH_SUCCESS_URL if successful.

8. You can fetch arbritary data from your website remotely by GETing https://yourwebsite.io/your-path/details/

    Populate REMAUTH_GET_DATA first.
    