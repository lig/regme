Registration for MongoEngine
============================

User registration and management library using MongoEngine


Features
--------

* Create inactive user
* Generate activation token
* Try to activate user via activation token
* Set user password
* Check is activation token expired
* Integrate with django.contrib.auth
* Registration form
* Activation form
* Sample/default registration templates


TODO
----

* Django command to prune users that were not activated.


Installation
------------

`pip install regme`


Configuration
-------------

In addition to [MongoEngine Django support settings](http://docs.mongoengine.org/django.html) Regme requires following settings:

    # The number of days activation token will be valid
    ACCOUNT_ACTIVATION_DAYS = 7
    
    # Regme custom user document for MongoEngine
    # You should not change it unless you know what are you doing
    MONGOENGINE_USER_DOCUMENT = 'regme.documents.User'
    
    # Include regme into installed apps list 
    INSTALLED_APPS = (
        # …
        'django.contrib.auth',
        # …
        'mongoengine.django.mongo_auth',
        # …
        'regme',
        # …
    )


Usage
-----


### Simple

* Include `regme.urls` into your `urlconf`.
* Use tag `{% url 'register' %}` to point to the regme registration view.
* (Optional) Override default templates placed in `regme/templates` folder.


### Advanced

* Use or subclass `regme.forms.UserCreationForm` and `regme.forms.UserActivationForm` manually.
* Subclass `regme.documents.User` and perform whatever magic you want.


Contribute
----------

Feel free to report any issue or fork this project on [Regme Github page](https://github.com/lig/regme).


Authors
-------

[Serge Matveenko](https://github.com/lig)


License
-------

Apache License. See `LICENSE` file.
