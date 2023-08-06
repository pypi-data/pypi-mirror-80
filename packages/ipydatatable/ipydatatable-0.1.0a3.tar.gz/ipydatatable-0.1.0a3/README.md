# ipydatatable

[![Version](https://img.shields.io/pypi/v/ipydatatable.svg)](https://pypi.python.org/pypi/ipydatatable)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gl/teia_engineering%2Fipydatatable/master?filepath=examples)
[![Documentation Status](http://readthedocs.org/projects/ipydatatable/badge/?version=latest)](https://ipydatatable.readthedocs.io/)

Library to wrap interactive datatables js into a library that helps pandas dataframes

## Installation


To install use pip:

    $ pip install ipydatatable
    $ jupyter nbextension enable --py --sys-prefix ipydatatable

To install for jupyterlab

    $ jupyter labextension install ipydatatable

For a development installation (requires npm),

    $ git clone https://github.com/teia_engineering/ipydatatable.git
    $ cd ipydatatable
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix ipydatatable
    $ jupyter nbextension enable --py --sys-prefix ipydatatable
    $ jupyter labextension install js

When actively developing your extension, build Jupyter Lab with the command:

    $ jupyter lab --watch

This takes a minute or so to get started, but then automatically rebuilds JupyterLab when your javascript changes.

Note on first `jupyter lab --watch`, you may need to touch a file to get Jupyter Lab to open.
