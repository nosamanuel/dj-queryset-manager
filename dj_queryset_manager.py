# -*- coding: utf-8 -*-
from functools import wraps

from django.db import models


QUERYSET_CLASS = '_queryset_class'
QUERYSET_METHOD = '_queryset_method'


def queryset_method(method):
    """
    Decorates a manager method so that its first argument is the result
    of the manager's `get_queryset` method. The decorated method will
    also be available on any queryset returned by the manager.
    """
    @wraps(method)
    def manager_method(manager, *args, **kwargs):
        queryset = manager.get_queryset()
        return method(queryset, *args, **kwargs)

    # Store the original method as a queryset method
    setattr(manager_method, QUERYSET_METHOD, method)
    return manager_method


class QuerySetManagerMixin(object):
    def get_query_set(self):
        # Backwards compatibility for Django 1.5 and below
        return self.get_queryset()

    def get_queryset(self):
        try:
            queryset = super(QuerySetManagerMixin, self).get_query_set()
        except AttributeError:
            # Manager.get_query_set was depricated in 1.6
            queryset = super(QuerySetManagerMixin, self).get_queryset()
        queryset_class = self._get_queryset_class(queryset)
        return queryset._clone(klass=queryset_class)

    def _get_queryset_class_name(self):
        return '%sQuerySet' % self.__class__.__name__

    def _get_queryset_method_attributes(self):
        for attribute_name in dir(self):
            attribute_value = getattr(self, attribute_name)
            queryset_method = getattr(attribute_value, QUERYSET_METHOD, None)
            if queryset_method:
                yield attribute_name, queryset_method

    def _get_queryset_class(self, queryset):
        # Use cached queryset class once available
        queryset_class = getattr(self, QUERYSET_CLASS, None)
        if queryset_class is not None:
            return queryset_class

        # Create a custom queryset class that inherits the default class
        # returned by this manager and implements all methods decorated
        # as queryset methods
        queryset_class_name = self._get_queryset_class_name()
        queryset_class = type(queryset_class_name, (type(queryset),), {})
        queryset_class.__module__ = self.__module__
        for name, method in self._get_queryset_method_attributes():
            setattr(queryset_class, name, method)

        # Cache the queryset class so that ever queryset produced by
        # this manager is an instance of the same class
        setattr(self, QUERYSET_CLASS, queryset_class)
        return queryset_class


class QuerySetManager(QuerySetManagerMixin, models.Manager):
    pass
