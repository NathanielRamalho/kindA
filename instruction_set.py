#!/usr/bin/env python
# coding: UTF-8
#
## @package instruction_set
#
#   Modeling the instructions.
#
#   @author Nathaniel Ramalho
#   @since 11/28/2020
#
from virtual_machine import VirtualMachine


##
# InstructionsUtils class has utilitarian methods for the instruction classes
#
class InstructionsUtils:
    INSTRUCTION_LABELS = ['add',
                          'addi',
                          'lw',
                          'sw',
                          'beq',
                          'jalr',
                          'halt',
                          'noop',
                          '.fill']

    ##
    # Returns a list of all labels for instructions and directives.
    #
    # @return list of all instructions and diretives names.
    def get_labels(self):
        return self.INSTRUCTION_LABELS

    ##
    # Checks whether the value of an operator for a register
    # contains correct information so that it can be converted
    # into an integer within the limit established by the
    # signature machine.
    #
    # @param reg given data
    # @return reg converted in integer
    @staticmethod
    def validate_register_operator(reg):
        exception_msg_type = 'O registrador deve ser um número inteiro positivo.'
        exception_msg_not_found = f'O "registrador {reg}" não existe.'

        if isinstance(reg, str):
            if reg.isnumeric():
                reg = int(reg)
            else:
                raise ValueError(exception_msg_type)
        else:
            if isinstance(reg, int):
                if reg < 0:
                    raise ValueError(exception_msg_type)
            else:
                raise ValueError(exception_msg_type)

        if reg not in VirtualMachine.AVAILABLE_REGISTERS:
            raise ValueError(exception_msg_not_found)

        return reg

    ##
    # Checks whether a given name refers to a valid instruction set instruction
    #
    # @param the name you want to check
    # @return True if its a valid name
    #
    def is_valid_instruction_name(self, name):
        if name in self.INSTRUCTION_LABELS:
            return True
        else:
            return False

    ##
    # Converts the passed value to a encoded value that represents a register
    #
    # @return input translated to binary.
    #
    @staticmethod
    def convert_register_to_binary(reg):
        converted = bin(reg)[2:]
        converted = '0' * (3 - len(converted)) + converted
        return converted

    ##
    # Converts a value to binary in the representation in two's complement.
    # raises an exception if the number cannot be represented.
    #
    # @param value to convert
    # @param word_size size of the memory word size
    # @return value converted to binaty Two's Complement.
    #
    @staticmethod
    def convert_to_binary_twos_complement(value: int, word_size) -> str:
        # Max and Min representation that word size allows.
        low_limit = -1 * 2 ** (word_size - 1)
        high_limit = (2 ** (word_size - 1)) - 1

        if value < low_limit or value > high_limit:
            raise ValueError('Overflow')

        # Convertion
        if value >= 0:
            value = bin(value)[2:]
            value = '0' * (word_size - len(value)) + value
        else:
            value = (value * -1) - 1
            value = bin(value)[2:]
            inverted = ''
            for digit in value:
                if digit == '0':
                    inverted += '1'
                else:
                    inverted += '0'
            inverted = '1' * (word_size - len(inverted)) + inverted
            value = inverted

        return value

    ##
    # Converts a binary number to hexadecimal
    #
    # @param is an integer on string format
    # @return hexadecimal representatio
    # todo: documentar em inglês
    @staticmethod
    def convert_binary_to_hexadecimal(num: str):
        num = hex(int(num, 2))[2:]
        num = '0' * (int(VirtualMachine.WORD_SIZE / 4) - len(num)) + num
        output = ''

        for ch in num:
            if ch.isalpha():
                ch = ch.upper()
            output += ch

        return output

    ##
    # Convert an integer value to a hexadecimal representation
    #
    # @param value to convert
    # @param memory word size
    #
    @staticmethod
    def convert_to_hexadecimal(value: int, word_size) -> str:
        result = hex(value)[2:]
        result = '0' * (word_size - len(result)) + result
        return result

    ##
    # Returns the name of an instruction from a code.
    # raises *ValueError* if the parameter contais incorrect data
    #
    # @param code that may represent an instruction if correct.
    #
    def get_name_by_code(self, val):
        if 0 <= val <= len(self.INSTRUCTION_LABELS) - 1:
            return self.INSTRUCTION_LABELS[val]
        else:
            raise ValueError('Decodificação: Código de instrução inválido.')

    ##
    # Converts a number encoded in binary two's complement to an integer.
    # rases a *ValueError* if something unnexpexted happens.
    #
    # returns the converted version of the passes value
    #
    @staticmethod
    def twos_complement_binary_to_int(val):
        output = ''
        if val[0] == '0':
            try:
                output = int(val[1:], 2)
            except ValueError as err:
                raise ValueError(f'Erro de decodificação: {err}')
        else:
            for ch in val:
                if ch == '0':
                    output += '1'
                else:
                    output += '0'
            try:
                output = int(output, 2) + 1
            except ValueError as err:
                raise ValueError(f'Erro de decodificação: {err}')
            output *= -1

        return output


