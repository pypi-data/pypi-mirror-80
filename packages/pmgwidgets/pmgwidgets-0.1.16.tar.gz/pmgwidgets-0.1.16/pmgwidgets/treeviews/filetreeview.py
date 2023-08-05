import os
from PyQt5.QtCore import Qt, QModelIndex, pyqtSignal, QLocale,QTranslator
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QMenu, QApplication, QMessageBox, QInputDialog, \
    QLineEdit


class RewriteQFileSystemModel(QFileSystemModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def headerData(self, p_int, Qt_Orientation, role=None):
        if (p_int == 0) and (role == Qt.DisplayRole):
            return self.tr('Name')
        elif (p_int == 1) and (role == Qt.DisplayRole):
            return self.tr('Size')
        elif (p_int == 2) and (role == Qt.DisplayRole):
            return self.tr('Type')
        elif (p_int == 3) and (role == Qt.DisplayRole):
            return self.tr('Last Modified')
        else:
            return super().headerData(p_int, Qt_Orientation, role)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 1


class PMGFilesTreeview(QTreeView):
    '''
    文件树
    '''
    open_signal = pyqtSignal(str)
    new_file_signal = pyqtSignal(str)
    new_folder_signal = pyqtSignal(str)
    delete_file_signal = pyqtSignal(str)
    rename_file_signal = pyqtSignal(str, str)

    def __init__(self, initial_dir: str = '', parent=None):
        super().__init__(parent)
        self.initial_dir = initial_dir
        self.setup_ui()
        self.bind_events()

    def setup_ui(self):
        '''
        界面初始化
        :return:
        '''
        path = os.path.join(os.path.dirname(__file__), 'translations', 'qt_{0}.qm'.format(QLocale.system().name()))
        app = QApplication.instance()
        translator = QTranslator()
        translator.load(path)
        app.installTranslator(translator)
        self.translator = translator

        self.setTabKeyNavigation(True)
        self.setDragEnabled(True)
        self.setDragDropOverwriteMode(True)
        self.setAlternatingRowColors(False)
        self.setUniformRowHeights(True)
        self.setSortingEnabled(True)
        self.setAnimated(True)
        self.setAllColumnsShowFocus(False)
        self.setWordWrap(False)
        self.setHeaderHidden(False)
        self.setObjectName("treeView_files")
        self.header().setSortIndicatorShown(True)

        self.model = RewriteQFileSystemModel()
        self.model.setRootPath(self.initial_dir)

        self.setModel(self.model)
        self.setRootIndex(self.model.index(self.initial_dir))
        self.setAnimated(False)
        self.setSortingEnabled(True)  # 启用排序
        self.header().setSortIndicatorShown(True)  # 启用标题排序
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.init_context_menu()

    def bind_events(self):
        '''
        回调、事件与信号初始化
        :return:
        '''
        self.openAction.triggered.connect(self.on_open)
        self.importAction.triggered.connect(self.on_import)
        self.renameAction.triggered.connect(self.on_rename)
        self.deleteAction.triggered.connect(self.on_delete)

        self.new_file_action.triggered.connect(self.on_new_file)
        self.new_folder_action.triggered.connect(self.on_new_folder)

        self.customContextMenuRequested.connect(self.show_context_menu)

    def init_context_menu(self):
        '''
        初始化右键菜单
        :return:
        '''
        self.contextMenu = QMenu(self)
        self.openAction = self.contextMenu.addAction(self.tr('Open'))

        self.importAction = self.contextMenu.addAction(self.tr('Import'))
        self.importAction.setEnabled(False)

        self.new_file_or_folder_menu = QMenu(self.tr('New..'))
        self.contextMenu.addMenu(self.new_file_or_folder_menu)
        self.new_file_action = self.new_file_or_folder_menu.addAction(self.tr('File'))
        self.new_folder_action = self.new_file_or_folder_menu.addAction(self.tr('Folder'))
        self.new_file_or_folder_menu.addSeparator()

        self.renameAction = self.contextMenu.addAction(self.tr('Rename'))
        self.deleteAction = self.contextMenu.addAction(self.tr('Delete'))

    def show_context_menu(self):
        '''
        显示上下文右键菜单
        :return:
        '''
        self.contextMenu.popup(QCursor.pos())
        self.contextMenu.show()

    def get_current_file_path(self):
        '''
        获取当前文件的路径
        :return:
        '''
        index = self.currentIndex()
        file_info = self.model.fileInfo(index)
        return file_info.absoluteFilePath()

    def on_new_folder(self):
        '''
        新建文件夹时出发的回调
        :return:
        '''
        path = self.get_current_file_path()
        name, stat = QInputDialog.getText(self, self.tr('Please Input file name'), '', QLineEdit.Normal, '')
        if name.find('.') != -1:
            QMessageBox.critical(self, self.tr('Error'),
                                 self.tr('Folder name %s is illeagal!' % name))
            return
        if stat:
            if os.path.isdir(path):
                new_folder_path = os.path.join(path, name)
            else:
                new_folder_path = os.path.join(os.path.dirname(path), name)

            if os.path.exists(new_folder_path):
                QMessageBox.critical(self, self.tr('Error'),
                                     self.tr('Folder %s already exists!' % name))
                return
            else:
                os.mkdir(new_folder_path)
                self.new_folder_signal.emit(new_folder_path)

    def on_new_file(self):
        '''
        新建文件时触发的回调
        :return:
        '''
        path = self.get_current_file_path()
        name, stat = QInputDialog.getText(self, self.tr('Please Input file name'), '', QLineEdit.Normal, '')
        if stat:
            if os.path.isdir(path):
                new_file_path = os.path.join(path, name)
            else:
                new_file_path = os.path.join(os.path.dirname(path), name)

            if os.path.exists(new_file_path):
                QMessageBox.critical(self, self.tr('Error'),
                                     self.tr('File %s already exists!' % name))
                return
            with open(new_file_path, 'wb') as f:
                f.close()
                self.new_file_signal.emit(new_file_path)

    def on_open(self):
        '''
        点击‘open’时候触发的回调，相当于双击。
        :return:
        '''
        path = self.get_current_file_path()
        self.open_signal.emit(path)

    def on_import(self):
        '''

        :return:
        '''
        pass

    def on_rename(self):
        '''
        点击’重命名‘时候的回调。
        :return:
        '''
        from pmgwidgets.platform import rename_file
        path = self.get_current_file_path()
        basename = os.path.basename(path)
        dir_name = os.path.dirname(path)
        name, stat = QInputDialog.getText(self, self.tr('Please Input file name'), '', QLineEdit.Normal, basename)
        if stat:
            new_absolute_path = os.path.join(dir_name, name)
            rename_result = rename_file(path, new_absolute_path)
            if not rename_result:
                QMessageBox.critical(self, self.tr('Error'),
                                     self.tr('Unable to Rename this file.'))
            else:
                self.rename_file_signal.emit(path, new_absolute_path)

    def on_delete(self):
        '''
        点击’删除‘时的回调
        :return:
        '''
        from pmgwidgets.platform import move_to_trash
        path = self.get_current_file_path()

        moved_successful = move_to_trash(path)
        if not moved_successful:
            QMessageBox.critical(self, self.tr('Error'),
                                 self.tr('Unable to Move this file to recycle bin.'))
        else:
            self.delete_file_signal.emit(path)


class Stack(object):

    def __init__(self):
        # 创建空列表实现栈
        self.__list = []

    def is_empty(self):
        # 判断是否为空
        return self.__list == []

    def push(self, item):
        # 压栈，添加元素
        self.__list.append(item)

    def pop(self):
        # 弹栈，弹出最后压入栈的元素
        if self.is_empty():
            return
        else:
            return self.__list.pop()

    def top(self):
        # 取最后压入栈的元素
        if self.is_empty():
            return
        else:
            return self.__list[-1]

    def __len__(self):
        return len(self.__list)

    def __str__(self):
        return str(self.__list)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    tree = PMGFilesTreeview('c:/users/', None)
    tree.show()
    sys.exit(app.exec_())
