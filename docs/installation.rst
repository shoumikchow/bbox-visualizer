.. highlight:: shell

============
Installation
============

Requirements
-----------

* Python >= 3.8
* opencv-python >= 4.1.0.25
* numpy >= 1.19.0

bbox-visualizer officially supports Python 3.8, 3.9, 3.10, 3.11, and 3.12.

Recommended Installation (using uv)
--------------------------------

`uv` is a extremely fast Python package installer and resolver. To install bbox-visualizer using uv:

1. First, install uv if you haven't already:

.. code-block:: console

    $ pip install uv

2. Then install bbox-visualizer:

.. code-block:: console

    $ uv pip install bbox-visualizer

Alternative Installation (using pip)
--------------------------------

You can also install bbox-visualizer using pip:

.. code-block:: console

    $ pip install bbox-visualizer

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for bbox_visualizer can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/shoumikchow/bbox-visualizer

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/shoumikchow/bbox-visualizer/tarball/master

Once you have a copy of the source, you can install it using uv (recommended):

.. code-block:: console

    $ uv pip install .

For development installation with all extra dependencies:

.. code-block:: console

    $ uv pip install ".[dev]"

Or using pip:

.. code-block:: console

    $ pip install .
    $ pip install ".[dev]"  # for development installation


.. _Github repo: https://github.com/shoumikchow/bbox-visualizer
.. _tarball: https://github.com/shoumikchow/bbox-visualizer/tarball/master
