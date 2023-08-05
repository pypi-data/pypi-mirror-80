=======================================
Quickstart guide
=======================================

Installation
============

You can install ``librec-auto`` using pip command as follows:

::

	$ pip install librec-auto

Since ``librec-auto`` uses ``Librec`` library for running the experiments, after installing ``librec-auto``, you will need to also download ``Librec`` library.

You can use the helper ``install`` command from ``librec_auto``, like this:

::

	$ python -m librec_auto install

The installation is complete. You can now run your experiments using ``librec-auto``.

Building from Source
====================

Instead of installing ``librec_auto`` from pip, you can also build it from the source with:

::

	$ python setup.py install

You may need to uninstall the ``librec_auto`` module first, by running:

::

	$ pip uninstall librec_auto
