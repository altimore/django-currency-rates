## 0.13.10 (2024-02-13)

### Fix

- updated dependencies

## 0.13.9 (2024-01-29)

### Fix

- the html has changed on exchangeratesorguk.py

## 0.13.8 (2024-01-25)

### Fix

- load the logger in the __main__

## 0.13.7 (2024-01-25)

### Fix

- do not request change rate to itself

## 0.13.6 (2024-01-25)

### Fix

- Updated the logging in the currency_rates application

## 0.13.5 (2024-01-25)

### Fix

- updated the currencyapicom parser

## 0.13.4 (2024-01-25)

### Fix

- added 522 as timeout error on exchangerateapi.io

## 0.13.3 (2023-12-05)

### Fix

- remove the github-ci code

## 0.13.2 (2023-11-28)

### Fix

- updated dependencies

## 0.13.1 (2023-11-28)

### Fix

- updated github ci script to bump version and generate changelog
- readme not displayed correctly

## 0.13.0 (2023-11-27)

### Feat

- trying to autobump on push

### Fix

- error in the readme syntax
- added a check to ignore exchangerateapiio if response is 524
- updated the pre-commit to the latest version

## 0.12.0 (2022-11-23)

### Feat

- added another currency provider.

## 0.11.1 (2022-11-01)

### Fix

- catching key error when there is no error mesage in the json response

## 0.11.0 (2022-10-29)

### Feat

- Added an view mixin to handle the Exchange rate not found exception and a form to input it manually.

## 0.10.1 (2022-10-29)

### Fix

- typo in the mixins

## 0.10.0 (2022-10-29)

### Feat

- add a redirect mixin for catching ratenotfound error

## 0.9.3 (2022-10-28)

### Fix

- added the build details in pyproject

## 0.9.2 (2022-10-28)

### Fix

- relative imports and unused imports

## 0.9.1 (2022-10-28)

### Fix

- relative import changed

## 0.9.0 (2022-10-28)

### Feat

- Reorganized the parsers in a subfolder, added a new one.
- Added a widget.py to be able to use as a django-select2 widget

### Fix

- a couple of errors solved.
- bump version number
- made the import relative to the current folder
- Deleted other top=model packages to be able to install the repo
