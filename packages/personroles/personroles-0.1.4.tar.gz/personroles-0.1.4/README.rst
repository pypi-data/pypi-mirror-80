Overview
========

.. |docs| image:: https://readthedocs.org/projects/person/badge/?version=latest
    :target: https://person.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |Codacy Badge| image:: https://app.codacy.com/project/badge/Grade/5a29d30f3ec7470cb17085a29a4c6a8f
    :target: https://www.codacy.com/manual/0LL13/person?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=0LL13/person&amp;utm_campaign=Badge_Grade)  

.. |build| image:: https://travis-ci.org/0LL13/person.svg?branch=master
    :target: https://travis-ci.org/github/0LL13/person
    :alt: Travis-CI Build Status

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/personroles.svg
    :target: https://www.python.org/
    :alt: Supported versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/personroles.svg
    :target: https://realpython.com/cpython-source-code-guide/ 
    :alt: Supported implementations

.. |license| image:: https://img.shields.io/github/license/0LL13/person
    :target: https://opensource.org/licenses/MIT
    :alt: GitHub

.. |update| image:: https://pyup.io/repos/github/0LL13/person/shield.svg
    :target: https://pyup.io/repos/github/0LL13/person/
    :alt: Updates

.. |coverage| image:: https://codecov.io/gh/0LL13/person/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/0LL13/person

.. |pypi| image:: https://img.shields.io/pypi/v/personroles
    :target: https://pypi.org/project/personroles/
    :alt: PyPI

.. |pull| image:: https://img.shields.io/github/issues-pr/0LL13/person
    :target: https://github.com/0LL13/person/pulls
    :alt: GitHub pull requests

.. |climate| image:: https://api.codeclimate.com/v1/badges/714a256d1edf47898a22/maintainability
   :target: https://codeclimate.com/github/0LL13/person/maintainability
   :alt: Maintainability



.. list-table::
    :widths: auto 

    * - limits
      - |pypi| |supported-versions| |supported-implementations| |climate|
    * - code
      - |Codacy Badge| |coverage| |build| |update| |pull|
    * - legal
      - |license|
    * - read
      - |docs|

A set of dataclasses concerning roles (academic, politician, ...)  of persons and their particulars

Features
--------

Currently names of this structure are supported::

    Names:                       first_name middle_name_1 middle_name_2 last_name/s
    Names with academic title:   academic_title/s first_name ... last_name/s
    Names with peer title:       peer_title/s first_name ... last_name/s
    Names with peer preposition: first_name ... peer_preposition last_name/s
    Names with all titles:       academic/peer_title first_name ... peer_preposition last_name/s

These roles have been sketched::

    Academic - academic_title
    Person - gender, born, age, deceased
    Noble - peer_title, peer_preposition
    Politician - electoral_ward, ward_no, voter_count, minister, offices, party, parties
    MdL - legislature, parl_pres, parl_vicePres

Usage
=====
::

    from personroles import person

    tom = person.Academic("Thomas H.", "Smith", academic_title="MBA")
    print(tom)

    Academic:
    academic_title=MBA
    first_name=Thomas
    last_name=Smith
    middle_name_1=H.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

Installation
------------
::

    pip install person-roles

Contribute
----------

| `Issue Tracker`_
| Source_

.. _`Issue Tracker`: https://github.com/0LL13/person/issues
.. _Source: https://github.com/0LL13/person

Support
-------

Feel free to fork and improve.

Warranty
--------

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT SHALL
THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY
DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.

License
-------

MIT License

Copyright (c) 2020 Oliver Stapel
