=======
ibancom
=======


.. image:: https://img.shields.io/pypi/v/ibancom.svg
        :target: https://pypi.python.org/pypi/ibancom

.. image:: https://img.shields.io/travis/RegioHelden/ibancom.svg
        :target: https://travis-ci.org/RegioHelden/ibancom

.. image:: https://readthedocs.org/projects/ibancom/badge/?version=latest
        :target: https://ibancom.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Python client for IBAN.com_ API

.. _IBAN.com: https://www.iban.com


* Free software: MIT license
* Documentation: https://ibancom.readthedocs.io.


Features
--------

* IBAN validation
* IBAN bank data details

Tests
-----

Tests will be automatically run by travis on commit to master.

They can also be executed locally using docker-compose by running ```docker-compose up```

Requirements upgrades
---------------------

Check for upgradeable packages by running ```docker-compose run --rm python pip-check```

Making a new release
--------------------

bumpversion_ is used to manage releases.

.. _bumpversion: https://www.iban.com

Add your changes to the HISTORY_ and run ```docker-compose run --rm python bumpversion <major|minor|patch>```, then push (including tags)

.. _HISTORY: ./HISTORY.rst

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

