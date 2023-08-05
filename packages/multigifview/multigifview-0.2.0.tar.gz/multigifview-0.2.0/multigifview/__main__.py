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
    # Make sure application exits on Ctrl-C
    import signal

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Use argparse to add help
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("file", nargs="+", help=".gif files to open")
    parser.add_argument(
        "-c",
        "--max-columns",
        help="maximum number of columns to use (default 2)",
        type=int,
        default=2,
    )
    from multigifview import __version__

    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s {}".format(__version__)
    )
    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = MultiGifView(args.file, max_columns=args.max_columns)
    window.show()
    window.reset_minimum_size()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
