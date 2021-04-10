#!/usr/bin/env python
# coding: UTF-8
#
## @package engine
#
#   Executing a list of instructions
#
#   @author Nathaniel Ramalho
#   @since 11/28/2020
#

from virtual_machine import VirtualMachine
from assembler import Assembler
from time import sleep
from instruction_set import Fill, Sw


class Engine:
    def __init__(self, context):
        self.execution_queue = []
        self.virtual_machine = None
        self.clock = 0.5
        self.status = StatusReady()
        self.context = context

    ##
    # Performs actions necessary to execute a program from
    #  text and executes the program
    #
    def run(self, text):
        if self.status.is_running:
            self.status = StatusReady()

        if not text:
            self.context.log_on_console('O código fonte está em branco.')
            self.context.log_on_console('Fim da execução.')
            self.context.change_back_pc_bg()
            self.context.console_space()
            self.context.enable_execution_button()
            return

        # Translation
        try:
            self.translate(text)
        except ValueError as err:
            self.context.log_on_console(err)
            self.context.log_on_console('Fim da Execução.')
            self.context.enable_execution_button()
            self.context.change_back_pc_bg()
            return

        # Execution
        self.create_virtual_machine()
        self.virtual_machine.reset_pc()

        self.status = StatusRunning()

        while self.status.is_running:
            pc = self.virtual_machine.get_pc()
            if not self.is_valid_pc(pc):
                self.context.log_on_console('Falha na execução.')
                self.context.log_on_console('    O endereço de memória acessado '
                                            'não contém uma instrução válida.')
                self.context.log_on_console('    (Dica: sempre termine seu '
                                            'código com halt)')
                self.virtual_machine.reset_pc()

                self.status = StatusReady()
                self.context.enable_execution_button()
                self.context.log_on_console('Fim da Execução.')
                self.context.change_back_pc_bg()
                return

            try:
                sleep(self.clock)

                instruction = self.execution_queue[pc]

                if isinstance(instruction, int):
                    raise ValueError(f'Erro de execução: "{instruction}" não é uma '
                                     f'instrução válida.\n(endereço de memória: {pc})')
                else:
                    inst_representation = self.execution_queue[pc].get_hexa_representation(self.virtual_machine)
                    self.virtual_machine.instruction_register = inst_representation
                    success = instruction.execute(self.virtual_machine)

                if success:
                    self.virtual_machine.increment_pc()
                    if isinstance(instruction, Sw):
                        self.update_execution_queue()
                        self.context.update_memory_table()
                        self.context.update_ui_pc()
                else:
                    self.status = StatusReady()
                    self.context.log_on_console('Fim da execução.')
                    self.context.change_back_pc_bg()
                    self.context.console_space()
                    self.context.enable_execution_button()
            except (ValueError, TypeError) as err:
                self.context.log_on_console(err)

                self.context.log_on_console('Fim da Execução.')
                self.context.console_space()
                self.context.change_back_pc_bg()

                self.virtual_machine.reset_pc()
                self.status = StatusReady()
                self.context.enable_execution_button()

    ##
    # Performs a series of actions to start the step execution.
    #
    def run_in_steps(self, text):
        if not text:
            self.context.log_on_console('O código fonte está em branco.')
            self.context.log_on_console('Fim da execução em etapas.')
            self.context.change_back_pc_bg()
            self.context.console_space()
            return

        if self.status.is_running:
            self.status = StatusReady()

        try:
            self.translate(text)
        except ValueError as err:
            self.context.log_on_console(err)
            self.context.log_on_console('Fim da Execução.')
            self.context.enable_execution_button()
            self.context.change_back_pc_bg()
            return

        self.create_virtual_machine()
        self.virtual_machine.reset_pc()
        self.virtual_machine.instruction_register = 0

        self.status = StatusWaiting()
        self.context.log_on_console('O sistema iniciou o processo de Execução em Etapas.')
        self.context.change_pc_bg()
        self.context.action_avancar.setDisabled(False)

    ##
    # Execute the next instruction of the execution queue when
    # in step execution mode
    #
    def step_foward(self):
        pc = self.virtual_machine.get_pc()
        if not self.is_valid_pc(pc):
            self.context.log_on_console('Falha na execução.')
            self.context.log_on_console('    O endereço de memória acessado não contém uma instrução válida.')
            self.context.log_on_console('    (Dica: Sempre termine seu código com "halt")')
            self.virtual_machine.reset_pc()
            self.status = StatusWaiting()
            self.context.action_avancar.setDisabled(True)
            self.context.log_on_console('Fim da execução.')
            self.context.change_back_pc_bg()
            self.context.console_space()
            return

        if not self.status.is_step_execution:
            self.context.log_on_console(
                'O sistema não está em modo de Execução em Etapas.')

            self.context.log_on_console('Fim da Execução.')
            self.context.enable_execution_button()
            self.context.change_back_pc_bg()

            return

        try:
            instruction = self.execution_queue[pc]

            if isinstance(instruction, int):
                raise ValueError(f'Erro de execução: "{instruction}" não é uma '
                                 f'instrução válida.\n(endereço de memória: {pc})')
            else:
                inst_representation = self.execution_queue[pc].get_hexa_representation(self.virtual_machine)
                self.virtual_machine.instruction_register = inst_representation
                success = instruction.execute(self.virtual_machine)

            if success:
                self.virtual_machine.increment_pc()
                if isinstance(instruction, Sw):
                    self.update_execution_queue()
                    self.context.update_memory_table()
                    self.context.update_ui_pc()
            else:
                self.context.action_avancar.setDisabled(True)
                self.context.log_on_console('Fim da Execução em Etapas.')
                self.context.change_back_pc_bg()
                self.context.console_space()
                self.status = StatusReady()
                self.context.enable_execution_button()
        except (ValueError, TypeError) as err:
            self.context.log_on_console(err)
            self.context.log_on_console('Fim da Execução.')
            self.context.change_back_pc_bg()
            self.virtual_machine.reset_pc()
            self.context.action_avancar.setDisabled(True)
            self.status = StatusWaiting()

        pc = self.virtual_machine.get_pc()

        if not self.is_valid_pc(pc):
            self.status = StatusReady()

    ##
    # Performs a series of actions to translate a text
    # into source code. It also invokes other methods to
    # load the translated data into the virtual machine.
    # reraises exceptions that may occur in the methods
    # called during its execution
    #
    # @param text texto de entrada do usuário
    def translate(self, text):
        if not text:
            self.context.log_on_console('Sem itens para traduzir.')
            self.context.console_space()
            return

        self.create_virtual_machine()
        try:
            self.populate_execution_queue(text)
            self.update_vm_labels()
            self.update_vm_main_memory()
        except ValueError as err:
            raise ValueError(err)
        self.context.log_on_console('Sucesso na tradução!')

    ##
    # Populates the execution queue with the instruction
    # list translated by the assembler.
    #
    def populate_execution_queue(self, text):
        assembler = Assembler()
        try:
            self.execution_queue = assembler.assemble(text)
        except ValueError as err:
            raise ValueError(err)

    ##
    #   Updates execution_queue based on virual_machine.main_memory
    #
    #   @see VirtualMachine
    def update_execution_queue(self):
        memory = self.virtual_machine.main_memory

        # TODO: Maybe this test is unnecessary
        if self.virtual_machine.BLOCKED_ADDRESS_KEY in memory.keys():
            memory.pop(self.virtual_machine.BLOCKED_ADDRESS_KEY)

        for i, k in enumerate(memory.keys()):
            if i >= len(self.execution_queue):
                self.execution_queue.append(memory[k])
            else:
                inst = self.execution_queue[i]
                if isinstance(inst, int):
                    value = inst
                else:
                    value = inst.get_hexa_representation(self.virtual_machine)
                    value = int(value, 16)
                if value != self.virtual_machine.main_memory[k]:
                    self.execution_queue[i] = memory[k]

        self.virtual_machine.block_memory(len(self.execution_queue) - 1)

    ##
    # Updates the data in the main memory of the virtual machine
    #
    def update_vm_main_memory(self):
        self.virtual_machine.clear_main_memory()

        try:
            for i, inst in enumerate(self.execution_queue):
                if isinstance(inst, Fill):
                    representation = inst.get_value()
                    if representation in self.virtual_machine.labels.keys():
                        representation = self.virtual_machine.get_label_value(representation)
                else:
                    hex_representation = inst.get_hexa_representation(self.virtual_machine)
                    representation = int(hex_representation, 16)
                self.virtual_machine.set_main_memory_value(representation, i)
            # TODO: (2021-sw) BLOQUEIO DA MEMÓRIA - TALVEZ REMOVER O TESTE EM UPDATE_EXECUTION_QUEUE
            self.virtual_machine.block_memory(len(self.execution_queue) - 1)
        except ValueError as err:
            raise ValueError(f'Atualização da memória principal: {err}')
        self.context.update_memory_table()

    ##
    # Updates the list of virtual machine labels
    #
    def update_vm_labels(self):
        self.create_virtual_machine()
        try:
            self.virtual_machine.clear_labels()
            for i, inst in enumerate(self.execution_queue):
                if inst.label is not None:
                    self.virtual_machine.add_label(inst.label, i)
                inst.set_address(i)
        except ValueError as err:
            raise ValueError(err)

    ##
    # Checks your past value can represent a valid register
    #
    # @param a value to check if can represent a register
    #
    def is_valid_pc(self, pc):
        if pc in list(range(len(self.execution_queue))):
            return True

        return False

    ##
    # Creates a virtual machine if not exists
    #
    def create_virtual_machine(self):
        if self.virtual_machine is None:
            self.virtual_machine = VirtualMachine(self.context)

    def set_clock(self, value):
        self.clock = value

    ##
    # Returns data tha represents a Engine class instance
    #
    # @retun A string that represents the object
    #
    def __repr__(self):
        msg = '\n-= ENGINE =-\n'
        msg += f'· Status: {self.status}\n'
        msg += f'· Clock: {self.clock}\n'
        msg += '· Execution Queue: \n'
        msg += '\t' + str(self.execution_queue) + '\n'
        msg += '· Virtual Machine:\n'
        msg += str(self.virtual_machine) + '\n'
        msg += '-= FIM =-:\n'

        return msg


# States
##
# EngineStatus is an abstract class
# to model all sistem status classes
#
class EngineStatus:
    NAME = 'Superclass'

    def __init__(self):
        self.is_running = False
        self.is_step_execution = False

    def __repr__(self):
        return self.NAME


##
# Classes whose instance represents the running engine
#
class StatusRunning(EngineStatus):
    NAME = 'Running'

    def __init__(self):
        super().__init__()
        self.is_running = True


##
# Class whose instance represents the waiting state.
# This state occurs when the engine is running a step execution.
#
class StatusWaiting(EngineStatus):
    NAME = 'Waiting'

    def __init__(self):
        super().__init__()
        self.is_running = True
        self.is_step_execution = True


##
# Class whose instance represents the engine in
# its normal state ready to receive commands.
#
class StatusReady(EngineStatus):
    NAME = 'Ready'

    def __init__(self):
        super().__init__()
