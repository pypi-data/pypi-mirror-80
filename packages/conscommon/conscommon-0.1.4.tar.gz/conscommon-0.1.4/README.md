Common module for Sirius applications
=====================================
[![Build Status](https://api.travis-ci.org/lnls-sirius/cons-common.svg)](https://travis-ci.org/lnls-sirius/cons-common)
![Latest tag](https://img.shields.io/github/tag/lnls-sirius/cons-common.svg?style=flat)
[![Latest release](https://img.shields.io/github/release/lnls-sirius/cons-common.svg?style=flat)](https://github.com/lnls-sirius/cons-common/releases)
[![PyPI version fury.io](https://badge.fury.io/py/conscommon.svg)](https://pypi.python.org/pypi/conscommon/)

Common features for Sirius scripts.
Available at **PyPi** https://pypi.org/project/conscommon/


Data
----
Web API interface.

Data Model
----------
Data model.

Spreadsheet
-----------
XLSX parser, this module should be avoided in favor of the WEB API, usefull in applications that will deal directly with the spreadsheet. Requires `pandas` and `xlrd`.