##
# It is an abstract class from which all instructions inherits
#
# todo: documentar
class Instruction:
    INSTRUCTION_CODE = 'super'

    ##
    # Constructor Method
    #
    def __init__(self):
        self.address = None

    ##
    # Allows you to assign a value to the address attribute
    #
    # @param address to assign os attribute.
    #
    def set_address(self, address):
        self.address = address

    ##
    # Abstract method that represents the Instructions operations.
    #
    def execute(self, virtual_machine):
        return True

    ##
    # Returns the hexadecimal representation of the instruction
    #
    def get_hexa_representation(self, *args):
        return self.INSTRUCTION_CODE


##
# It is an abstract class from which Addi, Lw, Sw and
# Beq instructions classes inherits.
#
# @see Addi
# @see Lw
# @see Sw
# @see Beq
#
class TwoRegistersInstruction(Instruction):
    ATTRIBUTE_NAME = '"NÃO DEFINIDO"'
    INSTRUCTION_NAME = '"Two Register Instruction"'
    INSTRUCTION_CODE = 'Superclass TwoRegistersIntruction'

    def __init__(self, la, ops):
        super().__init__()
        self.label = la
        if len(ops) >= 3:
            self.reg_a = ops[0]
            self.reg_b = ops[1]
            self.value = ops[2]
        else:
            raise ValueError('Não há argumentos suficientes para a operação (necessário: 3)')

    @property
    def reg_a(self):
        return self._reg_a

    @reg_a.setter
    def reg_a(self, value):
        try:
            value = InstructionsUtils.validate_register_operator(value)
        except ValueError as err:
            raise ValueError(f'Argumento 1: {err}')
        self._reg_a = value

    @property
    def reg_b(self):
        return self._reg_b

    @reg_b.setter
    def reg_b(self, value):
        try:
            value = InstructionsUtils.validate_register_operator(value)
        except ValueError as err:
            raise ValueError(f'Argumento 2: {err}')
        self._reg_b = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        negative = False
        if isinstance(value, str):
            if value[0] == '-':
                if value[1:].isnumeric():
                    negative = True
                    value = value[1:]
            if value.isnumeric():
                value = int(value)
                if negative:
                    value *= -1
            else:
                if not value.isalnum():
                    raise ValueError(f'Argumento 3: O valor passado ("{value}") '
                                     f'deve ser um inteiro ou um label válido.')
        elif not isinstance(value, int):
            raise ValueError(f'Argumento 3: O valor {self.ATTRIBUTE_NAME} '
                             f'deve ser um label ou um número inteiro.')

        self._value = value

    ##
    # Covert the instruction to a hexadecimal representation.
    #
    # @param vm is a VirtualMachine class Object
    # @return hexadecimal representation
    def get_hexa_representation(self, vm):
        if isinstance(self.value, str):
            try:
                value = vm.get_label_value(self.value)
            except ValueError as err:
                raise ValueError(f'Não foi possível converter a '
                                 f'instrução para hexadecimal. {err}')
        else:
            value = self.value

        prefix = '0000000'
        utils = InstructionsUtils()

        rega = utils.convert_register_to_binary(self.reg_a)
        regb = utils.convert_register_to_binary(self.reg_b)
        try:
            value = utils.convert_to_binary_twos_complement(value, 16)
        except ValueError as err:
            raise ValueError(err)

        binary_representation = prefix + self.INSTRUCTION_CODE + rega + regb + value
        output = utils.convert_binary_to_hexadecimal(binary_representation)
        return output

    ##
    # returns the representation of the instruction in pseudocode
    #
    def __repr__(self):
        return f'{self.INSTRUCTION_NAME} {self.reg_a} {self.reg_b} {self.value}'


