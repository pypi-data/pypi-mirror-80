socialoauth plugin for `Grvlms <https://docs.grvlms.overhang.io>`__
===================================================================================

Installation
------------

::

    pip install git+https://github.com/groovetch/grvlms-socialoauth

Usage
-----

::

    grvlms plugins enable socialoauth

Configuration
-------------

::
    grvlms socialoauth config -i (Run interactively to config ID azure client and secret key)
    grvlms socialoauth config -s (Set a configuration value base on format KEY=VAL)

Azure Configuration
-------------------

::
    - We must to set `SOCIALOAUTH_AZURE_CLIENT_ID` and `SOCIALOAUTH_AZURE_SECRET_KEY` variable. (Get them in your azure-portal).
      (If you don't have azure-portal account yet, please register at https://azure.microsoft.com/en-us/features/azure-portal)
    - Make sure `SOCIALOAUTH_ACTIVATE_AZURE` is true.


    

License
-------

This software is licensed under the terms of the AGPLv3.