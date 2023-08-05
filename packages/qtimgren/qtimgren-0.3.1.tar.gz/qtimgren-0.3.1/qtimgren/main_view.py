from PySide2.QtWidgets import QTableView, QStyledItemDelegate, \
    QStyleOptionViewItem, QApplication, QHeaderView
from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt, Slot, \
    QItemSelection, QItemSelectionModel, QAbstractItemModel, QSize, \
    QTimer, QSettings
from PySide2.QtGui import QImage, QPainter
from pyimgren.pyimgren import Renamer, exif_dat
from .profile_manager import Profile
import os.path
import re
import typing
import datetime
from fnmatch import fnmatch


class Model(QAbstractTableModel):
    rx = re.compile(r'.*\.jpe?g*', re.I)

    def __init__(self, profile: Profile, view: QTableView):
        super().__init__(view.parent())
        self.profile = profile
        self.view = view
        self.files = []
        self.orig = {}
        self.renamer = None
        self.ini_files()

    def ini_files(self):
        if self.profile is None:
            self.files = []
            self.orig = {}
            self.renamer = None
        else:
            self.files = [entry.name for entry in os.scandir(self.profile.path)
                          if entry.is_dir() or self.rx.match(entry.name)]
            self.renamer = Renamer(self.profile.path, self.profile.mask,
                                   self.profile.pattern, ext_mask='')
            self.orig = self.renamer.load_names()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.files)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 4

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: int = Qt.DisplayRole) -> typing.Any:
        header = ['Image', 'Name', 'Original', 'New name']
        if orientation == Qt.Orientation.Horizontal and role == Qt.DisplayRole:
            return header[section]

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> typing.Any:
        file = self.files[index.row()]
        if role == Qt.DisplayRole:
            if index.column() == 1:
                return file
            if index.column() == 2:
                return self.orig.get(file, None)
            if index.column() == 3:
                try:
                    dat = exif_dat(os.path.join(self.profile.path, file))
                    if dat is not None:
                        dat += datetime.timedelta(minutes=self.renamer.delta)
                        return dat.strftime(self.profile.pattern)
                except OSError:
                    pass
        elif index.column() == 0:
            if role == Qt.DecorationRole:
                return QImage(os.path.join(self.profile.path, file))
        return None

    @Slot()
    def profile_changed(self, profile):
        self.beginResetModel()
        self.profile = profile
        self.ini_files()
        self.endResetModel()

    @Slot()
    def delta_changed(self, delta):
        self.renamer.delta = delta
        self.dataChanged.emit(self.index(0, 3),
                              self.index(self.rowCount() - 1, 3))

    def item_selection(self, direct: bool = True) -> QItemSelection:
        sel = QItemSelection()
        sel1 = QItemSelection()
        if direct:
            for i, file in enumerate(self.files):
                if fnmatch(file, self.renamer.src_mask):
                    sel1.select(self.index(i, 0), self.index(i, 3))
                    sel.merge(sel1, QItemSelectionModel.SelectCurrent)
        else:
            for i, file in enumerate(self.files):
                if file in self.renamer.load_names():
                    sel1.select(self.index(i, 0), self.index(i, 3))
                    sel.merge(sel1, QItemSelectionModel.SelectCurrent)
        return sel

    def rename(self, files: list):
        self.renamer.rename(*files)
        self.reset()

    def back(self, files: list):
        self.renamer.back(*files)
        self.reset()

    def reset(self):
        self.beginResetModel()
        self.ini_files()
        self.endResetModel()