##
# Class implements the functionality of the "add" instruction.
# raises a *ValueError* if receives invalid parameters
#
# @param la: a string containing a label or None
# @param ops: a list with some operator an optionaly a comment
#
class Add(Instruction):
    INSTRUCTION_NAME = 'add'
    INSTRUCTION_CODE = '000'

    def __init__(self, la, ops):
        super().__init__()
        self.label = la

        # check if there are enough operands for object
        # initialization
        if len(ops) >= 3:
            self.reg_a = ops[0]
            self.reg_b = ops[1]
            self.reg_dest = ops[2]
        else:
            raise ValueError('Não há argumentos suficientes para a operação. (necessários: 3)')

    @property
    def reg_a(self):
        return self._reg_a

    @reg_a.setter
    def reg_a(self, value):
        try:
            value = InstructionsUtils.validate_register_operator(value)
        except ValueError as err:
            raise ValueError(f'Argumento 1: {err}')
        self._reg_a = value

    @property
    def reg_b(self):
        return self._reg_b

    @reg_b.setter
    def reg_b(self, value):
        try:
            value = InstructionsUtils.validate_register_operator(value)
        except ValueError as err:
            raise ValueError(f'Argumento 2: {err}')
        self._reg_b = value

    @property
    def reg_dest(self):
        return self._reg_dest

    @reg_dest.setter
    def reg_dest(self, value):
        try:
            value = InstructionsUtils.validate_register_operator(value)
        except ValueError as err:
            raise ValueError(f'Argumento 3: {err}')
        self._reg_dest = value

    ##
    # Performs the operation of the add instruction
    #
    def execute(self, vm):
        value_a = vm.get_register_value(self._reg_a)
        value_b = vm.get_register_value(self._reg_b)
        try:
            result = int(value_a + value_b)
            vm.set_register_value(result, self.reg_dest)
        except ValueError as err:
            # todo: msg
            raise ValueError(f'Erro de Execução: {err}')

        return True

    ##
    # Covert the instruction to a hexadecimal representation.
    #
    # @param vm is a VirtualMachine class Object
    # @return hexadecimal representation
    def get_hexa_representation(self, *args):
        utils = InstructionsUtils()
        prefix = '0' * 7
        rega = utils.convert_register_to_binary(self.reg_a)
        regb = utils.convert_register_to_binary(self.reg_b)
        regdest_complement = '0' * 13
        regdest = utils.convert_register_to_binary(self.reg_dest)

        bin_representation = prefix + rega + regb + regdest_complement + regdest
        output = utils.convert_binary_to_hexadecimal(bin_representation)

        return output

    ##
    # returns the representation of the instruction in pseudocode
    #
    def __repr__(self):
        return f'{self.INSTRUCTION_NAME} {self.reg_a} {self.reg_b} {self.reg_dest}'


##
# Class that implements the Addi instruction
#
class Addi(TwoRegistersInstruction):
    INSTRUCTION_NAME = 'addi'
    INSTRUCTION_CODE = '001'
    ATTRIBUTE_NAME = 'Imediato'

    def __init__(self, la, ops):
        super().__init__(la, ops)
        self.immediate = self.value

    ##
    # Performs the operation of the addi instruction
    #
    def execute(self, vm):
        value_a = vm.get_register_value(self.reg_a)

        try:
            if isinstance(self.immediate, str):
                immediate = vm.get_label_value(self.immediate)
            else:
                immediate = self.immediate

            result = int(value_a + immediate)
            vm.set_register_value(result, self.reg_b)
        except ValueError as err:
            raise ValueError(f'Erro de Execução: {err}')

        return True


##
# Class that implements the lw instruction
#
class Lw(TwoRegistersInstruction):
    INSTRUCTION_NAME = 'lw'
    INSTRUCTION_CODE = '010'
    ATTRIBUTE_NAME = 'Deslocamento'

    def __init__(self, la, ops):
        super().__init__(la, ops)
        self.displacement = self.value

    ##
    # Performs the operation of the lw instruction
    #
    def execute(self, vm):
        value_a = vm.get_register_value(self.reg_a)

        try:
            if isinstance(self.displacement, str):
                displacement = vm.get_label_value(self.displacement)
            else:
                displacement = self.displacement

            address = int(value_a + displacement)

            data = vm.get_main_memory_value(address)
            data = int(data)

            vm.set_register_value(data, self.reg_b)

        except ValueError as err:
            raise ValueError(f'Erro de Execução: {err}')

        return True


