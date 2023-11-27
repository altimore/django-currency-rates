=====================
django-currency-rates
=====================

Notes
=====

This is a fork from the original project to use recent django and python3

OpenExchange
============

Django currencies and exchange rates for django projects

You need a key from http://openexchangerates.org/ to get the echange rates

exchangeratesapi.io
===================
Same here https://exchangeratesapi.io/documentation/

Features
========

- Currencies and exchange rates models
- Exchange rates with diferent rates for diferent dates
- Load automatically currencies and rates from http://openexchangerates.org/

Installation
============
if installed remove the previous version
``poetry remove uninstall django-currency_rates``

#. ``poetry git+https://github.com/altimore/django-currency-rates/``
#. Add ``"currency_rates"`` to the ``INSTALLED_APPS`` tuple found in
   your settings file.
#. Add ``OPENEXCHANGERATES_APP_ID`` to your setting file with an app key from http://openexchangerates.org/
#. Run ``manage.py migrate``
#. Run ``manage.py load_currencies`` to load currencies from http://openexchangerates.org/
#. Run ``manage.py load_rates`` to load current eschange rates from http://openexchangerates.org/


Add to your settings.py :
`EXCHANGERATESAPIIO_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`

Extra
=======
If you use django-select2 you can use the widgets as follow :

.. code-block:: python
    from companies.widgets import OrganizationWidget
    from currency_rates.widgets import CurrencyWidget

    class BankAccountForm(forms.ModelForm):
        class Meta:
            model = BankAccount
            fields = "__all__"
            widgets = {
                "company": OrganizationWidget,
                "bank": OrganizationWidget,
                "currency": CurrencyWidget,
            }
