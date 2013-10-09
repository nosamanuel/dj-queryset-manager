import os
import unittest

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'

from django.db import models
from dj_queryset_manager import QuerySetManagerMixin, QuerySetManager
from dj_queryset_manager import queryset_method, QUERYSET_METHOD


def by_slug(queryset, slug, **kwargs):
    raise NotImplementedError


class SlugManager(QuerySetManager):
    by_slug = queryset_method(by_slug)


class AttributeErrorManager(QuerySetManager):
    @queryset_method
    def filter(queryset, **kwargs):
        """
        The `filter` method overwrites `QuerySet.filter` and should
        cause an attribute error when the queryset class is constructed.
        """
        pass


class TestQuerySetManager(unittest.TestCase):
    def test_queryset_manager_method(self):
        method = getattr(SlugManager.by_slug, QUERYSET_METHOD)
        self.assertEqual(method, by_slug)

    def test_queryset_class_method(self):
        manager = SlugManager()
        queryset = manager.get_queryset()
        self.assertTrue(hasattr(queryset, 'by_slug'))

    def test_queryset_class(self):
        manager = SlugManager()
        queryset_class = manager._get_queryset_class(models.query.QuerySet())
        self.assertTrue(issubclass(queryset_class, models.query.QuerySet))
        self.assertTrue(isinstance(manager.get_queryset(), queryset_class))
        self.assertTrue(isinstance(manager.get_query_set(), queryset_class))

    def test_existing_attribute(self):
        manager = AttributeErrorManager()
        self.assertRaises(AttributeError, manager.get_queryset)

    def test_wrapped_method(self):
        manager = SlugManager()
        self.assertRaises(NotImplementedError, manager.by_slug, slug='foo')


if __name__ == '__main__':
    unittest.main()
