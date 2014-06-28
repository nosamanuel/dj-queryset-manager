import os
import unittest

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'

from django.db import models
from dj_queryset_manager import QuerySetManager
from dj_queryset_manager import queryset_method, QUERYSET_METHOD


def by_slug(queryset, slug, **kwargs):
        raise NotImplementedError


class SlugManager(QuerySetManager):
    by_slug = queryset_method(by_slug)
    use_for_related_fields = False


class AttributeOverrideManager(QuerySetManager):
    @queryset_method
    def filter(queryset, *args, **kwargs):
        queryset = super(type(queryset), queryset).filter(**kwargs)
        queryset.exists = lambda: False
        return queryset


class TestModel(models.Model):
    class Meta:
        app_label = 'dj_queryset_manager'
        abstract = True


class Parent(TestModel):
    pass


class Child(TestModel):
    slug = models.SlugField()
    parent = models.ForeignKey(Parent, related_name='children')

    objects = SlugManager()


class QuerySetManagerTestCase(unittest.TestCase):
    def test_manager_sets_queryset_manager_method_attribute(self):
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
        manager = AttributeOverrideManager()
        queryset = manager.filter()
        self.assertFalse(queryset.exists())

    def test_wrapped_method(self):
        manager = SlugManager()
        self.assertRaises(NotImplementedError, manager.by_slug, slug='foo')


class RelatedManagerTestCase(unittest.TestCase):
    def test_related_manager_has_queryset_methods(self):
        parent = Parent()
        self.assertTrue(hasattr(parent.children, 'by_slug'))

    def test_related_queryset_has_queryset_methods(self):
        parent = Parent()
        queryset = parent.children.all()
        self.assertTrue(hasattr(queryset, 'by_slug'))

    def test_related_manager_calls_queryset_method(self):
        parent = Parent()
        manager = parent.children
        self.assertRaises(NotImplementedError, manager.by_slug, 'foo')

    def test_related_queryset_calls_queryset_method(self):
        parent = Parent()
        queryset = parent.children.all()
        self.assertRaises(NotImplementedError, queryset.by_slug, 'foo')


if __name__ == '__main__':
    unittest.main()