##
# Class that implements the sw instruction
#
class Sw(TwoRegistersInstruction):
    INSTRUCTION_NAME = 'sw'
    INSTRUCTION_CODE = '011'
    ATTRIBUTE_NAME = 'Deslocamento'

    def __init__(self, la, ops):
        super().__init__(la, ops)
        self.label = la
        self.displacement = self.value

    ##
    # Performs the operation of the sw instruction
    #
    def execute(self, vm):
        value_on_reg_a = vm.get_register_value(self.reg_a)

        try:
            if isinstance(self.displacement, str):
                displacement = vm.get_label_value(self.displacement)
            else:
                displacement = self.displacement

            address = int(value_on_reg_a + displacement)

            data = vm.get_register_value(self._reg_b)
            vm.set_main_memory_value(data, address)
        except (ValueError, MemoryError) as err:
            raise ValueError(f'Erro de Execução: {err}')

        return True


##
# Class that implements the beq instruction
#
class Beq(TwoRegistersInstruction):
    INSTRUCTION_NAME = 'beq'
    INSTRUCTION_CODE = '100'
    ATTRIBUTE_NAME = 'Deslocamento'

    def __init__(self, la, ops):
        super().__init__(la, ops)
        self.displacement = self.value

    ##
    # Performs the operation of the beq instruction
    #
    def execute(self, vm):
        value_reg_a = vm.get_register_value(self.reg_a)
        value_reg_b = vm.get_register_value(self.reg_b)
        using_label = False

        try:
            if isinstance(self.displacement, str):
                displacement = vm.get_label_value(self.displacement)
                using_label = True
            else:
                displacement = self.displacement

            if value_reg_a == value_reg_b:
                if using_label:
                    vm.set_pc(displacement - 1)
                else:
                    pc = vm.get_pc()
                    vm.set_pc(pc + displacement)
        except (TypeError, ValueError) as err:
            raise ValueError(f'Erro de Execução: {err}')

        return True

    ##
    # Covert the instruction to a hexadecimal representation.
    #
    # @param vm is a VirtualMachine class Object
    # @return hexadecimal representation
    def get_hexa_representation(self, vm):
        if isinstance(self.value, str):
            try:
                if self.address is not None:
                    pc = self.address
                else:
                    pc = vm.get_pc()
                value = vm.get_label_value(self.value)
                value_fix = value - pc - 1
                value = value_fix
            except ValueError as err:
                raise ValueError(f'Não foi possível converter a '
                                 f'instrução para hexadecimal. {err}')
        else:
            value = self.value

        prefix = '0000000'
        utils = InstructionsUtils()

        rega = utils.convert_register_to_binary(self.reg_a)
        regb = utils.convert_register_to_binary(self.reg_b)
        try:
            value = utils.convert_to_binary_twos_complement(value, 16)
        except ValueError as err:
            raise ValueError(err)

        binary_representation = prefix + self.INSTRUCTION_CODE + rega + regb + value
        output = utils.convert_binary_to_hexadecimal(binary_representation)
        return output


##
# Class that implements the jalr instruction
#
class Jalr(Instruction):
    INSTRUCTION_NAME = 'jalr'
    INSTRUCTION_CODE = '101'

    def __init__(self, la, ops):
        super().__init__()
        self.label = la
        if len(ops) >= 2:
            self.reg_a = ops[0]
            self.reg_b = ops[1]
        else:
            raise ValueError('Não há argumentos suficientes para '
                             'a operação. (necessário: 2)')

    @property
    def reg_a(self):
        return self._reg_a

    @reg_a.setter
    def reg_a(self, value):
        try:
            value = InstructionsUtils.validate_register_operator(value)
        except ValueError as err:
            raise ValueError(f'Argumento 1: {err}')
        self._reg_a = value

    @property
    def reg_b(self):
        return self._reg_b

    @reg_b.setter
    def reg_b(self, value):
        try:
            value = InstructionsUtils.validate_register_operator(value)
        except ValueError as err:
            raise ValueError(f'Argumento 2: {err}')
        self._reg_b = value

    ##
    # Performs the operation of the jalr instruction
    #
    def execute(self, vm):
        pc = vm.get_pc()
        value_reg_a = vm.get_register_value(self.reg_a)

        try:
            result = int(pc + 1)
            vm.set_register_value(result, self.reg_b)
            # todo: em ingles
            # recebe o valor do registrador menos 1 pois
            #  ao final da execução o engine vai incrementar o pc
            vm.set_pc(value_reg_a - 1)
        except (TypeError, ValueError) as err:
            # TODO: msg
            raise ValueError(f'Erro de Execução: {err}')

        return True

    ##
    # Covert the instruction to a hexadecimal representation.
    #
    # @param vm is a VirtualMachine class Object
    # @return hexadecimal representation
    def get_hexa_representation(self, *args):
        utils = InstructionsUtils()

        prefix = '0' * 7
        suffix = '0' * 16
        rega = utils.convert_register_to_binary(self.reg_a)
        regb = utils.convert_register_to_binary(self.reg_b)

        bin_representation = prefix + self.INSTRUCTION_CODE + rega + regb + suffix
        output = utils.convert_binary_to_hexadecimal(bin_representation)

        return output

    ##
    # returns the representation of the instruction in pseudocode
    #
    def __repr__(self):
        return f'{self.INSTRUCTION_NAME} {self.reg_a} {self.reg_b}'


