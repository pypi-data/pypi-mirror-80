OMERO.web
=========
.. image:: https://travis-ci.org/ome/omero-web.svg?branch=master
    :target: https://travis-ci.org/ome/omero-web

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black


Introduction
------------

OMERO.web provides a web based client and plugin infrastructure.

Dependencies
------------

Direct dependencies of OMERO.web are:

- `OMERO.py`_
- `ZeroC IcePy`_
- `Pillow`_
- `NumPy`_
- A WSGI capable web server

Installation
------------

See: `OMERO`_ documentation

Usage
-----

See: `OMERO`_ documentation

Contributing
------------

See: `OMERO`_ documentation

Developer installation
----------------------

OMERO.web depends on OMERO.py. If you want a developer installation of OMERO.py, replace ``pip install omero-py``
with instructions at https://github.com/ome/omero-py.

For a development installation we recommend creating a virtualenv with the following setup (example assumes ``python3.6`` but you can create and activate the virtualenv using any compatible Python):

::

    python3.6 -mvenv venv
    . venv/bin/activate
    pip install zeroc-ice==3.6.5
    pip install omero-py          # OR dev install (see above)
    git clone https://github.com/ome/omero-web
    cd omero-web
    pip install -e .

This will install OMERO.web into your virtualenv as an editable package, so any edits to source files should be reflected in your installation.

Note some omero-web tests may not run when this module and/or omero-py are installed in editable mode.

Running tests
-------------

Unit tests are located under the `test` directory and can be run with pytest.

Integration tests
^^^^^^^^^^^^^^^^^

Integration tests are stored in the main repository (ome/openmicroscopy) and depend on the
OMERO integration testing framework. Reading about `Running and writing tests`_ in the `OMERO`_ documentation
is essential.

Release process
---------------

This repository uses `bump2version <https://pypi.org/project/bump2version/>`_ to manage version numbers.
To tag a release run::

    $ bumpversion release

This will remove the ``.dev0`` suffix from the current version, commit, and tag the release.

To switch back to a development version run::

    $ bumpversion --no-tag patch

NB: this assumes next release will be a ``patch`` (see below).
To complete the release, push the master branch and the release tag to origin::

    $ git push origin master v5.8.0

If any PRs are merged that would require the next release to be a ``major`` or ``minor`` version
(see `semver.org <https://semver.org/>`_) then that PR can include a version bump created via::

    $ bumpversion --no-tag minor|major

If this hasn't been performed prior to release and you wish to specify the next version
number directly when creating the release, this can be achieved with::

    $ bumpversion --new-version 5.9.0 release

omero-web-docker
^^^^^^^^^^^^^^^^

Following ``omero-web`` release, need to update and release ``omero-web-docker``.

License
-------

OMERO.web is released under the AGPL.

Copyright
---------

2009-2020, The Open Microscopy Environment, Glencoe Software, Inc.

.. _OMERO: https://www.openmicroscopy.org/omero
.. _OMERO.py: https://pypi.python.org/pypi/omero-py
.. _ZeroC IcePy: https://zeroc.com/
.. _Pillow: https://python-pillow.org/
.. _NumPy: http://matplotlib.org/
.. _Running and writing tests: https://docs.openmicroscopy.org/latest/omero/developers/testing.html
