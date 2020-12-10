#!/usr/bin/env python
# coding: UTF-8
#
## @package virtual_machine
#
#   Class that models a virtual machine.
#
#   @author Nathaniel Ramalho
#   @since 11/28/2020
#
class VirtualMachine:
    AVAILABLE_REGISTERS = [0, 1, 2, 3, 4, 5, 6, 7]
    MAX_MEM_ADDRESS = 4294967296
    WORD_SIZE = 32
    BLOCKED_ADDRESS_KEY = 'freeze'

    def __init__(self, context):
        self.context = context

        self.registers = [0] * 8
        self.labels = dict()
        self.main_memory = dict()
        self.unblock_memory()
        self.pc = 0
        self.instruction_register = 0

    ##
    # Changes the value of a register
    # reaises *ValueError* if the value is invalid or if the
    # address is incorrect
    #
    # @param value that will be applied on register
    # @param is the address of the register
    # TODO: Documentar
    def set_register_value(self, value: int, register):
        if not isinstance(value, int):
            raise ValueError('Valor inválido para atribuição em registrador.')

        if register == 0:
            raise ValueError('O valor do "Registrador 0" não pode ser alterado.')

        if register not in self.AVAILABLE_REGISTERS:
            raise ValueError(f'O registrador {register} não existe.')

        self.registers[register] = value
        self.context.update_registers_table()

    ##
    # Returns the value of the register from a input address
    #
    # @param register address
    #
    def get_register_value(self, register):
        return self.registers[register]

    ##
    # Empties the main memory dictionary and unblocks the
    # protected adresses
    #
    def clear_main_memory(self):
        self.main_memory.clear()
        self.unblock_memory()

        self.context.clear_memory_table()

    ##
    # Blocks a range of main memory from index 0 to index received.
    #
    # @param last index that will be blocked
    #
    def block_memory(self, index):
        self.main_memory[self.BLOCKED_ADDRESS_KEY] = index

    ##
    # Unblock all memory addresses
    #
    def unblock_memory(self):
        self.main_memory[self.BLOCKED_ADDRESS_KEY] = -1

    ##
    # Returns the last blocked memory address
    #
    # @return last index of blocked memory
    #
    def get_blocked_memory_addresses(self):
        return self.main_memory[self.BLOCKED_ADDRESS_KEY]

    ##
    # Retrieves a value from memory at an informed address.
    #
    # @param address of main memory
    # @return data at the address
    def get_main_memory_value(self, address: int):
        if 0 <= address <= self.MAX_MEM_ADDRESS:
            try:
                data = self.main_memory[address]
            except KeyError:
                return 0
        else:
            # TODO: msg
            raise ValueError(f'O endereço "{address}" da memória principal não pode ser acessado.')

        return data

    ##
    # Assign a value to a main memory address
    #
    # @param value that will be stored
    # @param address that the date will be stored
    def set_main_memory_value(self, value, address):
        blocked_addresses = self.get_blocked_memory_addresses()

        if blocked_addresses >= 0:
            if 0 <= address <= blocked_addresses:
                raise MemoryError(f'O endereço {address} está bloqueado para gravação.')

        if 0 <= address <= self.MAX_MEM_ADDRESS:
            self.main_memory[address] = value
        else:
            raise ValueError(f'O endereço "{address}" da memória principal não pode ser acessado.')
        if blocked_addresses > -1:
            self.context.update_memory_table()

    ##
    # clears data from memory, registers, labels, etc. of the virtual machine
    #
    def reset_machine(self):
        self.reset_pc()
        self.clear_labels()
        self.clear_main_memory()
        self.clear_all_registers()
        self.instruction_register = 0

    ##
    # Cleans the virtual machine labels list
    #
    def clear_labels(self):
        self.labels.clear()

    ##
    # Adds a label to the labels dictionary
    # raises ValueError if the address is out of memory addresses range
    #
    # @param key is the label
    # @param value is memory address that contais the labeled instruction
    #
    def add_label(self, key, value):
        if 0 <= value <= self.MAX_MEM_ADDRESS:
            self.labels[key] = value
        else:
            raise ValueError(f'O label "{key}" aponta para um endereço '
                             f'de memória inválido.')

    ##
    # gets a label value
    #
    # @param key of the label
    # @return value of the label
    def get_label_value(self, key):
        try:
            value = self.labels[key]
        except KeyError as k:
            # TODO: msg
            raise ValueError(f'O label {k} não foi encontrado.')

        return value

    ##
    # Returns the value of the program counter
    #
    # @return self.pc value is returned
    def get_pc(self):
        return self.pc

    ##
    # Changes the value of the pc attribute if the value
    # passed is valid otherwise it raises an error
    #
    # @param value to be applied on pc
    def set_pc(self, value):
        if not isinstance(value, int):
            raise TypeError('PC somente recebe valores inteiros.')
        if value < -1:
            raise ValueError('Valor inválido para PC')
        self.pc = value
        self.context.update_ui_pc()
        self.context.update_ui_instruction_register()

    ##
    # Increments pc attribute
    #
    def increment_pc(self):
        self.pc += 1
        self.context.update_ui_pc()
        self.context.update_ui_instruction_register()

    ##
    # Sets pc value as zero
    #
    def reset_pc(self):
        self.pc = 0
        self.context.update_ui_pc()

    ##
    # Change all registers value to zero
    #
    def clear_all_registers(self):
        for i in range(len(self.registers)):
            self.registers[i] = 0

        self.context.update_registers_table()

    @property
    def instruction_register(self):
        return self._instruction_register

    @instruction_register.setter
    def instruction_register(self, value):
        self._instruction_register = value
        self.context.update_ui_instruction_register()

    ##
    # Creates a textual representation of the virtual machine and its properties values
    #
    def __repr__(self):
        msg = '==============================================================\n'
        msg += '=                    Máquina Virtual:                        =\n'
        msg += '==============================================================\n'
        msg += 'registradores:\t'
        for i, val in enumerate(self.registers):
            msg += f'r{i}: {val} | '
        msg += '\n'
        alt = '{'
        for i, k in enumerate(self.main_memory.keys()):
            if k == self.BLOCKED_ADDRESS_KEY:
                continue
            if i == self.pc:
                alt += '->'
            alt += f'{k}: \'{self.main_memory[k]}\', '
        alt += '}'
        msg += f'Memoria principal: {alt}\n'
        # msg += f'Memoria principal: {self.main_memory}\n'
        msg += f'Pc:\t{self.pc}\n'
        msg += f'Labels:\t{self.labels}\n'
        msg += f'registrador de instrução:\t{self.instruction_register}\n'
        msg += '==============================================================\n'

        return msg
