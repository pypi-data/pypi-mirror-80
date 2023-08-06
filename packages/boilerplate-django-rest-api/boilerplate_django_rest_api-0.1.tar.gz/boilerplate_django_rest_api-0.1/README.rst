=====
REST
=====

REST is a Django app build with rest api package such as DjangoRestFramework.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "rest" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'rest',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('rest/', include('django_boilerplate.urls')),

3. Run ``python manage.py migrate`` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to test the rest (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/users/ to test the rest api