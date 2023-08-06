Forked from and based on https://github.com/Relrin/sanic-base-extension (sanic-base-extension)
Extensions were forked and modified to keep the code updated with 
the latest version of dependecnies and to add additional functionality

sanic-ext-base
##############
Flask-like extension support for Sanic framework

Features
========
- Flask-like style initializing and using with Sanic applications
- Easy to write a new extension and use it later

Installation
============
This package should be installed using pip: ::

    pip install sanic-ext-base


Example
=======
.. code-block:: python

    from sanic import Sanic
    from sanic_ext import BaseExtension


    class CustomExtension(BaseExtension):
        extension_name = app_attribute = 'custom'

        def hello(self, user):
            print("Hello, {}!".format(user))


    app = Sanic(__name__)
    CustomExtension()  # available via `app.custom` or `app.extensions['custom']`
    app.custom.hello('world')  # Hello, world!

License
=======
The sanic-ext-base is published under BSD license. For more details read LICENSE_ file.

.. _links:
.. _LICENSE: https://github.com/openwhalereef/sanic-ext-base/blob/master/LICENSE