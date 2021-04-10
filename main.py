#!/usr/bin/env python
# coding: UTF-8
#
## @package main
#
#   Main program of kindA.
#
#   @author Nathaniel Ramalho
#   @since 10/03/2020
#
from PySide2.QtWidgets import QApplication, QListWidgetItem, QTableWidgetItem, QFileDialog
from PySide2.QtCore import Qt
from ui_help import Help
from ui_main_window import Window
from engine import Engine
from instruction_set import InstructionsUtils as Utils, Fill, Instruction
from assembler import Assembler
import sys


##
# Class that configures the Graphic User Interface
#
class MainWindow(Window):
    def __init__(self):
        super().__init__()

        # font = QFont("Sanserif", 12)
        # font.setStyleHint(QFont.SansSerif)
        # QApplication.setFont(font)

        self.is_external_document = False
        self.path_external_document = ''

        self.engine = Engine(self)

        self.configure_actions()

        self.help_dialog = None

        self.clear_registers_table()
        self.clear_console()
        self.clear_memory_table()

        self.configure_clock_widgets()

        self.log_on_console('Systema pronto.')
        self.console_space()

    ##
    #   Method that configures the action from GUI Model
    #
    def configure_actions(self):
        # Arquivo
        self.action_salvar.triggered.connect(self.file_save)
        self.action_salvar_como.triggered.connect(self.file_save_as)
        self.action_exportar.triggered.connect(self.file_export)
        self.action_abrir.triggered.connect(self.file_open)
        self.action_fechar.triggered.connect(self.file_close)
        self.action_sair.triggered.connect(self.close_application)
        # Executar
        self.action_executar.triggered.connect(self.execute)
        self.action_executar_etapas.triggered.connect(self.run_in_steps)
        self.action_avancar.triggered.connect(self.step_foward)
        self.action_traduzir.triggered.connect(self.translate)
        self.action_redefinir.triggered.connect(self.reset_virtual_machine)
        # Ajuda
        self.action_sobre.triggered.connect(self.open_about)
        self.action_ajuda.triggered.connect(self.open_help)

    ##
    # Configures the start value of the graphic
    # control that changes the clock speed
    #
    def configure_clock_widgets(self):
        # setting up initial values
        clock = self.engine.clock
        self.dial_clock.setValue(clock * 10)
        self.lcd_clock_value.display(clock)

        # triggering dial button
        self.dial_clock.valueChanged.connect(self.change_clock)

    ##
    # Method called to change the engine clock
    #
    def change_clock(self):
        clock_value = self.dial_clock.value() / 10
        self.lcd_clock_value.display(clock_value)
        self.engine.set_clock(clock_value)

    ##
    # Save current open file or calls save all dialog to save a new file
    #
    def file_save(self):
        if not self.is_external_document:
            self.file_save_as()
            return

        path = self.path_external_document
        try:
            with open(path, 'w') as f:
                text = self.frame_editor.code_editor.toPlainText()
                f.write(text)
        except OSError as err:
            error = 'Falha ao salvar o arquivo'
            detail = f'Erro interno ao salvar: {err}'
            title = 'Salvar...'
            self.show_info_dialog(title, error, detail)

    ##
    # Opens a dialog box to save the current code as a new file
    #
    def file_save_as(self, export=None):
        file_type = 'Código Fonte (*.asc)'
        if export:
            file_type = 'Binario (*.mc)'

        file = QFileDialog.getSaveFileName(self,
                                           'Salvar como...',
                                           '',
                                           f'{file_type};;'
                                           'Todos os arquivos (*.*)')
        try:
            if not file[0]:
                # user Canceled
                return
        except IndexError as err:
            error = 'Falha ao salvar o arquivo'
            detail = f'Erro interno ao salvar: {err}'
            title = 'Salvar como...'
            self.show_info_dialog(title, error, detail)

        try:
            with open(file[0], 'w') as f:
                text = self.frame_editor.code_editor.toPlainText()
                f.write(text)
                self.is_external_document = True
                self.path_external_document = file
                self.action_fechar.setDisabled(False)
        except OSError as err:
            error = 'Falha ao salvar o arquivo.'
            detail = f'Erro interno ao salvar: {err}'
            title = 'Salvar como...'
            self.show_info_dialog(title, error, detail)

    ##
    # Converts current code to binary the opens a dialog
    # to save the converted file
    #
    def file_export(self):
        title = 'Exportar...'

        file = QFileDialog.getSaveFileName(self,
                                           'Exportar para binário...',
                                           '',
                                           'Binário (*.mc);;'
                                           'Todos os arquivos (*.*)')
        try:
            if not file[0]:
                # user Canceled/ close dialog
                return
        except IndexError as err:
            self.log_on_console(f'Erro Interno: {err}')

        self.engine.create_virtual_machine()
        vm = self.engine.virtual_machine

        text = self.frame_editor.code_editor.toPlainText()
        output = ''
        try:
            assembler = Assembler()
            instructions = assembler.assemble(text)
            for i, inst in enumerate(instructions):
                output += inst.get_hexa_representation(vm)
                if i < len(instructions):
                    output += '\n'

            with open(file[0], 'w') as f:
                f.write(output)
        except ValueError as err:
            error = 'Falha ao exportar o arquivo.'
            detail = f'Ocorreu um erro na tradução. (Erro: {err})'

            self.show_info_dialog(title, error, detail)
        except OSError:
            error = 'Não foi possivel Exportar o arquivo.'
            detail = 'Verifique se você tem permissão para ' \
                     'salvar arquivos no local selecionado.'
            self.show_info_dialog(title, error, detail)

    ##
    # Opens a dialog to load a file.
    #
    def file_open(self):
        # todo: ver mais opções de qfile dialog. get openfile name
        name = QFileDialog.getOpenFileName(self,
                                           'Abrir arquivo',
                                           '',
                                           'Arquivos kindA (*.asc *.mc);'
                                           ';Código Fonte (*.asc);'
                                           '; Binário (*.mc);'
                                           ';Todos os Arquivos (*.*)')

        try:
            if not name[0]:
                return
        except IndexError as err:
            self.log_on_console(f'Erro Interno: {err}')
            error = 'Falha ao abrir o arquivo'
            detail = f'Erro interno ao tentar abrir o arquivo: {err}'
            title = 'Abrir...'
            self.show_info_dialog(title, error, detail)

        try:
            with open(name[0], 'r') as f:
                text = f.read()
                self.frame_editor.code_editor.setPlainText(text)
                self.path_external_document = name[0]
                self.is_external_document = True
                self.action_fechar.setDisabled(False)
                self.open_code_editor_tab()
        except UnicodeDecodeError as err:
            # todo: tratar melhor essa exceção
            error = 'Falha ao abrir o arquivo'
            detail = f'Arquivo inválido: {err}'
            title = 'Abrir...'
            self.show_info_dialog(title, error, detail)

    ##
    # Closes current document
    #
    def file_close(self):
        self.frame_editor.code_editor.clear()
        self.is_external_document = False
        self.path_external_document = ''
        self.action_fechar.setDisabled(True)

    ##
    # Finishes software execution
    #
    def close_application(self):
        self.close()

    ##
    # Prepares the interface and the engine for the execution of a
    # source code
    #
    def execute(self):
        self.clear_console()
        self.clear_memory_table()
        self.log_on_console('Executando...')
        self.change_pc_bg()
        text = self.frame_editor.get_editor_text()

        self.engine.run(text)

    ##
    # Enables the execution button.
    #
    def enable_execution_button(self):
        self.action_executar.setDisabled(False)

    ##
    # Prepares the interface and the engine for the execution of a
    # source code in step execution mode
    #
    def run_in_steps(self):
        self.clear_console()
        self.clear_memory_table()
        self.log_on_console('Execução em Etapas:')
        text = self.frame_editor.get_editor_text()
        self.engine.run_in_steps(text)

    ##
    # Allows you to proceed with the execution if you are
    # in step execution mode
    #
    def step_foward(self):
        self.engine.step_foward()

    ##
    # calls the engine translation method and prepares
    # the interface to receive the updated data
    #
    def translate(self):
        self.clear_memory_table()
        self.log_on_console('Traduzindo...')
        text = self.frame_editor.get_editor_text()

        try:
            self.engine.translate(text)
        except ValueError as err:
            self.log_on_console(err)

    ##
    # call the virtual machine method that reset itself data
    #
    def reset_virtual_machine(self):
        vm = self.engine.virtual_machine
        if vm is not None:
            vm.reset_machine()

    ##
    # Opens about dialog
    #
    def open_about(self):
        self.show_about()

    ##
    # Opens Help Dialog
    #
    def open_help(self):
        self.help_dialog = Help()
        self.help_dialog.show()

    ##
    # Writes passed information into graphic interface console.
    #
    # @param text that will be shown on console
    def log_on_console(self, text):
        self.frame_console.list_widget_console.addItem(
            QListWidgetItem(str(f'{text}')))
        self.frame_console.repaint()

        self.frame_console.list_widget_console.scrollToBottom()

    ##
    # Clears all console texts
    #
    def clear_console(self):
        while self.frame_console.list_widget_console.count() > 0:
            self.frame_console.list_widget_console.takeItem(0)

    ##
    # Skip a link on cosole
    #
    def console_space(self):
        self.log_on_console('')

    ##
    # Updates the registers table
    #
    def update_registers_table(self):
        regs = self.engine.virtual_machine.registers
        for i, v in enumerate(regs):
            item_widget_table = QTableWidgetItem(str(v))
            item_widget_table.setTextAlignment(Qt.AlignCenter)
            self.frame_register.table_register.setItem(i, 0, item_widget_table)
            v = Utils.convert_to_binary_twos_complement(v, 32)
            v = Utils.convert_binary_to_hexadecimal(v)
            v = '0x' + v
            self.frame_register.table_register.setItem(i, 1, QTableWidgetItem(v))
            self.frame_register.table_register.repaint()

    ##
    # Completely clears the registers table
    #
    def clear_registers_table(self):
        row = self.frame_register.table_register.rowCount()
        for i in range(row):

            item_table_widget = QTableWidgetItem('0')
            item_table_widget.setTextAlignment(Qt.AlignCenter)

            item_table_widget_hex = QTableWidgetItem('0x00000000')
            item_table_widget_hex.setTextAlignment(Qt.AlignCenter)

            self.frame_register.table_register.setItem(i, 0, item_table_widget)
            self.frame_register.table_register.setItem(i, 1, item_table_widget_hex)

    ##
    # Updates the UI memory table
    #
    def update_memory_table(self):
        memory = dict(self.engine.virtual_machine.main_memory)
        table = self.frame_editor.memory_table
        queue = self.engine.execution_queue

        if self.engine.virtual_machine.BLOCKED_ADDRESS_KEY in memory.keys():
            blocked = memory.pop(self.engine.virtual_machine.BLOCKED_ADDRESS_KEY)

        table.setRowCount(table.DEFAULT_ROW_COUNT)

        for i, k in enumerate(memory.keys()):
            # Adding new row:
            table.setRowCount(table.rowCount() + 1)

            # Address integer representation
            table.setItem(i, 0, QTableWidgetItem(str(k)))

            vm = self.engine.virtual_machine
            # if index < len(queue) and if Instruction
            # else

            if i < len(queue) and (isinstance(queue[i], Instruction) or isinstance(queue[i], Fill)):
                inst_hexa = '0x' + queue[k].get_hexa_representation(vm)
                inst_str = str(queue[k])
            else:
                f = Fill(None, [memory[k]])
                inst_hexa = '0x' + f.get_hexa_representation(vm)
                inst_str = str(memory[k])

            # Add the instruction at i 1
            table.setItem(i, 1, QTableWidgetItem(inst_str))

            # Add hexadecimal representation on i 2
            table.setItem(i, 2, QTableWidgetItem(inst_hexa))

            # Add the hexadecimas address on i 3
            # Converting the address:
            hexa_address = Utils.convert_to_hexadecimal(k, 8)
            hexa_address = '0x' + hexa_address
            table.setItem(i, 3, QTableWidgetItem(hexa_address))

        self.frame_editor.memory_table.repaint()
        self.open_memory_table()

    ##
    # Clean the memory table
    #
    def clear_memory_table(self):
        # clear limpa os headers...
        # self.frame_editor.memory_table.clear()
        table = self.frame_editor.memory_table
        rows = table.rowCount()
        cols = table.columnCount()
        for i in range(rows):
            for j in range(cols):
                table.setItem(i, j, QTableWidgetItem(''))
            table.removeRow(i)

        table.setRowCount(0)

    ##
    # selects a row from the memory table
    #
    def select_memory_table_row(self, row):
        table = self.frame_editor.memory_table
        if row <= table.rowCount():
            table.selectRow(row)

    ##
    # Brings the memory table tab to front
    #
    def open_memory_table(self):
        self.select_memory_table_row(0)
        self.frame_editor.tab_widget_main.setCurrentIndex(1)

    ##
    # Brings the Code Editor tab to front
    #
    def open_code_editor_tab(self):
        self.frame_editor.tab_widget_main.setCurrentIndex(0)

    ##
    # Updates the program counter display
    #
    def update_ui_pc(self):
        int_pc_value = self.engine.virtual_machine.get_pc()
        pc_value = '0x' + Utils.convert_to_hexadecimal(int_pc_value, 8)

        self.frame_pc.lbl_pc_value.setText(pc_value)
        self.select_memory_table_row(int_pc_value)
        self.frame_pc.lbl_pc_value.repaint()

    ##
    # Changes the program counter display background color
    #
    def change_pc_bg(self):
        self.frame_pc.frame_pc.setStyleSheet(
            'background-color: #17B36E;'
            'border-radius: 8px;'
            'border: 2px solid #00BBFF;'
            'color: white')

    ##
    # Changes the PC display back to default background color
    #
    def change_back_pc_bg(self):
        self.frame_pc.frame_pc.setStyleSheet(
            'background-color: #2D2D2D;'
            'border-radius: 8px;'
            'border: 2px solid #00BBFF;'
            'color: white')

    ##
    # Updates the instruction Register display value
    #
    def update_ui_instruction_register(self):
        vm = self.engine.virtual_machine
        running_status = self.engine.status.is_running
        no_instruction = False

        if vm is not None:
            if vm.instruction_register == 0 and not running_status:
                no_instruction = True
            else:
                pc = vm.get_pc()
                if self.engine.is_valid_pc(pc):
                    inst = self.engine.execution_queue[pc]

                    representation = inst.get_hexa_representation(vm)
                    representation = '0x' + str(representation)

                    self.frame_pc.lbl_register_value.setText(representation)
        else:
            no_instruction = True

        if no_instruction:
            self.frame_pc.lbl_register_value.setText('0x00000000')

        self.frame_pc.lbl_register_value.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
