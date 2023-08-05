# pylint: skip-file
import json
import os
import tempfile
import unittest

import ioc
import unimatrix.lib.test
from django.urls import reverse
from django.test import TestCase

from iam.ext.idc.lib import SecretsDirectoryLoader
from iam.ext.idc.infra.repo import SubjectRepository


TEST_PROVIDERS = """
---
apiVersion: v1alpha1
kind: OAuth2Provider
metadata:
  name: oauth-oidc
type: accounts.google.com
spec:
  description: Google
  credentials:
    id: foo
    secret: bar
  scope:
  - openid
  - email
  - profile


---
apiVersion: v1alpha1
kind: OAuth2Provider
metadata:
  name: default
type: accounts.google.com
spec:
  description: Google
  defaultProvider: true
  credentials:
    id: foo
    secret: bar
  scope:
  - openid
  - email
  - profile


---
apiVersion: v1alpha1
kind: OAuth2Provider
metadata:
  name: mock
  annotations:
    lsid: "1"
type: mock
spec:
  description: Mock Provider for Authenticated User
  credentials:
    id: foo
    secret: bar
  scope:
  - openid
  - email
  - profile


---
apiVersion: v1alpha1
kind: OAuth2Provider
metadata:
  name: mock-nouser
type: mock
spec:
  description: Mock Provider for Authenticated User
  credentials:
    id: foo
    secret: bar
  scope:
  - openid
  - email
  - profile
"""


@unittest.skipIf(not os.getenv('DJANGO_SETTINGS_MODULE'),
    "AuthenticationEndpointsTestCase requires DJANGO_SETTINGS_MODULE")
@unimatrix.lib.test.system
class AuthenticationEndpointsTestCase(TestCase):
    fixtures = ['test-subjects']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        secdir = os.environ['APP_SECDIR'] = tempfile.mkdtemp()
        providers_dir = os.path.join(secdir, 'iam.unimatrixone.io/providers')
        os.makedirs(providers_dir)
        with open(os.path.join(providers_dir, 'test.yml'), 'w') as f:
            f.write(TEST_PROVIDERS)
        ioc.provide('iam.IdentityProviderLoaders', [
            SecretsDirectoryLoader(secdir=secdir)
        ], force=True)

    def test_authorize_logs_in_subject(self):
        response = self.client.get(
            reverse('iam:authorize', kwargs={'using': 'mock'}),
            follow=True)
        self.assertEqual(response.status_code, 200, response)

    def test_authorize_logs_not_in_none_subject(self):
        response = self.client.get(
            reverse('iam:authorize', kwargs={'using': 'mock-nouser'}),
            follow=True)
        self.assertEqual(response.status_code, 403)

    def test_login_sets_redirect_cookie(self):
        response = self.client.get(
            reverse('iam:login', kwargs={'using': 'mock'})\
                + '?next=/hello'
        )
        self.assertIn('idc.post_login_redirect', response.cookies)

    def test_login_redirects(self):
        response = self.client.get(
            reverse('iam:login', kwargs={'using': 'mock'})\
                + '?next=/hello',
            follow=True
        )
        self.assertNotIn('idc.post_login_redirect', response.cookies)
        self.assertEqual(response.request['PATH_INFO'], '/hello')

    def test_login_unknown_provider_returns_404(self):
        response = self.client.get(reverse('iam:login', kwargs={'using': 'bla'}))
        self.assertEqual(response.status_code, 404)

    def test_login_default_redirects(self):
        response = self.client.get(reverse('iam:login.default'))
        self.assertEqual(response.status_code, 302)

    def test_oidc_login_redirects(self):
        response = self.client.get(
            reverse('iam:login', kwargs={'using': 'oauth-oidc'}))
        self.assertEqual(response.status_code, 302)

    def test_oidc_invalid_provider_response(self):
        response = self.client.get(reverse('iam:authorize', kwargs={'using': 'oauth-oidc'}))
        self.assertEqual(response.status_code, 500)

    def test_get_default_provider_returns_default(self):
        response = self.client.get(reverse('iam:providers.default'))
        dto = json.loads(bytes.decode(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(dto['name'], 'default')

    def test_list_providers(self):
        response = self.client.get(reverse('iam:providers'))
        self.assertEqual(response.status_code, 200)
