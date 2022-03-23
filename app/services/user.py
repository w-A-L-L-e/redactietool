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
from flask_login import UserMixin
from flask import session

OAS_APPNAME = os.environ.get('OAS_APPNAME', 'mediahaven')


def check_saml_session():
    if 'samlUserdata' in session:
        user_data = session.get('samlUserdata')
        if 'apps' not in user_data:
            return False
        if OAS_APPNAME in user_data['apps']:
            return True

    return False


class User(UserMixin):
    def __init__(self):
        self.name = 'Debug Login'
        self.email = 'wstest@meemoo.be'

    def save_saml_username(self, saml_attribs):
        # attributes=
        # dict_items([('apps', [..., 'mediahaven']),
        # ('cn', ['First name last name']), ('entryUUID', ['user uuid']),
        # ('givenName', ['Walter']), ('mail', ['some@testmail.com']), ('o', ['OR-some-org here']),
        # ('oNickname', ['meemoo']), ('role', ['Meemoo']), ('sector', ['Cultuur']), ('sn', ['Lastname'])])
        # session.get('samlUserdata').get('cn')[0]
        self.name = saml_attribs.get('cn')[0]
