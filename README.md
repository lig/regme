Registration for MongoEngine
============================

User registration and management library using MongoEngine

State
-----

*Beta*


Features
-------------

* Create inactive user
* Generate activation token
* Try to activate user via activation token
* Set user password
* Check is activation token expired
* Integrate with django.contrib.auth
* Registration form
* Activation form
* Password recovery form
* Password change form


ToDo
----

* Sample/default registration templates
* Remove (deactivate) account form
* Reactivate account form
* Documentation


Documentation
-------------

See `tests` folder for usage and config samples.


Installation
------------

`pip install regme`


Configuration
-------------

The only additional setting regme requires is `ACCOUNT_ACTIVATION_DAYS`. You must provide this setting in your `settings.py` file. This setting defines for how long user activation token should be considered as valid. Recomended value is `7`, e.g.:

    ACCOUNT_ACTIVATION_DAYS = 7
