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
