dj-queryset-manager
~~~~~~~~~~~~~~~~~~~

A Django utility that makes it simple to write DRY queryset methods.


Warning
-------

This project has been superceded by ``QuerySet.as_manager()``. See `the docs <https://docs.djangoproject.com/en/dev/ref/models/querysets/#django.db.models.query.QuerySet.as_manager>`_.



Usage
-----

1. Create a manager class that inherit the ``QuerySetManager``
2. Decorate your filter methods with ``queryset_method``. **These methods receive a queryset instead of a manager as the first argument**.

.. code:: python

    from dj_queryset_manager import QuerySetManager, queryset_method

    class MyManager(QuerySetManager):
        @queryset_method
        def by_slug(queryset, slug):
            return queryset.filter(slug=slug)

        @queryset_method
        def filter(queryset, *args, **kwargs):
            return super(type(queryset), queryset).filter(*args, **kwargs)


For reference, here is a standard implementation:

.. code:: python

    from django.db.models import Manager
    from django.db.models.query import QuerySet

    class MyQuerySet(QuerySet):
        def by_slug(self, slug):
            return self.filter(slug=slug)

        def filter(self, *args, **kwargs):
            return super(MyQuerySet, self).filter(*args, **kwargs)


    class MyManager(Manager):
        def get_query_set(self): # Better remember the arguments to QuerySet
            QuerySet(self.model, using=self._db)

        def get_queryset(self): # And don't forget about Django 1.6
            return self.get_query_set()

        def by_slug(self, *args, **kwargs):  # Enjoy this duplicate signature
            return self.get_queryset().filter(*args, **kwargs)


Mix-in
------

Some third-party apps ship managers as part of their API. If you need to extend any existing manager, use the ``QuerySetManagerMixin``. This example uses the ``InheritanceManager`` from `django-model-utils <https://github.com/carljm/django-model-utils>`_.

.. code:: python

    from model_utils.managers import InheritanceManager
    from dj_queryset_manager import QuerySetManagerMixin, queryset_method

    class MyInheritanceManager(QuerySetManagerMixin, InheritanceManager):
        @queryset_method
        def by_slug(queryset, slug):
            return queryset.filter(slug=slug)


Planned Obsolescence
--------------------

This project will be partially obsoleted by Django 1.7, when you can do this:

.. code:: python

    from django.db.models import Manager
    from django.db.models.query import QuerySet

    class MyQuerySet(QuerySet):
        def by_slug(self, slug):
            return queryset.filter(slug=slug)

    MyManager = Manager.from_queryset(MyQuerySet)


However, if you still need to extend existing managers, or you don't want to worry about the upgrade path from ``Manager.get_query_set`` to ``Manager.get_queryset`` in your own code, you may want to stick with this package.


Installation
------------

    $ pip install dj-queryset-manager
