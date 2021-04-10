#!/usr/bin/env python
# coding: UTF-8
#
## @package assembler
#
#   Translating text to instructions.
#
#   @author Nathaniel Ramalho
#   @since 11/28/2020
#

from instruction_set import *


##
# The Assembler class allows the convertion of
# a text to a list of Intruction type object
#
# @see Instruction
class Assembler:
    ##
    # Process user input text and return a vector with
    # lists of terms one for each line
    #
    # @param string
    # @retur [[srt]]
    @staticmethod
    def process_text(text: str):
        text = text.strip().split('\n')
        t_processado = []
        for line in text:
            t_processado.append(line.strip().split())
        return t_processado

    ##
    # Translates a line of processed text into an instruction
    #
    # @return an Instruction class object
    @staticmethod
    def translate_line(line: [str]):
        label = None
        ops = []
        utils = InstructionsUtils()

        if not line:
            raise ValueError('A linha está vazia')

        if ':' in line[0]:
            try:
                if line[0][0].isalpha():
                    label = line[0].strip().strip(':').lower()
                    name = line[1].strip().lower()
                    ini = 2
                else:
                    raise ValueError('O label só pode começar com letras.')
            except IndexError:
                raise ValueError('Sintaxe incorreta.')
            except ValueError as err:
                raise ValueError(err)
        else:
            name = line[0].strip().lower()
            ini = 1

        for term in line[ini:]:
            ops.append(term)

        if not utils.is_valid_instruction_name(name):
            raise ValueError(f'"{name}" não é uma instrução válida.')

        try:
            if name == 'add':
                instruction = Add(label, ops)
            elif name == 'addi':
                instruction = Addi(label, ops)
            elif name == 'lw':
                instruction = Lw(label, ops)
            elif name == 'sw':
                instruction = Sw(label, ops)
            elif name == 'beq':
                instruction = Beq(label, ops)
            elif name == 'jalr':
                instruction = Jalr(label, ops)
            elif name == 'halt':
                instruction = Halt(label)
            elif name == 'noop':
                instruction = Noop(label)
            elif name == '.fill':
                instruction = Fill(label, ops)
            else:
                raise ValueError(f'"{name}" não é uma instrução válida.')
        except (ValueError, TypeError) as err:
            raise ValueError(err)

        return instruction

    ##
    # Translates text into a list of instructions
    #
    # @return a list of Instruction class instances
    #
    # @see Instruction
    def assemble(self, text: str):
        translated = []

        if text.strip() == '':
            return translated

        processed_text = self.process_text(text)

        is_binary_code = self.is_binary_code(processed_text)

        for i, line in enumerate(processed_text):
            try:
                if is_binary_code:
                    instruction = self.decode_line(line[0])
                else:
                    instruction = self.translate_line(line)
                translated.append(instruction)
            except ValueError as err:
                raise ValueError(f'Erro de tradução na linha {i + 1}: {err}')

        return translated

    ##
    # Checks whether a rendered text is a binary code
    #
    # @return True if is binary code and False otherwise
    @staticmethod
    def is_binary_code(processed_text):
        for line in processed_text:
            if len(line) != 1:
                return False

            if len(line[0]) != 8:
                return False

            try:
                int(line[0], 16)
            except ValueError:
                return False

        return True

    ##
    # Converts an binary code entry to a list of instructions
    #
    # @return a list of Instruction class instances
    @staticmethod
    def decode_line(text):
        bin_converted = ''
        for ch in text:
            ch = bin(int(ch, 16))[2:]
            ch = '0' * (4 - len(ch)) + ch
            bin_converted += ch

        label = None
        name = bin_converted[0:10]
        op0 = bin_converted[10:13]
        op1 = bin_converted[13:16]
        op2 = bin_converted[17:]

        utils = InstructionsUtils()

        try:
            name = int(name, 2)
            if 0 <= name <= 7:
                name = utils.get_name_by_code(name)
                op0 = int(op0, 2)
                op1 = int(op1, 2)
                op2 = utils.twos_complement_binary_to_int(op2)
            else:
                name = '.fill'
                op0 = utils.twos_complement_binary_to_int(bin_converted)
        except ValueError as err:
            raise ValueError(f'Decodificação: {err}')

        ops = [op0, op1, op2]

        try:
            if name == 'add':
                instruction = Add(label, ops)
            elif name == 'addi':
                instruction = Addi(label, ops)
            elif name == 'lw':
                instruction = Lw(label, ops)
            elif name == 'sw':
                instruction = Sw(label, ops)
            elif name == 'beq':
                instruction = Beq(label, ops)
            elif name == 'jalr':
                instruction = Jalr(label, ops)
            elif name == 'halt':
                instruction = Halt(label)
            elif name == 'noop':
                instruction = Noop(label)
            elif name == '.fill':
                instruction = Fill(label, ops)
            else:
                raise ValueError(f'"{name}" não é uma instrução válida.')
        except (ValueError, TypeError) as err:
            raise ValueError(err)

        return instruction
