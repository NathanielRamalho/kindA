#!/usr/bin/env python
# coding: UTF-8
#
## @package ui_main_window
#
#   Models the kindA Graphin User Interface.
#
#   @author Nathaniel Ramalho
#   @since 11/28/2020
#
from PySide2.QtWidgets import QMainWindow, QApplication, \
    QHBoxLayout, QVBoxLayout, QSplitter, QAction, QTabWidget, \
    QTableWidget, QTableWidgetItem, QListWidget, QFrame, \
    QLabel, QHeaderView, QAbstractItemView, QDial, QLCDNumber, \
    QMessageBox
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtCore import Qt, QSize
from ui_code_editor import CodeEditor
import sys


##
# Class that creates Graphi User Interface
#
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.left = 300
        self.top = 150
        self.width = 1000
        self.height = 600
        self.title = 'kindA - MIPS Simulator'
        self.icon_name = 'assets/icon_logo.png'

        # frames
        self.frame_editor = EditorFrame()
        self.frame_console = ConsoleFrame()
        self.frame_register = RegisterFrame()
        self.frame_pc = PCFrame()

        # actions
        self.action_executar = None
        self.action_executar_etapas = None
        self.action_avancar = None
        self.action_traduzir = None
        self.action_parar = None
        self.action_salvar = None
        self.action_salvar_como = None
        self.action_exportar = None
        self.action_abrir = None
        self.action_fechar = None
        self.action_sair = None
        self.action_sobre = None
        self.action_ajuda = None
        self.action_redefinir = None

        # Widgets
        self.dial_clock = QDial()
        self.lcd_clock_value = QLCDNumber()

        self.create_menu_and_toolbar()

        self.init_window()

    ##
    # Initializes and configures the main window
    #
    def init_window(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(self.icon_name))
        self.setGeometry(self.left,
                         self.top,
                         self.width,
                         self.height)
        self.setIconSize(QSize(20, 20))
        # self.setStyleSheet(
        #     'QScrollBar:vertical{'
        #     'border-style: none;'
        #     'background: transparent;'
        #     'width: 8px}'
        #     'QScrollBar:handle:vertical{'
        #     'background-color: white;'
        #     'min-height: 20px;}'
        #     'QScrollBar::up-arrow:vertical, '
        #     'QScrollBar::down-arrow:vertical {'
        #     'border-style: none;'
        #     'background: transparent;'
        #     '}')

        self.setStyleSheet('QScrollBar:vertical {'
                           'border: none;'
                           'background: yellow;'
                           'width: 8px;'
                           'margin: 21px 0 21px 0;'
                           'border-radius: 0px;}'
                           'QScrollBar:handle:vertical{'
                           'background: #596064;'
                           'min-height: 25px;'
                           'border-radius: 7px}'
                           'QScrollBar:add-line:vertical {'
                           'border: none;'
                           'background: #27292A;'
                           'height: 20px;'
                           'border-bottom-left-radius: 7px;'
                           'border-bottom-right-radius: 7px;'
                           'subcontrol-position: bottom;'
                           'subcontrol-origin: margin;}'
                           'QScrollBar:sub-line:vertical {'
                           'border: none;'
                           'background: #27292A;'
                           'height: 20px;'
                           'border-top-left-radius: 7px;'
                           'border-top-right-radius: 7px;'
                           'subcontrol-position: top;'
                           'subcontrol-origin: margin;}'
                           'QScrollBar:up-arrow:vertical, '
                           'QScrollBar:down-arrow:vertical {'
                           'background: none; '
                           'height: 5px;}'
                           'QScrollBar:add-page:vertical, '
                           'QScrollBar:sub-page:vertical{'
                           'background: none;}'
                           ''
                           'QScrollBar:horizontal{'
                           'border: none;'
                           'background: rgb(52, 59, 72);'
                           'height: 8px;'
                           'margin: 0px 21px 0 21px;'
                           'border-radius: 0px;}'
                           'QScrollBar:handle:horizontal{'
                           'background: #596064;'
                           'min-width: 25px;}'
                           'QScrollBar:add-line:horizontal{'
                           'border: none;'
                           'background: #27292A;'
                           'width: 20px;'
                           'subcontrol-position: right;'
                           'subcontrol-origin: margin;}'
                           'QScrollBar:sub-line:horizontal {'
                           'border: none;'
                           'background: #27292A;'
                           'width: 20px;'
                           'subcontrol-position: left;'
                           'subcontrol-origin: margin;}'
                           'QScrollBar:up-arrow:horizontal, '
                           'QScrollBar:down-arrow:horizontal{'
                           'background: none;'
                           'width: 5px}'
                           'QScrollBar:add-page:horizontal, '
                           'QScrollBar:sub-page:horizontal{'
                           'background: none;}')

        hbox_main = QHBoxLayout()
        frame_main = QFrame()
        frame_main.setStyleSheet('background-color: black; color: black')
        hbox_main.setContentsMargins(3, 3, 3, 3)

        # Criando o splitter vertical
        main_splitter_vertical = QSplitter(Qt.Vertical)
        splitter_horizontal = QSplitter(Qt.Horizontal)

        main_splitter_vertical.setStyleSheet('background-color: black;')

        # adicionando elementos no splitter horizontal
        splitter_horizontal.addWidget(self.frame_editor)
        splitter_horizontal.addWidget(self.frame_pc)
        splitter_horizontal.addWidget(self.frame_register)
        splitter_horizontal.setSizes([4, 1, 2])

        main_splitter_vertical.addWidget(splitter_horizontal)
        main_splitter_vertical.addWidget(self.frame_console)

        # Settando os tamanhos iniciais.
        main_splitter_vertical.setSizes([1, 2])

        # adicionano o spliter ao hbox_main
        hbox_main.addWidget(main_splitter_vertical)

        # self.setLayout(hbox_main)

        self.setCentralWidget(frame_main)
        frame_main.setLayout(hbox_main)

        self.show()

    ##
    # Creates and configures Menu bar and tool bar
    #
    def create_menu_and_toolbar(self):
        # Definindo  a barra de Menu
        main_menu = self.menuBar()
        main_menu.setStyleSheet('QMenuBar{'
                                'background-color: #3C3F41;'
                                'color: #9BAEC1;}'
                                'QMenuBar:item:selected{'
                                'Background-color: #4D5154;'
                                'color: #9BAEC1;}'
                                'QMenuBar:item:pressed{'
                                'Background-color: #596064;'
                                'color: #9BAEC1;}'
                                'QMenu{'
                                'background-color: #3C3F41;'
                                'color: #9BAEC1;}'
                                'QMenu:item:selected{'
                                'Background-color: #4D5154;'
                                'color: #9BAEC1;}'
                                'QMenu:item:pressed{'
                                'Background-color: #596064;'
                                'color: #9BAEC1;}')

        # adding actions on menu bar
        menu_arquivo = main_menu.addMenu('Arquivo')
        menu_executar = main_menu.addMenu('Executar')
        menu_ajuda = main_menu.addMenu('Ajuda?')

        # Creating menu bar itens (Actions)
        # MENU ARQUIVO
        self.action_salvar = QAction(
            QIcon('assets/icon_salvar.png'),
            'Salvar',
            self)
        self.action_salvar_como = QAction('Salvar como...', self)
        self.action_exportar = QAction('Exportar...', self)
        self.action_abrir = QAction(QIcon('assets/icon_open.png'), 'Abrir...', self)
        self.action_fechar = QAction('Fechar documento...', self)
        self.action_sair = QAction('Sair', self)
        self.action_salvar.setShortcut(QKeySequence('Ctrl+s'))
        self.action_salvar_como.setShortcut(QKeySequence('Ctrl+Shift+s'))
        self.action_sair.setShortcut(QKeySequence('Alt+F4'))

        # MENU EXECUTAR
        self.action_executar = QAction(QIcon('assets/icon_run.png'), 'Executar', self)
        self.action_executar_etapas = QAction(QIcon('assets/icon_step_run.png'), 'Executar em etapas', self)
        self.action_avancar = QAction(QIcon('assets/icon_avacar.png'), 'Avançar', self)
        self.action_traduzir = QAction(QIcon('assets/icon_translate.png'), 'Traduzir', self)
        self.action_parar = QAction(QIcon('assets/icon_stop.png'), 'Parar execução', self)
        self.action_redefinir = QAction('Redefinir máquina virtual', self)
        self.action_executar.setShortcut(QKeySequence('Shift+F10'))
        self.action_executar_etapas.setShortcut(QKeySequence('Shift+F9'))
        self.action_avancar.setShortcut(QKeySequence('F7'))
        self.action_traduzir.setShortcut(QKeySequence('Ctrl+t'))
        self.action_parar.setShortcut(QKeySequence('Shift+F9'))

        # AJUDA
        self.action_sobre = QAction('Sobre', self)
        self.action_ajuda = QAction('Ajuda', self)

        # Adding itens to menu
        # Arquivo
        menu_arquivo.addAction(self.action_abrir)
        menu_arquivo.addAction(self.action_fechar)
        menu_arquivo.addSeparator()
        menu_arquivo.addAction(self.action_salvar)
        menu_arquivo.addAction(self.action_salvar_como)
        menu_arquivo.addAction(self.action_exportar)
        menu_arquivo.addSeparator()
        menu_arquivo.addAction(self.action_sair)
        # Executar
        menu_executar.addAction(self.action_executar)
        menu_executar.addAction(self.action_executar_etapas)
        menu_executar.addAction(self.action_avancar)
        menu_executar.addAction(self.action_traduzir)
        menu_executar.addAction(self.action_redefinir)
        # Ajuda
        menu_ajuda.addAction(self.action_sobre)
        menu_ajuda.addAction(self.action_ajuda)

        # Dial button
        self.dial_clock.setMaximum(10)
        self.dial_clock.setMinimum(0)
        self.dial_clock.setValue(0)
        self.dial_clock.setMaximumSize(QSize(30, 30))
        self.dial_clock.setToolTip('Ajustar clock')

        # Dial button screen
        self.lcd_clock_value.display(00)
        self.lcd_clock_value.setStyleSheet('border: 1px solid #4D5154;')
        self.lcd_clock_value.setMaximumWidth(60)

        # Disabling actions
        self.action_avancar.setDisabled(True)
        # self.action_ajustar_clock.setDisabled(True)
        self.action_fechar.setDisabled(True)

        # Toolbar:
        toolbar = self.addToolBar('Toolbar')

        # toobar style:
        toolbar.setStyleSheet(
            'QToolBar{'
            'background-color: #3C3F41;'
            # 'spacing: 3px'
            '}'
            'QToolButton:hover{'
            'border-style: none;'
            'background-color: #596064;'
            'border-radius: 4px;}'
            'QToolTip{'
            'color: #27292A;}'
            'QToolbar:separator{'
            'background-color: red;}')
        toolbar.setFloatable(False)
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(20, 20))

        toolbar.addAction(self.action_salvar)
        toolbar.addAction(self.action_abrir)
        toolbar.addSeparator()
        toolbar.addAction(self.action_traduzir)
        toolbar.addAction(self.action_executar)
        toolbar.addSeparator()
        toolbar.addAction(self.action_executar_etapas)
        toolbar.addAction(self.action_avancar)
        toolbar.addSeparator()

        toolbar.addWidget(self.dial_clock)

        toolbar.addWidget(self.lcd_clock_value)

        # seconds label
        lbl_segundos = QLabel('s')
        lbl_segundos.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        lbl_segundos.setStyleSheet('font-size: 15px;color: #9BAEC1')
        toolbar.addWidget(lbl_segundos)

    ##
    # Shows information dialog box
    #
    # @param title to the dialog
    # @param error message to present
    # @param detail of the error
    #
    def show_info_dialog(self, title, error, detail):
        dialog_box = QMessageBox()
        dialog_box.setWindowIcon(QIcon(self.icon_name))
        dialog_box.setWindowTitle(title)
        dialog_box.setText(error)
        dialog_box.setDetailedText(detail)
        dialog_box.setDefaultButton(QMessageBox.Ok)

        dialog_box.exec_()

    ##
    # Shows about dialog box
    #
    def show_about(self):
        about = QMessageBox()
        about.setStyleSheet('background-color: goldenrod;color:red;')
        about.about(
            self,
            'Sobre o kindA',
            'kindA versão 1.0 (11/2020)\n\n\nAutor: Nathaniel Ramalho')
        # about.show()


##
# Class thats models the editor window of the interface
#
class EditorFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(
                           'QFrame{'
                           'background-color: #2d2d2d;}'
                           'QTabWidget{'
                           'background-color: #333333;}'
                           'QTabBar:tab{'
                           'background-color: #3C3F41;'
                           'color: #9BAEC1}'
                           'QTabBar:tab:hover{'
                           'background-color: #27292A;}'
                           'QTabBar:tab:selected{'
                           'background-color: #4D5154;}')

        self.code_editor = CodeEditor()
        self.memory_table = MemoryTable()

        hbox_frame_editor_main = QHBoxLayout()

        self.tab_widget_main = QTabWidget()
        self.tab_widget_main.addTab(self.code_editor, 'Editor')
        self.tab_widget_main.addTab(self.memory_table, 'Memória Principal')

        hbox_frame_editor_main.addWidget(self.tab_widget_main)
        hbox_frame_editor_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(hbox_frame_editor_main)

    ##
    # Resturns the current text of the editor
    #
    def get_editor_text(self):
        return self.code_editor.toPlainText()


##
# Class that models memory window at the graphic interface
#
class MemoryTable(QTableWidget):
    COLUMN_COUNT = 4
    DEFAULT_ROW_COUNT = 0

    def __init__(self):
        super().__init__()

        self.setColumnCount(self.COLUMN_COUNT)

        self.setRowCount(self.DEFAULT_ROW_COUNT)

        self.configure()

    ##
    # Configures the window
    #
    def configure(self):
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setAlternatingRowColors(True)

        self.setStyleSheet('QTableWidget{'
                           'alternate-background-color: #2D2D2D;'
                           'background-color: #323232;'
                           'color: #9BAEC1}'
                           'QHeaderView:section{'
                           'background-color: #3C3F41;'
                           'color: #AEAEAE;'
                           'border-style: none;}')

        # para ocupar toda a janela:
        # ultima coluna se expande ate o final
        self.horizontalHeader().setStretchLastSection(True)
        # distribui igualmente o tamanho das colunas
        # self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # ajustando o tamanho das colunas
        # não funciona com o set sectio rezise mode
        # self.setColumnWidth(1, 300)

        # self.table.setStyleSheet('alternate-background-color: pink; background-color: cyan')

        self.setHorizontalHeaderLabels(['Endereço',
                                        'Valor',
                                        'Código',
                                        'Cód. Endereço'])
        self.verticalHeader().hide()

        self.setRowCount(self.rowCount() + 10)
        self.setItem(0, 0, QTableWidgetItem('adicionando um item'))


##
# Class that creates PC and IR display window
#
class PCFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet('background-color: #2d2d2d')

        self.frame_pc = QFrame()

        self.setMaximumWidth(150)
        self.setMinimumWidth(150)

        self.lbl_pc_value = QLabel('0x00000000')
        self.lbl_pc_value.setStyleSheet('background-color: lightgray')
        self.lbl_register_value = QLabel('0x00000000')
        self.lbl_register_value.setStyleSheet('background-color: lightgray')

        self.configure()

    ##
    # Configures the window
    #
    def configure(self):
        hbox_main_layout = QVBoxLayout()

        # creating frames
        frame_register = QFrame()

        # frames style
        # pc
        vbox_inside_pc = QVBoxLayout()
        vbox_inside_pc.setContentsMargins(0, 0, 0, 0)
        self.frame_pc.setStyleSheet(
            'background-color: #2D2D2D;'
            'border-radius: 8px;'
            'border: 2px solid #00BBFF;'
            'color: white')
        self.frame_pc.setMaximumHeight(105)
        self.frame_pc.setMaximumWidth(105)
        self.frame_pc.setMinimumWidth(105)
        self.frame_pc.setMinimumHeight(105)
        lbl_title_pc = QLabel('PC')
        lbl_title_pc.setAlignment(Qt.AlignCenter)
        lbl_title_pc.setStyleSheet(
            'background-color: transparent; '
            # 'font-weight: bold;'
            'font-size: 20px;'
            'border-style: none')
        self.lbl_pc_value.setAlignment(Qt.AlignCenter)
        self.lbl_pc_value.setStyleSheet(
            'background-color: transparent; '
            'font-weight: bold;'
            'font-size: 12px;'
            'border-style: none')
        vbox_inside_pc.addWidget(lbl_title_pc)
        vbox_inside_pc.addWidget(self.lbl_pc_value)
        self.frame_pc.setLayout(vbox_inside_pc)

        # register
        vbox_inside_register = QVBoxLayout()
        vbox_inside_register.setContentsMargins(0, 0, 0, 0)

        frame_register.setMinimumWidth(105)
        frame_register.setMinimumHeight(105)
        frame_register.setMaximumWidth(105)
        frame_register.setMaximumHeight(105)
        frame_register.setStyleSheet(
            'background-color: #2d2d2d;'
            'border-radius: 8px;'
            'border: 2px solid #00BBFF;'
            'color: white;')

        lbl_title_register = QLabel('IR')
        lbl_title_register.setAlignment(Qt.AlignCenter)
        lbl_title_register.setStyleSheet(
            'background-color: transparent; '
            # 'font-weight: bold;'
            'font-size: 20px;'
            'border-style: none')

        self.lbl_register_value.setAlignment(Qt.AlignCenter)
        self.lbl_register_value.setStyleSheet(
            'background-color: transparent; '
            'font-weight: bold;'
            'font-size: 12px;'
            'border-style: none;')
        vbox_inside_register.addWidget(lbl_title_register)
        vbox_inside_register.addWidget(self.lbl_register_value)

        frame_register.setLayout(vbox_inside_register)

        hbox_main_layout.addWidget(self.frame_pc)
        hbox_main_layout.addWidget(frame_register)
        hbox_main_layout.setAlignment(self.frame_pc, Qt.AlignHCenter)
        hbox_main_layout.setAlignment(frame_register, Qt.AlignHCenter)

        self.setLayout(hbox_main_layout)


