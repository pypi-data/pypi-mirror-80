================================================================================
gease - gITHUB RELease
================================================================================

.. image:: https://api.travis-ci.org/moremoban/gease.svg
   :target: http://travis-ci.org/moremoban/gease

.. image:: https://codecov.io/github/moremoban/gease/coverage.png
   :target: https://codecov.io/github/moremoban/gease
.. image:: https://badge.fury.io/py/gease.svg
   :target: https://pypi.org/project/gease

.. image:: https://pepy.tech/badge/gease/month
   :target: https://pepy.tech/project/gease/month

.. image:: https://img.shields.io/github/stars/moremoban/gease.svg?style=social&maxAge=3600&label=Star
    :target: https://github.com/moremoban/gease/stargazers



It's understood that you may use github cli, however **gease** simply makes a git release using github api v3.

.. image:: https://github.com/moremoban/gease/raw/master/images/cli.png
   :width: 600px


Installation
================================================================================


You can install gease via pip:

.. code-block:: bash

    $ pip install gease


or clone it and install it:

.. code-block:: bash

    $ git clone https://github.com/moremoban/gease.git
    $ cd gease
    $ python setup.py install

Setup and Configuration
================================================================================

First, please create `personal access token` for yourself
`on github <https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/>`_.

.. image:: https://github.com/moremoban/gease/raw/master/images/generate_token.png

Next, please create a gease file(`.gease`) in your home directory and place the
token inside it. Gease file is a simple json file. Here is an example::

   {"user":"chfw","personal_access_token":"AAFDAFASDFADFADFADFADFADF"}

Organisation
----------------

In order to make a release for your organisation, "read:org" right is required:

.. image:: https://user-images.githubusercontent.com/4280312/33229231-0220f60e-d1c3-11e7-8c95-3e1207415929.png

Command Line
================================================================================

::

   gease simply makes a git release using github api v3. version 0.0.1

   Usage: gs repo tag [release message]

   where:

      release message is optional. It could be a quoted string or space separate
	  string

   Examples:

      gs gease v0.0.1 first great release
      gs gease v0.0.2 "second great release"



::
contributors list the contributors of a repo. version 0.0.4

Usage: contributors user/org repo

Where:
   user/org is the your github username or orgnisation name
   repo is the repository name

Examples:

    contributors pyexcel pyexcel-io


License
================================================================================

MIT
