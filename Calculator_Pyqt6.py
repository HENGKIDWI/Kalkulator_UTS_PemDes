import os
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLineEdit, QTabWidget
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QAction, QIcon


class GridCalculatorTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFont(QFont('Arial', 26))
        self.display.setFixedHeight(70)
        layout.addWidget(self.display)

        grid = QGridLayout()
        buttons = [
            'AC', 'Del', '/', 
            '7', '8', 'x',
            '5', '6', '-',
            '3', '4', '+',
            '0', '1', '=',
        ]

        positions = [(i, j) for i in range(6) for j in range(3)]
        
        for position, button in zip(positions, buttons):
            btn = QPushButton(button)
            btn.setFont(QFont('Arial', 18))
            btn.setFixedSize(100, 80)
            btn.clicked.connect(self.onButtonClick)
            grid.addWidget(btn, *position)

        layout.addLayout(grid)
        self.setLayout(layout)

    def onButtonClick(self):
        button = self.sender().text()
        self.parent.processButton(button, self.display)

class KombinasiCalculatorTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        

        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFont(QFont('Arial', 26))
        self.display.setFixedHeight(70)
        main_layout.addWidget(self.display)

        buttons_layout = QHBoxLayout()
        
        for column in [
            ['AC', '7', '5', '3', '0'],
            ['Del', '8', '6', '4', '1'],
            ['/', 'x', '-', '+', '='],
        ]:
            column_layout = QVBoxLayout()
            for button in column:
                btn = QPushButton(button)
                btn.setFont(QFont('Arial', 18))
                btn.setFixedSize(100, 80)
                btn.clicked.connect(self.onButtonClick)
                column_layout.addWidget(btn)
            buttons_layout.addLayout(column_layout)

        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

    def onButtonClick(self):
        button = self.sender().text()
        self.parent.processButton(button, self.display)

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Calculator')
        self.setGeometry(600, 100, 400, 450)
        layout = QVBoxLayout()
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(GridCalculatorTab(self), "Grid")
        self.tab_widget.addTab(KombinasiCalculatorTab(self), "Kombinasi")

        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

    def processButton(self, button, display):
        current = display.text()

        if button == 'AC':
            display.setText('')
        elif button == 'Del':
            display.setText(current[:-1] if len(current) > 1 else '')
        elif button == '=':
            try:
                result = eval(current.replace('x', '*'))
                display.setText(str(result))
            except:
                display.setText('Error')
        else:
            if current == '' and button != '.':
                display.setText(button)
            else:
                display.setText(current + button)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec())
