# -*- coding: utf-8 -*-
#
#  @Author: Walter Schreppers
#
#  app/services/user.py
#
#   wrapper with UserMixin to make flask-login play nicely with our jwt token
#   this allows us to have the real username in our menu structure on all pages
#

import os
import jwt
from flask_login import UserMixin


# we might need this back laters...
OAS_SERVER = os.environ.get('OAS_SERVER', 'https://oas-qas.viaa.be')
OAS_APPNAME = os.environ.get('OAS_APPNAME', 'mediahaven')
OAS_JWT_SECRET = os.environ.get('OAS_JWT_SECRET', '')


class User(UserMixin):
    def __init__(self):
        self.name = 'Debug Login'
        self.email = 'wstest@meemoo.be'

    # TODO: once we switch to true SAML this is the only method that needs a changin
    def save_jwt_username(self, token):
        try:
            dt = jwt.decode(
                token,
                audience=[OAS_APPNAME],
                algorithms=['HS256'],
                verify=False,
                options={'verify_signature': False}
            )

            self.name = dt.get('cn')

        except jwt.exceptions.DecodeError:
            self.name = "Debug Login (dec error)"
        except jwt.exceptions.ExpiredSignatureError:
            self.name = "JWT Session Expired"
        except jwt.exceptions.InvalidAudienceError:
            self.name = "JWT Invalid Audience"
