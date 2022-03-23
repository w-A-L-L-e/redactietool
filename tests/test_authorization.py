# -*- coding: utf-8 -*-
#
#  @Author: Walter Schreppers
#
#  tests/test_authorization.py
#

import pytest


def test_wrong_credentials(client):
    res = client.post('/legacy_login', data=dict(
        username='avo-syncrator',
        password='wrong_pass',
    ), follow_redirects=True)

    assert 'Fout email of wachtwoord' in res.data.decode()


def test_right_credentials(client):
    res = client.post('/legacy_login', data=dict(
        username='admin',
        password='admin',
    ), follow_redirects=True)

    assert 'Fout email of wachtwoord' not in res.data.decode()
