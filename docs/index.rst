.. auto-version documentation master file, created by
   sphinx-quickstart on Mon Feb 18 14:35:23 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

auto-version's documentation
============================

.. toctree::

Installation
------------

Just run

::

    pip install auto-version

Usage
-----

You may use it entirely from the CLI, but it may not be advised for projects. The cli is just htere for convenience.

It is intended to be used via a configuration file, by default named *version.conf*

Here is the one used for this module:

::

    {
        "files": "increment_version.py",
        "current_version": "0.1.0",
        "style": "Triplet"
    }

The ``style`` option is a string representing the name of the style class to use. Here, I use the Triplet format, which consists in ``<major>.<minor>.<patch>``.

``"files"`` may be a simple string, or an array, like this:

::

    {
        "files": [
            "path/to/file",
            "other/path/to/file"
        ],
        other stuff,
        blablabla
    }

See `auto_version.styles`_ for more available version string styles.




In-depth documentation for trve l33t hackerz of the internets
-------------------------------------------------------------

Organisation
~~~~~~~~~~~~

Modules detail
~~~~~~~~~~~~~~
.. automodule:: auto_version.parsers
   :members:


.. automodule:: auto_version.styles
   :members:


Less usefull stuff
~~~~~~~~~~~~~~~~~~

.. automodule:: auto_version.utils
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
