#!/usr/bin/env python
# coding: UTF-8
#
## @package ui_code_editor
#
#   Models code editor
#
#   Based on a tutorial from Qt documentation available in:
#   https://doc.qt.io/qt-5/qtwidgets-widgets-codeeditor-example.html
#
#   Adapted to python by Nathaniel Ramalho
#   @since 11/28/2020
#
from PySide2.QtWidgets import QWidget, QPlainTextEdit, QTextEdit
from PySide2.QtCore import Qt, QRect, QSize
from PySide2.QtGui import QColor, QPainter, QTextFormat


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)

        self.code_editor = editor

    ##
    # Overrides the superclass sizeHint method
    #
    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    ##
    # Overrides the superclass paintEvent method
    #
    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_number_area = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width(0)

        # text editor color
        self.setStyleSheet('color: #DDDDDD; '
                           'font-size: 12px;'
                           'font-weight: bold')

    ##
    # Dynamically calculates the size of the area with line numbers
    # according to the number and decimal places
    def line_number_area_width(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits

        # resizing line area
        space += 5

        return space

    ##
    # Updates the width of line_number_area
    #
    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    ##
    # Updates the line number area
    #
    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    ##
    # Overrides the superclass method that treats of resize events
    #
    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(
            QRect(
                cr.left(),
                cr.top(),
                self.line_number_area_width(),
                cr.height()))

    ##
    # Hightlights the entire line that cursor is
    #
    def highlight_current_line(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            # Line Highlight color
            # bkp of original color
            # lineColor = QColor(Qt.yellow).lighter(160)
            lineColor = QColor(100, 100, 100)

            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    ##
    # It deals with the drawing of the area of the numbers on the left
    #
    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)

        # side area background-color
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        height = self.fontMetrics().height()
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)

                # cor dos números da área lateral
                # bkp original
                painter.setPen(Qt.black)

                painter.drawText(
                    0,
                    top,
                    self.line_number_area.width(),
                    height,
                    Qt.AlignLeft,
                    number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1
