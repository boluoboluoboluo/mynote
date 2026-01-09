import random
import sys
from PySide6 import QtWidgets,QtCore,QtGui

class MyWidget(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()

		self.hello = ["唐僧","孙悟空","猪八戒","沙和尚"]
		self.button = QtWidgets.QPushButton("click me")
		self.text = QtWidgets.QLabel("hello world",alignment=QtCore.Qt.AlignCenter)

		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.addWidget(self.text)
		self.layout.addWidget(self.button)
		self.button.clicked.connect(self.magic)

	@QtCore.Slot()
	def magic(self):
		self.text.setText(random.choice(self.hello))

if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	widget = MyWidget()
	widget.resize(800,600)
	widget.show()

	sys.exit(app.exec())
