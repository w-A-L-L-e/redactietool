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

    def save_saml_username(self, saml_attribs):
        #attributes= 
        # dict_items([('apps', [..., 'mediahaven']), 
        # ('cn', ['First name last name']), ('entryUUID', ['user uuid']), 
        # ('givenName', ['Walter']), ('mail', ['some@testmail.com']), ('o', ['OR-some-org here']), 
        # ('oNickname', ['meemoo']), ('role', ['Meemoo']), ('sector', ['Cultuur']), ('sn', ['Lastname'])])
        # session.get('samlUserdata').get('cn')[0]
        self.name = saml_attribs.get('cn')[0]

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
            self.name = "Developer Login"
        except jwt.exceptions.ExpiredSignatureError:
            self.name = "JWT Session Expired"
        except jwt.exceptions.InvalidAudienceError:
            self.name = "JWT Invalid Audience"
