============
Photogallery
============

Photogallery is Django app to allow users to look through pictures 
and posts created by admin.

Quick start
-----------

1. Add "photogallery" to INSTALLED_APPS::
    
    INSTALLED_APPS = [
        ...
        'photogallery',
    ]

2. Add photogallery URLconf to urls.py::

    path('photogallery/', include('photogallery.urls')),

3. Run ``python manage.py migrate`` to create models.

4. Start the server and add post on http://127.0.0.1:8000/admin/ after enabling Admin app.

5. Visit http://127.0.0.1:8000/photogallery/ to look through all added picture posts.