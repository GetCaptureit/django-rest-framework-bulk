Django REST Framework Bulk
==========================

.. image:: https://badge.fury.io/py/djangorestframework-bulk.png
   :target: http://badge.fury.io/py/djangorestframework-bulk

.. image:: https://d2weczhvl823v0.cloudfront.net/miki725/django-rest-framework-bulk/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

Django REST Framework bulk CRUD view mixins.

Overview
--------

Django REST Framework comes with many generic views however none
of them allow to do bulk operations such as create, update and delete.
To keep the core of Django REST Framework simple, its maintainer
suggested to create a separate project to allow for bulk operations
within the framework. That is the purpose of this project.

Requirements
------------

* Python (2.6, 2.7 and 3.3)
* Django 1.3+
* Django REST Framework >= 3.0.0

Installing
----------

Using pip::

    $ pip install djangorestframework-bulk

or from source code::

    $ pip install -e git+http://github.com/miki725/django-rest-framework-bulk#egg=djangorestframework-bulk

Example
-------

The bulk views (and mixins) are very similar to Django REST Framework's own
generic views (and mixins)::

    from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView

    class FooView(ListBulkCreateUpdateDestroyAPIView):
        queryset = FooModel.objects.all()
        serializer_class = FooModelSerializer

where `FooModelSerializer` is defined as::

    from rest_framework_bulk.serializers import BulkListSerializer, BulkSerializerMixin
    from rest_framework.serializers import ModelSerializer

    class FooModelSerializer(BulkSerializerMixin, ModelSerializer):
        class Meta:
            model = FooModel
            list_serializer_class = BulkListSerializer

A ``list_serializer_class`` definition has become necessary due to API changes in the Django REST Framework 3.0
regarding multiple updates
(see `ListSerializer in the docs <http://www.django-rest-framework.org/api-guide/serializers/#listserializer>`_ for
details). The additional serializer mixin temporarily adds a unique field to the deserialized values for determining
which instance to update, as read-only fields are otherwise discarded. By default the ``id`` field is used, but can be
set by overriding the ``update_lookup_field`` class attribute.

The above will allow to create the following queries

::

    # list queryset
    GET

::

    # create single resource
    POST
    {"field":"value","field2":"value2"}     <- json object in request data

::

    # create multiple resources
    POST
    [{"field":"value","field2":"value2"}]

::

    # update multiple resources (requires all fields)
    PUT
    [{"field":"value","field2":"value2"}]   <- json list of objects in data

::

    # partial update multiple resources
    PATCH
    [{"field":"value"}]                     <- json list of objects in data

::

    # delete queryset (see notes)
    DELETE

Router
------

The bulk router can map automatically the bulk actions ::

	from rest_framework_bulk.routes import BulkRouter
		
	class UserViewSet(BulkCreateModelMixin
	                  BulkUpdateModelMixin,
	                  BulkDestroyModelMixin,
	                  viewsets.ModelViewSet):
	    model = User
	    
	    def allow_bulk_destroy(self, qs, filtered):
	        """Don't forget to fine-grain this method"""
	
	router = BulkRouter()
	router.register(r'users', UserViewSet)

Notes
-----

Most API urls have two URL levels for each resource:

1. ``url(r'foo/', ...)``
2. ``url(r'foo/(?P<pk>\d+)/', ...)``

The second url however is not applicable for bulk operations because
the url directly maps to a single resource. Therefore all bulk
generic views only apply to the first url.

There are multiple generic view classes in case only a certail
bulk functionality is required. For example ``ListBulkCreateAPIView``
will only do bulk operations for creating resources.
For a complete list of available generic view classes, please
take a look at the source code at ``generics.py`` as it is mostly
self-explanatory.

Most bulk operations are pretty safe in terms of how they operate,
that is you excplicitly describe all requests. For example, if you
need to update 3 specific resources, you have to explicitly identify
those resources in the request's ``PUT`` or ``PATCH`` data.
The only exception to this is bulk delete. Conside a ``DELETE``
request to the first url. That can potentially delete all resources
without any special confirmation. To try to account for this, bulk delete
mixin allows to implement a hook to determine if the bulk delete
request should be allowed::

    class FooView(BulkDestroyAPIView):
        def allow_bulk_destroy(self, qs, filtered):
            # custom logic here

            # default checks if the qs was filtered
            # qs comes from self.get_queryset()
            # filtered comes from self.filter_queryset(qs)
            return qs is not filtered

By default it checks if the queryset was filtered and if not will not
allow the bulk delete to complete. The logic here is that if the request
is filtered to only get certain resources, more attention was payed hence
the action is less likely to be accidental. On how to filter requests,
please refer to Django REST
`docs <http://www.django-rest-framework.org/api-guide/filtering>`_.
Either way, please use bulk deletes with extreme causion since they
can be dangerous.

Credits
-------

Maintainers/contributors:

* Miroslav Shubernetskiy - https://github.com/miki725
* Arien Tolner - https://github.com/Bounder
* Kevin Brown - https://github.com/kevin-brown
* Martin Cavoj - https://github.com/macav
* Mjumbe Poe - https://github.com/mjumbewu
* Thomas Wajs - https://github.com/thomasWajs
* Xavier Ordoquy - https://github.com/xordoquy