class View(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.images_display = None
        QApplication.instance().aboutToQuit.connect(self.save)

    def initialize(self, model: QAbstractItemModel, images_display):
        super().setModel(model)
        self.images_display = images_display
        self.load()
        self.reset_selection()

    @Slot()
    def profile_changed(self, profile):
        old = self.model().profile.path
        self.model().profile_changed(profile)
        if old != profile.path:
            self.itemDelegateForColumn(0).reset_cache()
        self.reset_selection()

    @Slot(float)
    def delta_changed(self, delta):
        self.model().delta_changed(delta)

    @Slot()
    def rename(self):
        self.model().rename(self.selected_files())

    @Slot()
    def back(self):
        self.model().back(self.selected_files())

    @Slot()
    def reset_selection(self):
        return self._do_selection(True)

    def _do_selection(self, direction: bool):
        selection = self.selectionModel()
        item_sel = self.model().item_selection(direction)
        selection.select(item_sel, QItemSelectionModel.ClearAndSelect)

    @Slot()
    def select_renamed(self):
        return self._do_selection(False)

    @Slot()
    def save(self):
        settings = QSettings()
        settings.beginGroup('View')
        settings.beginWriteArray('col_size')
        for i in range(3):
            settings.setArrayIndex(i)
            w = self.columnWidth(i)
            if w != 0:
                settings.setValue('col', w)
        settings.endArray()
        settings.setValue('display_images',
                          self.images_display.checkState() == Qt.Checked)
        settings.endGroup()

    @Slot()
    def display_images(self, display):
        self.setColumnHidden(0, not display)
        if not display:
            self.verticalHeader().resizeSections(QHeaderView.ResizeToContents)

    def load(self):
        settings = QSettings()
        settings.beginGroup('View')
        sz = settings.beginReadArray('col_size')
        for i in range(sz):
            settings.setArrayIndex(i)
            w = settings.value('col')
            self.setColumnWidth(i, w)
        settings.endArray()
        display = settings.value('display_images', type=bool)
        if not display:
            self.setColumnHidden(0, True)
        self.images_display.setCheckState(Qt.Checked if display
                                          else Qt.Unchecked)
        settings.endGroup()
        delegate = ImageDelegate(self)
        self.setItemDelegateForColumn(0, delegate)
        self.pre_load(delegate)

    def selected_files(self):
        return [self.model().data(ix, Qt.DisplayRole)
                for ix in self.selectionModel().selectedRows(1)]

    def pre_load(self, delegate):
        view = self
        files = view.model().files
        width = view.columnWidth(0)
        cur = 0
        timer = QTimer(view)

        def step():
            nonlocal width, cur, files
            if view.model().files is not files:
                cur = 0
                files = view.model().files
            if view.columnWidth(0) != 0 and view.columnWidth(0) != width:
                cur = 0
                width = view.columnWidth(0)
            if cur < len(files) and width != 0:
                delegate.do_get_pixmap(view.model(), cur, width)
                cur += 1
            if cur >= len(files):
                timer.setInterval(1000)
            else:
                timer.setInterval(0)

        timer.timeout.connect(step)
        timer.start()


class ImageDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cache = {}

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        pixmap = self.get_pixmap(option, index)
        return QSize() if pixmap.isNull() else pixmap.size()

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        pixmap = self.get_pixmap(option, index)
        if not pixmap.isNull():
            view = option.styleObject
            view.setRowHeight(index.row(), pixmap.height())
            painter.drawImage(option.rect, pixmap)

    def get_pixmap(self, option: QStyleOptionViewItem, index: QModelIndex) -> QImage:
        view = option.styleObject
        model = view.model()
        w = view.columnWidth(0)
        return self.do_get_pixmap(model, index.row(), w)

    def do_get_pixmap(self, model, row, w):
        if w == 0:
            return QImage()
        file = model.files[row]
        try:
            pixmap = self.cache[model.orig.get(file, file)]
            if (pixmap is not None) and (not pixmap.isNull()) and (pixmap.width() != w):
                pixmap = None
        except KeyError:
            pixmap = None
        if pixmap is None:
            image = QImage(os.path.join(model.profile.path, file))
            pixmap = image.scaledToWidth(w)
            self.cache[model.orig.get(file, file)] = pixmap
        return pixmap
