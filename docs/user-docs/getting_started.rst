Getting Started
===============

This document will show you how to get up and running with **Hy2roresO**.
You will have your docs imported on Read the Docs in 5 minutes,
displayed beautifully for the world.

If you are already using Sphinx or Markdown for your docs, skip ahead to
:ref:`import-docs`.

A quick introduction
---------------

You have two options for formatting your documentation:

Installing the plugin
---------------------

From QGIS Plugin Manager
~~~~~~~~~~~~~~~~~~~~~~~~

To install the plugin, you can simply use QGIS Plugin Manager. In your QGIS, click ``Plugin`` menu and ``Manage and Install Plugins``... After the Plugin Installer dialog shows up, search for Hy2roresO in the search box of the dialog in the ``All`` tab. Select the Hy2roresO plugin and click ``Install``

From the repository
~~~~~~~~~~~~~~~~~~~

If you are adventurous and would like to get the latest code of the plugin, you can install it directly from the repository. The repository is in Github here. There are 2 ways that you can do generally:

* Download the zip from github here: ZIP Master, extract the zip, and copy the extracted root directory into QGIS local plugins directory (on Linux it’s ``~/.local/share/QGIS/QGIS3/profiles/default/python/plugins`` where ``~`` is ``/home/USER``, on Windows it’s ``C:\Users\{username}\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins``)

* Use git: clone the repository in that directory or clone in your preferred location and use symbolic link in local plugins directory.

The :doc:`contribute` page has more information on getting in touch.

Other stuff to remove
~~~~~~~~~~~~~~~~~~~~~

Assuming you have Python_ already, `install Sphinx`_::

    $ pip install sphinx sphinx-autobuild

Create a directory inside your project to hold your docs::

    $ cd /path/to/project
    $ mkdir docs

Run ``sphinx-quickstart`` in there::

    $ cd docs
    $ sphinx-quickstart

``index.rst`` and some other files

Now, edit your ``index.rst`` and add some information about your project.
Include as much detail as you like (refer to the reStructuredText_ syntax
or `this template`_ if you need help). Build them to see how they look::

    $ make html

.. note:: You can use ``sphinx-autobuild`` to auto-reload your docs. Run ``sphinx-autobuild . _build/html`` instead.

In Markdown

You can use Markdown and reStructuredText in the same Sphinx project.
We support this natively on Read the Docs, and you can do it locally::

    $ pip install recommonmark

Then in your ``conf.py``:

.. code-block:: python

    from recommonmark.parser import CommonMarkParser

    source_parsers = {
        '.md': CommonMarkParser,
    }

    source_suffix = ['.rst', '.md']

.. note:: Markdown doesn't support a lot of the features of Sphinx,
          like inline markup and directives. However, it works for
          basic prose content. reStructuredText is the preferred
          format for technical documentation, please read `this blog post`_
          for motivation.

.. _this blog post: http://ericholscher.com/blog/2016/mar/15/dont-use-markdown-for-technical-docs/

.. _connect-account:
