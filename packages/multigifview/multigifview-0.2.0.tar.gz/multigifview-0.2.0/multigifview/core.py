from pathlib import Path

from .mainwindow import Ui_MainWindow
from Qt.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QShortcut,
    QSizePolicy,
    QSpacerItem,
    QStyle,
    QVBoxLayout,
)
from Qt.QtGui import QMovie, QKeySequence


class MultiGifView(QMainWindow, Ui_MainWindow):
    """A program for viewing .gif files"""

    def __init__(self, filenames, *, max_columns):
        super().__init__(None)
        self.setupUi(self)

        # extra keyboard shortcuts
        quit_shortcut = QShortcut(QKeySequence("Q"), self)
        quit_shortcut.activated.connect(QApplication.instance().quit)
        quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        quit_shortcut.activated.connect(QApplication.instance().quit)
        quit_shortcut = QShortcut(QKeySequence("Ctrl+X"), self)
        quit_shortcut.activated.connect(QApplication.instance().quit)
        quit_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        quit_shortcut.activated.connect(QApplication.instance().quit)
        previous_shortcut = QShortcut(QKeySequence("left"), self)
        previous_shortcut.activated.connect(self.previous_action)
        next_shortcut = QShortcut(QKeySequence("right"), self)
        next_shortcut.activated.connect(self.next_action)
        beginning_shortcut = QShortcut(QKeySequence("up"), self)
        beginning_shortcut.activated.connect(self.beginning_action)
        end_shortcut = QShortcut(QKeySequence("down"), self)
        end_shortcut.activated.connect(self.end_action)

        def set_clicked(widget, function):
            widget.clicked.connect(function)
            if hasattr(function, "__doc__"):
                widget.setToolTip(function.__doc__.strip())

        set_clicked(self.play_button, self.play_action)
        set_clicked(self.previous_button, self.previous_action)
        set_clicked(self.next_button, self.next_action)
        set_clicked(self.beginning_button, self.beginning_action)
        set_clicked(self.end_button, self.end_action)

        if max_columns < 1:
            raise ValueError(f"Number of columns must be positive, got {max_columns}")
        n_columns = min(max_columns, len(filenames))
        self.columns = [self.column0]
        for i in range(n_columns)[1:]:
            # Create column
            column = QVBoxLayout()
            column.setObjectName(f"column{i}")
            spacerItem = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
            column.addItem(spacerItem)
            self.gif_layout.addLayout(column)
            self.columns.append(column)

        self.extra_movies = []
        self.extra_gif_widgets = []
        for i, arg in enumerate(filenames):
            gif_widget = QLabel(self.centralwidget)
            gif_widget.setText("")
            gif_widget.setObjectName(f"gif_widget{i + 1}")

            filepath = Path(arg)
            movie = QMovie(str(filepath))
            movie.setCacheMode(QMovie.CacheAll)
            gif_widget.setMovie(movie)
            movie.jumpToFrame(0)

            column = self.columns[i % n_columns]
            position = column.count() - 1
            column.insertWidget(position, gif_widget)

            self.extra_movies.append(movie)
            self.extra_gif_widgets.append(gif_widget)

        # Set a sensible initial width
        scrollable_width = (
            sum([c.sizeHint().width() for c in self.columns])
            + self.columns[0].spacing()
            + sum([2 * c.spacing() for c in self.columns[1:-1]])
            + self.columns[-1].spacing()
            + self.scrollArea.verticalScrollBar().sizeHint().width()
        )
        (
            left_margin,
            top_margin,
            right_margin,
            bottom_margin,
        ) = self.verticalLayout_main.getContentsMargins()
        max_width = (
            QApplication.desktop().availableGeometry().width()
            - left_margin
            - right_margin
        )
        self.scrollArea.setMinimumWidth(min(scrollable_width, max_width))

        # Set a sensible initial height
        column_heights = [c.sizeHint().height() for c in self.columns]
        highest_col_index = column_heights.index(max(column_heights))
        scrollable_height = (
            column_heights[highest_col_index]
            + self.columns[highest_col_index].spacing()
            + self.scrollArea.horizontalScrollBar().sizeHint().height()
        )
        control_bar_height = (
            self.horizontalLayout.sizeHint().height()
            + 2 * self.horizontalLayout.spacing()
        )
        menu_bar_height = self.menubar.sizeHint().height()
        title_bar_height = QApplication.style().pixelMetric(QStyle.PM_TitleBarHeight)
        max_height = (
            QApplication.desktop().availableGeometry().height()
            - top_margin
            - bottom_margin
            - control_bar_height
            - menu_bar_height
            - title_bar_height
        )
        self.scrollArea.setMinimumHeight(min(scrollable_height, max_height))

        # want the longest-running gif to be the one that's directly controlled, so that
        # it can play all the way to the end, not have to stop when the first movie
        # reaches its last frame
        frame_counts = [m.frameCount() for m in self.extra_movies]
        ind_longest = frame_counts.index(max(frame_counts))
        self.movie = self.extra_movies.pop(ind_longest)

        # Create actions so extra movies follow self.movie
        self.movie.frameChanged.connect(self.change_frames)

    def play_action(self):
        """Play the gif"""
        if self.movie.state() == QMovie.Running:
            self.movie.setPaused(True)
        elif self.movie.state() == QMovie.Paused:
            self.movie.setPaused(False)
        else:
            self.movie.start()

    def previous_action(self):
        """Back one frame"""
        self.movie.jumpToFrame(
            (self.movie.currentFrameNumber() - 1) % self.movie.frameCount()
        )

    def next_action(self):
        """Forward one frame"""
        self.movie.jumpToNextFrame()

    def beginning_action(self):
        """Back to beginning"""
        self.movie.jumpToFrame(0)

    def end_action(self):
        """Forward to end"""
        self.movie.jumpToFrame(self.movie.frameCount() - 1)

    def change_frames(self, new_frame):
        """Change all the frames in step"""
        for movie in self.extra_movies:
            length = movie.frameCount()
            if new_frame < length:
                movie.jumpToFrame(new_frame)
            else:
                movie.jumpToFrame(length - 1)

    def reset_minimum_size(self):
        """Allow window to be shrunk from default size"""
        self.scrollArea.setMinimumWidth(0)
        self.scrollArea.setMinimumHeight(0)
