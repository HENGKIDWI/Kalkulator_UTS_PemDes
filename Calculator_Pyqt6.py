import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLineEdit, QTabWidget
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Calculator')
        self.setGeometry(600, 100, 400, 450)
        layout = QVBoxLayout()
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.South)
        self.tab_widget.addTab(GridCalculatorTab(self), "Grid")
        self.tab_widget.addTab(KombinasiCalculatorTab(self), "Kombinasi")

        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

    def valid(self, exp):
        if "/0" in exp:
            return False
        if exp and (exp[-1] in ['+', '-', 'x', '/']):
            return False
        return True

    def processButton(self, button, display):
        current = display.text()
        if button == 'AC':
            display.setText('0')
        elif button == 'Del':
            display.setText(current[:-1] if len(current) > 1 else '0')
        elif button == '=':
            if self.valid(current):
                result = self.calculate(current)
                display.setText(str(result))
            else:
                display.setText('Error')
        else:
            if current == 'Error':
                display.setText(button if button not in ['+', '-', 'x', '/'] else '0' + button)
            elif current == '0':
                if button in ['+', '-', 'x', '/']:
                    display.setText(current + button)
                elif button == '0': 
                    return
                else:
                    display.setText(button)
            else:
                if button in ['+', '-', 'x', '/'] and current[-1] in ['+', '-', 'x', '/']:
                    return
                else:
                    display.setText(current + button)

    def calculate(self, expression):
        operators = ['+', '-', 'x', '/']
        operand_list = []
        operator_list = []

        num = ''
        for char in expression:
            if char in operators:
                if num:
                    operand_list.append(int(num))
                    num = ''
                operator_list.append(char)
            else:
                num += char

        if num:  
            operand_list.append(int(num))

        result = operand_list[0]

        for i in range(len(operator_list)):
            operator = operator_list[i]
            next_operand = operand_list[i + 1]

            if operator == '+':
                result += next_operand
            elif operator == '-':
                result -= next_operand
            elif operator == 'x':
                result *= next_operand
            elif operator == '/':
                if next_operand != 0:
                    result /= next_operand
                else:
                    return "Error"

        return int(result)


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
        self.display.setText('0')
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
        self.display.setText('0')
        self.display.setFont(QFont('Arial', 26))
        self.display.setFixedHeight(70)
        main_layout.addWidget(self.display)

        buttons_layout = QHBoxLayout()
        
        for column in [
            ['7', '6', '3', '1'],
            ['8', '5', '4', '0'],
            ['/', 'x', '-', '+'],
            ['AC', 'Del', '=']
        ]:
            column_layout = QVBoxLayout()
            for button in column:
                btn = QPushButton(button)
                btn.setFont(QFont('Arial', 18))
                btn.setFixedSize(100, 80)
                if button == "=":
                    btn.setFixedHeight(165)
                btn.clicked.connect(self.onButtonClick)
                column_layout.addWidget(btn)
            buttons_layout.addLayout(column_layout)

        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

    def onButtonClick(self):
        button = self.sender().text()
        self.parent.processButton(button, self.display)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec())
