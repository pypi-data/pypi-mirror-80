MultiGifView
============

MultiGifView is a bare-bones Python program for viewing several .gif files at
once, with their play-back synchronised.

The gifs are opened in two columns.

### Installation

Install with pip

    $ pip install multigifview

or with conda

    $ conda install -c conda-forge multigifview

### Usage

    $ multigifview movie1.gif movie2.gif movie3.gif ...

Once the window is opened:

* play/pause - space, or click play button in bottom left

* next frame - n, right arrow or seek-forward button in bottom left

* previous frame - p, left arrow or seek-backward button in bottom left

* end - e, down arrow, or skip-forward button in bottom left

* beginning - b, up arrow, or skip-backward button in bottom left

* quit - q, Ctrl-q, Ctrl-w, Ctrl-x or close the window

Command line argumens:

``-c, --max-columns <i>`` : use at most ``<i>`` columns for display
``-h, --help`` : print help text
``-v, --version`` : print the version number

### In Python code

MultiGifView can be used from within Python code.

    >>> from multigifview import show_gifs
    >>> show_gifs("gif1.gif", "gif2.gif")

Any number of gifs can be passed as positional arguments. ``max_columns`` can
be passed as a keyword argument.

Acknowledgements
----------------

Contributors: [John Omotani](https://github.com/johnomotani)

#### Thanks

From John Omotani to [Peter Hill](https://github.com/ZedThree) for writing the
gui for [hypnotoad](https://github.com/boutproject/hypnotoad) from which I
learned to make a Qt gui in Python.