##
# Class that implements the halt instruction
#
class Halt(Instruction):
    INSTRUCTION_NAME = 'halt'
    INSTRUCTION_CODE = '01800000'

    def __init__(self, la):
        super().__init__()
        self.label = la

    ##
    # Performs the operation of the halt instruction
    #
    def execute(self, vm):
        return False

    ##
    # returns the representation of the instruction in pseudocode
    #
    def __repr__(self):
        return self.INSTRUCTION_NAME


##
# Class that implements the noop instruction
#
class Noop(Instruction):
    INSTRUCTION_NAME = 'noop'
    INSTRUCTION_CODE = '01C00000'

    def __init__(self, la):
        super().__init__()
        self.label = la

    ##
    # Performs no operatin as the noop instruction
    #
    def execute(self, vm):
        return True

    ##
    # returns the representation of the instruction in pseudocode
    #
    def __repr__(self):
        return self.INSTRUCTION_NAME


##
# Class that implemente the directive  ".fill"
#
class Fill:
    NAME = '.fill'

    def __init__(self, la, ops):
        self.label = la
        if len(ops) >= 1:
            self.value = ops[0]
        else:
            raise ValueError('Não há argumentos suficientes para a operação. (Necessário: 1)')
        self.address = None

    def set_address(self, address):
        self.address = address

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, str):
            negative = False
            if value[0] == '-':
                if value[1:].isnumeric():
                    value = value[1:]
                    negative = True
            if value.isnumeric():
                value = int(value)
                if negative:
                    value *= -1

                # TODO: (2021) Aqui tem que mudar pois o range vai mudar com a representação nova
                # Defining possible range
                min_val = -1 * (2 ** (VirtualMachine.WORD_SIZE - 2))
                max_val = (2 ** (VirtualMachine.WORD_SIZE - 2)) - 1

                if value < min_val or value > max_val:
                    raise ValueError(f'.fill deve receber um valor entre '
                                     f'{min_val} e {max_val}')

            elif not value.isalpha():
                raise ValueError('Argumento 1: Recebe somente Inteiros ou '
                                 'Labels com caracteres válidos.')
        elif not isinstance(value, int):
            raise ValueError('Argumeto 1: O argumento deve ser um número '
                             'inteiro ou um label com caracteres válidos.')

        self._value = value

    @staticmethod
    def execute(*args):
        return True

    ##
    # Covert the instruction to a hexadecimal representation.
    #
    # @param vm is a VirtualMachine class Object
    # @return hexadecimal representation
    def get_hexa_representation(self, vm):
        if isinstance(self.value, str):
            try:
                value = vm.get_label_value(self.value)
            except ValueError as err:
                raise ValueError(f'Não foi possível converter a instrução '
                                 f'para hexadecimal. {err}')
        else:
            value = self.value

        utils = InstructionsUtils()

        try:
            # TODO: (2021) PEDIDO PARA CONVERSÃO DE FILL
            bin_repr = utils.convert_to_binary_twos_complement(value, VirtualMachine.WORD_SIZE-1)
        except ValueError as err:
            raise ValueError(err)
        # TODO: (2021) TROCANDO O 1 PELO 0 RESOLVE PARCIALMENTE O PROBLEMA
        #  VAI APRESENTAR O NÚMERO COMO DESEJADO MAS A REPRESENTAÇÃO INTERNA
        #  E A INTERPRETAÇÃO DE HEXADECIMAIS ESTARA QUEBRADA
        bin_repr = '1' + bin_repr
        output = utils.convert_binary_to_hexadecimal(bin_repr)

        return output

    def get_value(self):
        return self._value

    ##
    # returns the representation of the number passed along with the directive
    #
    def __repr__(self):
        return f'{self.NAME} {self.value}'
