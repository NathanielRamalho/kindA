#!/usr/bin/env python
# coding: UTF-8
#
## @package ui_help
#
#   Models a help dialog graphid interface.
#
#   @author Nathaniel Ramalho
#   @since 11/28/2020
#
#
from PySide2.QtWidgets import QVBoxLayout, QTextEdit, QWidget, QScrollArea
from PySide2.QtGui import QIcon


##
# Class thats models and configures a help dialog
#
class Help(QWidget):
    def __init__(self):
        super().__init__()

        self.left = 400
        self.top = 200
        self.width = 800
        self.height = 400
        self.title = 'Ajuda'
        self.icon_path = 'assets/icon_logo.png'

        self.init_window()

    ##
    # Initializes and configures help window
    #
    def init_window(self):
        # window configuration
        self.setGeometry(self.left,
                         self.top,
                         self.width,
                         self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(self.icon_path))
        self.setStyleSheet(
            'QWidget{'
            'background-color: #2d2d2d;'
            'color: white;}'
            # 'QTextEdit{'
            # 'background-color: #2D2D2D;}'
            'QLabel{background-color: goldenrod;}')

        self.setMinimumWidth(400)
        self.setMinimumHeight(200)
        # self.setMaximumHeight(300)

        # main layout
        layout_main = QVBoxLayout()
        layout_main.setContentsMargins(0, 0, 0, 0)
        layout_main.setSpacing(0)

        # Scroll Area
        scroll_area_main = QScrollArea()
        scroll_area_main.setStyleSheet(
            'QTextEdit{'
            'background-color: #2d2d2d; '
            'color: #AAAAAA;'
            'border-style: none;}')

        # layout frame_main
        layout_scroll_area = QVBoxLayout()
        layout_scroll_area.setContentsMargins(10, 0, 0, 0)

        # 'body{color:black;}' \
        # Content
        t = '' \
            '<html lang="pt-br">' \
            '<head>' \
            '    <meta charset="UTF-8">' \
            '   <meta name="viewport"' \
            '          content="width=device-width, user-scalable=no, ' \
            'initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">' \
            '    <meta http-equiv="X-UA-Compatible" content="ie=edge">' \
            '    <title>Document</title>' \
            '    <style>' \
            '        body{' \
            '            background-color: #2D2D2D;' \
            '            color:#9BAEC1;' \
            '            font-size: 13px;' \
            '        }' \
            '        p{margin: 0;}' \
            '        ul{margin-top: 0;}' \
            '        table{' \
            '            border-collapse: collapse;' \
            '            background-color: #323232;' \
            '            color: #9BAEC1;' \
            '            margin-left: 15px;' \
            '            margin-top: 10px;' \
            '        }' \
            '        table, th, td{' \
            '            border: 1px solid #828790;' \
            '            text-align: center;' \
            '            padding: 5px;' \
            '        }' \
            '        th{' \
            '            background-color: #3C3F41;' \
            '        }' \
            '        h1, h2, h3, h4{' \
            '            margin: 20px 0 5px 0;' \
            '            color: #AAAAAA;' \
            '        }' \
            '        .subitem{list-style-type: none;}' \
            '        .icon{' \
            '            width: 20px;' \
            '            height: 20px;' \
            '            margin-top: auto;' \
            '            margin-bottom: auto;' \
            '        }' \
            '    </style>' \
            '</head>' \
            '<body>' \
            '<h1>Como usar o kindA</h1>' \
            '<h2>Executando o código:</h2>' \
            '<p>Há três formas de executar o programa:</p>' \
            '<ul>' \
            '    <li>Acessando o menu "Executar" > "Executar".</li>' \
            '    <li>Acionado o botão <img width="20" height="20" class="icon" src="assets/icon_run.png" ' \
            'alt="Executar"> na barra de ferramentas.</li>' \
            '    <li>Pelo atalho de Teclado Shift + F10.</li>' \
            '</ul>' \
            '' \
            '<h2>Execução em Etapas:</h2>' \
            '<p>Pode ser iniciada de 3 formas:</p>' \
            '<ul>' \
            '    <li>Acessando o menu "Executar" >  "Executar em etapas".</li>' \
            '   <li>Acionado o botão <img width="20" height="20" class="icon" src="assets/icon_step_run.png"' \
            '                              alt="Executar em etapas"> na barra de ferramentas.</li>' \
            '    <li>Pelo atalho de Teclado Shift + F9.</li>' \
            '</ul>' \
            '<p>Quando acionado, é possível avançar na execução do' \
            '    código apertando o botão <img width="20" height="20" class="icon" ' \
            'src="assets/icon_avacar.png" alt="Avançar">.</p>' \
            '<p>Também é possível avançar através do menu "Executar" > "Avançar" ou pelo atalho de teclado F7.</p>' \
            '' \
            '<h2>Traduzindo o Código:</h2>' \
            '<p>O código pode ser traduzido de três formas:</p>' \
            '<ul>' \
            '    <li>Acessando o menu "Executar" >  "Traduzir".</li>' \
            '   <li>Acionado o botão <img width="20" height="20" class="icon" src="assets/icon_translate.png"' \
            '                              alt="Traduzir"> na barra de ferramentas.</li>' \
            '    <li>Pelo atalho de Teclado Ctrl + T.</li>' \
            '</ul>' \
            '' \
            '<h1>Características do Simulador</h1>' \
            '<p>' \
            '    O kindA é um simulador de execução de programas em linguagem Assembly, que funciona' \
            '    com um conjunto de instruções de uma máquina hipotética com as seguintes características:</p><br>' \
            '<ul>' \
            '    <li>Processador com palavra de 32-bits,</li>' \
            '    <li>Instruções de 32 bits,</li>' \
            '    <li>Representação de números inteiros em palavras de 32 bits e</li>' \
            '    <li>Endereço de 32 bits (Endereça até 4.294.967.296 palavras de memória)</li>' \
            '</ul>' \
            '<h2>Registradores</h2>' \
            '<p>' \
            '    O sistema possui 8 registradores com endereços de 0 até 7.' \
            '    O registrador R0 armazena o número zero e não pode ser alterado.' \
            '</p>' \
            '<br>' \
            '<h2>Conjunto de Instruções</h2>' \
            'O conjunto de instruções do kindA é composta por 8 instruções.' \
            'São elas: “add”, “addi”, “lw”, “sw”, “beq”, “jalr”, ' \
            '“noop” e “halt”. <br>A seguir veremos alguma informações sobre o funcionamento,' \
            'sintaxe e representação de cada instrução deste conjunto.' \
            '<br>' \
            '<h3>Instrução “add”</h3>' \
            '<ul>' \
            '    <li>Código da operação: "000"</li>' \
            '    <li>Funcionamento:</li>' \
            '    <li class="subitem">' \
            '        <ul>' \
            '            <li>Soma os conteúdos de regA e regB e atribui o resultado a regDest.</li>' \
            '        </ul>' \
            '    </li>' \
            '    <li>Sintaxe:</li>' \
            '    <li class="subitem">' \
            '        <ul>' \
            '            <li>add regA regB destReg</li>' \
            '        </ul>' \
            '    </li>' \
            '</ul>' \
            '' \
            '<h4>Representação:</h4>' \
            '<table align="left">' \
            '    <tr>' \
            '        <th>Bits:</th>' \
            '        <th>31-25</th>' \
            '        <th>24-22</th>' \
            '        <th>21-19</th>' \
            '        <th>18-16</th>' \
            '        <th>15-3</th>' \
            '        <th>2-0</th>' \
            '    </tr>' \
            '    <tr>' \
            '        <td></td>' \
            '        <td>Não utilizado</td>' \
            '        <td>opCode</td>' \
            '        <td>regA</td>' \
            '        <td>regB</td>' \
            '        <td>Não utilizado</td>' \
            '        <td>destReg</td>' \
            '    </tr>' \
            '</table>' \
            '<br>' \
            '' \
            '<h3>Instrução “addi”</h3>' \
            '<ul>' \
            '    <li>Código da operação: "001"</li>' \
            '    <li>Funcionamento</li>' \
            '    <li class="subitem">' \
            '        <ul>' \
            '            <li>Soma o conteúdo de regA com immediate e atribui o resultado a regB.</li>' \
            '        </ul>' \
            '    </li>' \
            '    <li>Sintaxe:</li>' \
            '    <li class="subitem">' \
            '        <ul>' \
            '            <li>addi regA regB immediate</li>' \
            '        </ul>' \
            '    </li>' \
            '</ul>' \
            '<h4>Representação:</h4>' \
            '<table align="left">' \
            '    <tr>' \
            '        <th>Bits:</th>' \
            '        <th>31-25</th>' \
            '        <th>24-22</th>' \
            '        <th>21-19</th>' \
            '        <th>18-16</th>' \
            '        <th>15-0</th>' \
            '    </tr>' \
            '    <tr>' \
            '        <td></td>' \
            '        <td>0000 000</td>' \
            '        <td>opCode</td>' \
            '        <td>regA</td>' \
            '        <td>regB</td>' \
            '        <td>Não utilizado</td>' \
            '    </tr>' \
            '</table>' \
            '<p>*"immediate” é convertido para o binário em complemento a 2.</p>' \
            '' \
            '' \
            '<br>' \
            '<h3>Instrução “lw”</h3>' \
            '<ul>' \
            '    <li>Código da operação: "010"</li>' \
            '    <li>Funcionamento</li>' \
            '    <li class="subitem">' \
            '        <ul>' \
            '            <li>Carrega conteúdo da memória com o endereço igual a' \
            '                regA + off no registrador regB</li>' \
            '        </ul>' \
            '    </li>' \
            '    <li>Sintaxe:</li>' \
            '    <li class="subitem">' \
            '        <ul>' \
            '            <li>lw regA regB off</li>' \
            '        </ul>' \
            '    </li>' \
            '</ul>' \
            '' \
            '' \
            '<table align="left">' \
            '    <tr>' \
            '        <th>Bits:</th>' \
            '        <th>31-25</th>' \
            '        <th>24-22</th>' \
            '        <th>21-19</th>' \
            '        <th>18-16</th>' \
            '        <th>15-0</th>' \
            '    </tr>' \
            '    <tr>' \
            '        <td></td>' \
            '        <td>Não utilizado</td>' \
            '        <td>opCode</td>' \
            '        <td>regA</td>' \
            '        <td>regB</td>' \
            '        <td>*off</td>' \
            '    </tr>' \
            '</table>' \
            '<p>*"off” é convertido para o binário em complemento a 2.</p>' \
            '' \
            '<br>' \
            '<h3>Instrução “sw”</h3>' \
            '<ul>' \
            '    <li>Código da operação: "011"</li>' \
            '    <li>Funcionamento</li>' \
            '    <li class="subitem">' \
            '        <ul>' \
            '            <li>Salva o conteúdo de regB no endereço de memória igual a' \
            '                regA + off no registrador regB</li>' \
            '        </ul>' \
            '    </li>' \
            '    <li>Sintaxe:</li>' \
            '    <li class="subitem">' \
            '        <ul>' \
            '            <li>sw regA regB off</li>' \
            '        </ul>' \
            '    </li>' \
            '</ul>' \
            '<table align="left">' \
            '    <tr>' \
            '        <th>Bits:</th>' \
            '        <th>31-25</th>' \
            '        <th>24-22</th>' \
            '        <th>21-19</th>' \
            '        <th>18-16</th>' \
            '        <th>15-0</th>' \
            '    </tr>' \
            '    <tr>' \
            '        <td></td>' \
            '        <td>Não utilizado</td>' \
            '        <td>opCode</td>' \
            '        <td>regA</td>' \
            '        <td>regB</td>' \
            '        <td>off</td>' \
            '    </tr>' \
            '</table>' \
            '<p>*"off” é convertido para o binário em complemento a 2.</p>' \
            '<br>' \
            '<h3>Instrução “beq”</h3>' \
            '<ul>' \
            '    <li>Código da operação: "100"</li>' \
            '    <li>Funcionamento</li>' \
            '    <li class="subitem">' \
            '        <ul>' \
            '            <li>Compara os valores de regA e regB. Se forem iguais' \
            '                altera o PC para o resultado da soma: off + pc + 1.' \
            '                Se forem diferentes o programa segue o seu fluxo normal</li>' \
            '        </ul>' \
            '    </li>' \
            '    <li>Sintaxe:</li>' \
            '    <li class="subitem">' \
            '        <ul>' \
            '            <li>Beq regA regB off</li>' \
            '        </ul>' \
            '    </li>' \
            '</ul>' \
            '' \
            '<table align="left">' \
            '    <tr>' \
            '        <th>Bits:</th>' \
            '        <th>31-25</th>' \
            '        <th>24-22</th>' \
            '        <th>21-19</th>' \
            '        <th>18-16</th>' \
            '        <th>15-0</th>' \
            '    </tr>' \
            '    <tr>' \
            '        <td></td>' \
            '        <td>Não utilizado</td>' \
            '        <td>opCode</td>' \
            '        <td>regA</td>' \
            '        <td>regB</td>' \
            '        <td>off</td>' \
            '    </tr>' \
            '</table>' \
            '<p>*"off” é convertido para o binário em complemento a 2.</p>' \
            '' \
            '<br>' \
            '<h3>Instrução “Jalr”</h3>' \
            '<ul>' \
            '    <li>Código da operação: "101"</li>' \
            '    <li>Funcionamento</li>' \
            '    <li class="subitem">' \
            '        <ul>' \
            '            <li>Incrementa o valor do “PC” e salva o resultado ' \
            'no registrador “regB” e copia o conteúdo do “regA” para o "PC”.</li>' \
            '        </ul>' \
            '    </li>' \
            '    <li>Sintaxe:</li>' \
            '    <li class="subitem">' \
            '        <ul>' \
            '            <li>jarl regA regB</li>' \
            '        </ul>' \
            '    </li>' \
            '</ul>' \
            '<table align="left">' \
            '    <tr>' \
            '        <th>Bits:</th>' \
            '        <th>31-25</th>' \
            '        <th>24-22</th>' \
            '        <th>21-19</th>' \
            '        <th>18-16</th>' \
            '        <th>15-0</th>' \
            '    </tr>' \
            '    <tr>' \
            '        <td></td>' \
            '        <td>Não utilizado</td>' \
            '        <td>opCode</td>' \
            '        <td>regA</td>' \
            '        <td>regB</td>' \
            '        <td>Não utilizado</td>' \
            '    </tr>' \
            '</table>' \
            '' \
            '<br>' \
            '<h3>Instrução “halt”</h3>' \
            '<ul>' \
            '    <li>Código da operação: "110"</li>' \
            '    <li>Funcionamento</li>' \
            '    <li class="subitem">' \
            '        <ul>' \
            '            <li>Encerra a execução do programa.</li>' \
            '        </ul>' \
            '    </li>' \
            '    <li>Sintaxe:</li>' \
            '    <li class="subitem">' \
            '        <ul>' \
            '            <li>halt</li>' \
            '        </ul>' \
            '    </li>' \
            '</ul>' \
            '' \
            '<table align="left">' \
            '    <tr>' \
            '        <th>Bits:</th>' \
            '        <th>31-25</th>' \
            '        <th>24-22</th>' \
            '        <th>21-0</th>' \
            '    </tr>' \
            '    <tr>' \
            '        <td></td>' \
            '        <td>Não utilizado</td>' \
            '        <td>opCode</td>' \
            '        <td>Não utilizado</td>' \
            '    </tr>' \
            '</table>' \
            '' \
            '<br>' \
            '<h3>Instrução “noop”</h3>' \
            '' \
            '<p>' \
            '    A instrução “noop” (no operation) não realiza nenhuma' \
            '    ação e nem recebe operadores.' \
            '</p>' \
            '' \
            '<h4>Sintaxe:</h4>' \
            '<p>noop</p>' \
            '<ul>' \
            '    <li>Código da operação: "111"</li>' \
            '    <li>Funcionamento</li>' \
            '    <li class="subitem">' \
            '        <ul>' \
            '            <li>Não realiza nenhuma operação.</li>' \
            '        </ul>' \
            '    </li>' \
            '    <li>Sintaxe:</li>' \
            '    <li class="subitem">' \
            '        <ul>' \
            '            <li>noop</li>' \
            '        </ul>' \
            '    </li>' \
            '</ul>' \
            '<table align="left">' \
            '    <tr>' \
            '        <th>Bits:</th>' \
            '        <th>31-25</th>' \
            '        <th>24-22</th>' \
            '        <th>21-0</th>' \
            '    </tr>' \
            '    <tr>' \
            '        <td></td>' \
            '        <td>Não utilizado</td>' \
            '        <td>opCode</td>' \
            '        <td>Não utilizado</td>' \
            '    </tr>' \
            '</table>' \
            '' \
            '<br>' \
            '<h2>Diretivas</h2>' \
            '<p>' \
            '    As diretivas permitem que o programador indique como o montador deve' \
            '    operar. O kindA tem apenas uma diretiva: “.fill”.' \
            '</p>' \
            '<ul>' \
            '    <li>Funcionamento</li>' \
            '    <li class="subitem">' \
            '        <ul>' \
            '            <li>Informa ao sistema que deve salvar um valor em memória.</li>' \
            '        </ul>' \
            '    </li>' \
            '    <li>Sintaxe:</li>' \
            '    <li class="subitem">' \
            '        <ul>' \
            '            <li>.fill valor</li>' \
            '        </ul>' \
            '    </li>' \
            '</ul>' \
            '<table align="left">' \
            '    <tr>' \
            '        <th>Bits:</th>' \
            '        <th>31</th>' \
            '        <th>30-0</th>' \
            '    </tr>' \
            '    <tr>' \
            '        <td></td>' \
            '        <td>Recebe o valor “1”</td>' \
            '        <td>valor</td>' \
            '    </tr>' \
            '</table>' \
            '' \
            '<br>' \
            '<h2>Labels</h2>' \
            '<p>' \
            '    Os labels são uma forma de demarcar os endereços de memória,' \
            '    onde estão gravadas as instruções para que possam ser referenciados' \
            '    futuramente.' \
            '</p>' \
            '<h4>Sintaxe:</h4>' \
            '<p>meuLabel: instrução operadores</p>' \
            '' \
            '<p>' \
            '    Os labels devem sempre serem definidos no início da linha de' \
            '    código e seu nome não aceita caracteres especiais, exceto os' \
            '    dois pontos ao final do nome. Além disso a nomenclatura do labels' \
            '    não aceita que comecem com números. Em outras palavras, a nomenclatura' \
            '    dos labels só pode ser constituída de letras e números, desde que não' \
            '    comece por números.' \
            '</p>' \
            '<p>' \
            '    Somente as instruções “lw”, “sw” e “beq” aceitam o uso de labels' \
            '    em seus respectivos operandos “off”.' \
            '</p><br><br>' \
            '</body>' \
            '</html>'

        txt1 = QTextEdit()
        txt1.setHtml(t)
        txt1.setReadOnly(True)

        layout_scroll_area.addWidget(txt1)

        scroll_area_main.setLayout(layout_scroll_area)
        layout_main.addWidget(scroll_area_main)
        self.setLayout(layout_main)
