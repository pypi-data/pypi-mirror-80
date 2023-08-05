# pylint: skip-file
from unittest import TestCase

import unimatrix.lib.test
from django.apps import apps

from ..subject import SubjectRepository


@unimatrix.lib.test.unit
class SubjectRepositoryTestCase(TestCase):

    @property
    def model(self):
        return apps.get_model('idc.AssertedSubject')

    def setUp(self):
        self.repo = SubjectRepository()

    def test_model_is_correct(self):
        self.assertEqual(self.repo.model, self.model)

    def test_do_not_exist_is_proxied(self):
        self.assertEqual(self.repo.DoesNotExist, self.model.DoesNotExist)
