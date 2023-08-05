#!/usr/bin/env python3

import argparse

from Qt.QtWidgets import QApplication
import sys

from .core import MultiGifView


def main():
    """Simple gif viewer

    Commands:
    play - space
    previous frame - p or left-arrow
    next frame - n or right-arrow
    beginning - b or up arrow
    end - e or down arrow
    quit - q, Ctrl-q, Ctrl-w or Ctrl-x
    """
    # Use argparse to add help
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("file", nargs="+", help=".gif files to open")
    from multigifview import __version__

    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s {}".format(__version__)
    )
    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = MultiGifView(args.file)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
