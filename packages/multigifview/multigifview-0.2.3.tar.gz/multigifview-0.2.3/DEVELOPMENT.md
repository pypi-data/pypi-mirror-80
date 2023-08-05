MultiGifView development
========================

Issue reports and pull requests welcome at
https://github.com/johnomotani/multigifview!

The Qt code for the main window interface is created using qtcreator from Qt (provided
for example by ``conda install qt``) to create/edit the file
``qtdesignerfiles/mainwindow.ui``. The ``.ui`` file is than translated to the Python
code in ``multigifview/mainwindow.py`` with the ``pyuic5`` utility from by PyQt5
(provided for example by ``conda install pyqt>=5``) like this:

    $ pyuic5 mainwindow.ui > ../multigifview/mainwindow.py

``multigifview/mainwindow.py`` should never be edited directly, as changes will be
overwritten when a new version is generated.

The rest of the functionality is provided by the ``MultiGifView`` class in
``multigifview/main.py``.

Installing from git repo
------------------------

Suggested way to install from the git repo is to use

    $ pip install --user -e .

to make an editable install (the installed version will see changes in the repo).

Installing in non-editable mode using

    $ pip install --user .

will fail because the man page does not exist - it is auto-generated in a
Github action for releases. If you want to do this, either copy the stub to get
a generic man page noting that multigifview is a development version

    $ cp man/multigifview.1.dev-stub man/multigifview.1

or create a new man page. For example this can be done as in the Github action

    $ pip install --user -e .
    $ help2man -N multigifview > man/multigifview.1

The ``pip install --user -e .`` is needed first to create the multigifview
executable because use of a relative import means it is not possible to run
``multigifview/__main__.py`` directly.
