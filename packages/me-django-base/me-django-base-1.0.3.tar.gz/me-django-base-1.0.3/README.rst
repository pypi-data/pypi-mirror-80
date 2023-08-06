=====
Base
=====

Base is a Django app to conduct Web-based base. For each
question, visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "base" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'base',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^base/', include('base.urls')),

3. Run `python manage.py migrate` to create the base models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a base (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/base/ to participate in the base.