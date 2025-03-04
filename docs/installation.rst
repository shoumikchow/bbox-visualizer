.. highlight:: shell

============
Installation
============

Recommended Installation (using uv)
--------------------------------

`uv` is an extremely fast Python package installer and resolver. To install bbox-visualizer using uv:

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

From Source
----------

The source for bbox-visualizer can be downloaded from the `Github repo`_.

You can clone the public repository:

.. code-block:: console

    $ git clone git://github.com/shoumikchow/bbox-visualizer

Once you have a copy of the source, you can install it with uv (recommended):

.. code-block:: console

    $ uv pip install -e .

For development installation with all extra dependencies:

.. code-block:: console

    $ uv pip install -e ".[dev]"

Or using pip:

.. code-block:: console

    $ pip install -e .
    $ pip install -e ".[dev]"  # for development installation

.. _Github repo: https://github.com/shoumikchow/bbox-visualizer