##
# Class that models register window at the graphic interface
#
class RegisterFrame(QFrame):
    def __init__(self):
        super().__init__()

        # self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet('QFrame{background-color: #2d2d2d;}')
        self.setMinimumWidth(45)

        self.table_register = QTableWidget()

        self.configure()

    ##
    # Configures the window
    #
    def configure(self):
        # NOVO TITULO:
        # console title bar
        frame_title = QFrame()
        frame_title.setStyleSheet(
            'QFrame{'
            'background-color: #27292A;'
            'border-top: 1px solid #828790;'
            'border-left: 1px solid #828790;'
            'border-right: 1px solid #828790;'
            '}')
        frame_title.setMinimumHeight(25)

        tit_icon = QLabel()
        icon = QIcon('assets/icon_register.png')
        pixmap = icon.pixmap(QSize(14, 14))
        tit_icon.setPixmap(pixmap)
        tit_icon.resize(QSize(20, 20))
        tit_icon.setMaximumWidth(20)
        tit_icon.setStyleSheet('border-style: none;')

        tit_console = QLabel('Registradores')
        tit_console.setAlignment(Qt.AlignLeft)
        tit_console.setAlignment(Qt.AlignVCenter)
        tit_console.setStyleSheet(
            'Font-size: 12px;'
            'color:white;'
            'border-style: none')

        hbox_console_title_bar = QHBoxLayout()
        hbox_console_title_bar.setContentsMargins(5, 2, 0, 2)

        hbox_console_title_bar.addWidget(tit_icon, Qt.AlignLeft)
        hbox_console_title_bar.addWidget(tit_console, Qt.AlignLeft)

        frame_title.setLayout(hbox_console_title_bar)
        # NOVO TITULO:

        self.table_register.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_register.setColumnCount(2)
        self.table_register.setRowCount(8)
        self.table_register.setHorizontalHeaderLabels(['Valor', 'Código'])
        self.table_register.setVerticalHeaderLabels(['R0',
                                                     'R1',
                                                     'R2',
                                                     'R3',
                                                     'R4',
                                                     'R5',
                                                     'R6',
                                                     'R7'])
        # self.table_register.setMaximumHeight(266)
        self.table_register.setAlternatingRowColors(True)
        self.table_register.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table_register.setStyleSheet('QTableWidget{'
                                          'alternate-background-color: #2D2D2D;'
                                          'background-color: #323232;'
                                          'color: #9BAEC1;'
                                          'border-top: 1px solid red;'
                                          'border-bottom: 1px solid #828790;'
                                          'border-left: 1px solid #828790;'
                                          'border-right: 1px solid #828790;'
                                          '}'
                                          'QHeaderView:section:vertical{color: #00BBFF}'
                                          'QHeaderView:section{'
                                          'background-color: #3C3F41;'
                                          'color: #AEAEAE;'
                                          'border-style: none;}'
                                          'QTableCornerButton:section{'
                                          'background-color: #27292A;}')

        self.table_register.verticalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        hbox_register_frame = QVBoxLayout()
        hbox_register_frame.setContentsMargins(0, 0, 0, 0)

        hbox_register_frame.addWidget(frame_title)
        hbox_register_frame.addWidget(self.table_register)
        hbox_register_frame.setSpacing(0)

        self.setLayout(hbox_register_frame)


