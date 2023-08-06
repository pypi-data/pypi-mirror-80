# pylint: skip-file
import os

import unimatrix.lib.test
from django.test import TestCase

from ..subject import SubjectRepository


@unimatrix.lib.test.system
class SubjectRepositoryTestCase(TestCase):

    def get_instance(self, **kwargs):
        return self.repo.model(asid=bytes.hex(os.urandom(16)))

    def setUp(self):
        self.repo = SubjectRepository()

    def test_exists_returns_false_on_empty_database(self):
        self.assertFalse(self.repo.exists(1))

    def test_persist(self):
        obj = self.get_instance()
        self.repo.persist(obj)
        self.assertTrue(self.repo.exists(obj.pk))

    def test_get_by_pk(self):
        obj = self.get_instance()
        self.repo.persist(obj)
        self.repo.get(pk=obj.pk)
