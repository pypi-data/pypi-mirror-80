

.. ddt_api_calls documentation master file, created by startproject.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ddt-api-calls's documentation!
=========================================

:Version: 0.3.0
:Source: https://github.com/maykinmedia/ddt-api-calls
:Keywords: django, debug, debug_toolbar, requests, api
:PythonVersion: 3.8

|build-status| |coverage| |black|

|python-versions| |django-versions| |pypi-version|

A Django Debug Toolbar pannel to track calls made with requests library

.. contents::

.. section-numbering::

Features
========

* Track (API) calls made with the requests library
* Display individual request method, path and duration
* Display total number of calls and total duration start-end

Installation
============

Requirements
------------

* Python 3.6 or above
* setuptools 30.3.0 or above
* Django 2.2 or newer


Install
-------

.. code-block:: bash

    pip install ddt-api-calls


1. Add ``ddt_api_calls`` to ``INSTALLED_APPS``.
2. Add ``ddt_api_calls.panels.APICallsPanel`` to the ``DEBUG_TOOLBAR_PANELS`` setting.


Usage
=====

Make your usual requests and see the data in the panels :-)


.. |build-status| image:: https://travis-ci.org/maykinmedia/ddt-api-calls.svg?branch=master
    :target: https://travis-ci.org/maykinmedia/ddt-api-calls

.. |coverage| image:: https://codecov.io/gh/maykinmedia/ddt-api-calls/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/maykinmedia/ddt-api-calls
    :alt: Coverage status

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/ddt-api-calls.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/ddt-api-calls.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/ddt-api-calls.svg
    :target: https://pypi.org/project/ddt-api-calls/
