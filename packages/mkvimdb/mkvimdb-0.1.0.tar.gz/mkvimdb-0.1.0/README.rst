=======
mkvimdb
=======


.. image:: https://img.shields.io/pypi/v/mkvimdb.svg
        :target: https://pypi.python.org/pypi/mkvimdb

.. image:: https://img.shields.io/travis/gnomonconquest/mkvimdb.svg
        :target: https://travis-ci.com/gnomonconquest/mkvimdb

.. image:: https://readthedocs.org/projects/mkvimdb/badge/?version=latest
        :target: https://mkvimdb.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/gnomonconquest/mkvimdb/shield.svg
     :target: https://pyup.io/repos/github/gnomonconquest/mkvimdb/
     :alt: Updates



Retag MKV files using IMDB, commandline, or an XML file.


* Free software: MIT license
* Documentation: https://mkvimdb.readthedocs.io.


Features
--------

* Creates XMl file for tagging.

* Creates common sense cannonical filenames.

* Is aware of TV series as well as films.

* Can operate interactively as well as fuzzy best guess.

* Use resulting XML to retag an MKV, for example...

`mkvpropedit tarantino,quentin-pulp_fiction-1994.mkv -t global:tarantino,quentin-pulp_fiction-1994.xml`

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