##
# Class that models Console window at the graphic interface
#
class ConsoleFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.list_widget_console = QListWidget()

        self.configure()

    ##
    # Configures the window
    #
    def configure(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setMinimumHeight(75)

        vbox_frame_console = QVBoxLayout()
        vbox_frame_console.setContentsMargins(0, 0, 0, 0)
        vbox_frame_console.setSpacing(0)

        # console title bar
        frame_title = QFrame()
        frame_title.setStyleSheet('background-color: #1d1d1d')

        tit_icon = QLabel()
        icon = QIcon('assets/icon_console.png')
        pixmap = icon.pixmap(QSize(20, 20))
        tit_icon.setPixmap(pixmap)
        tit_icon.resize(QSize(20, 20))
        tit_icon.setMaximumWidth(20)

        tit_console = QLabel('Console')
        tit_console.setAlignment(Qt.AlignLeft)
        tit_console.setAlignment(Qt.AlignVCenter)
        tit_console.setStyleSheet(
            'Font-size: 12px;'
            'color:white')

        hbox_console_title_bar = QHBoxLayout()
        hbox_console_title_bar.setContentsMargins(5, 2, 0, 2)

        hbox_console_title_bar.addWidget(tit_icon, Qt.AlignLeft)
        hbox_console_title_bar.addWidget(tit_console, Qt.AlignLeft)

        frame_title.setLayout(hbox_console_title_bar)

        self.list_widget_console.setStyleSheet(
            'QListWidget{'
            'background-color: #244057; '
            'border-style: none;'
            'border-top: 1px solid red;'
            'padding: 5px;'
            'font-size: 13px;'
            'color: white;}'
            )

        vbox_frame_console.addWidget(frame_title)
        vbox_frame_console.addWidget(self.list_widget_console)

        self.setLayout(vbox_frame_console)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = Window()
    sys.exit(app.exec_())
