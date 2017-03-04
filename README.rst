=====================
django-currency-rates
=====================

Notes
=====

This is a simple fork from the original project just to use django on python3.

OpenExchange
============

Django currencies and exchange rates for django projects

You need a key from http://openexchangerates.org/ to get the echange rates

Features
========

- Currencies and exchange rates models
- Exchange rates with diferent rates for diferent dates
- Load automatically currencies and rates from http://openexchangerates.org/

Installation
============
if installed remove the previous version
``pip uninstall django-currency_rates``

#. ``pip install https://github.com/altimore/django-currency-rates/archive/master.zip``
#. Add ``"currency_rates"`` to the ``INSTALLED_APPS`` tuple found in
   your settings file.
#. Add ``OPENEXCHANGERATES_APP_ID`` to your setting file with an app key from http://openexchangerates.org/
#. Run ``manage.py migrate``
#. Run ``manage.py load_currencies`` to load currencies from http://openexchangerates.org/
#. Run ``manage.py load_rates`` to load current eschange rates from http://openexchangerates.org/
