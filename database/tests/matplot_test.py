import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt

# Your plotting code here
plt.plot([1, 2, 3, 4])
plt.ylabel('Some numbers')
plt.savefig('test_plot.png')
#import sys
#from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
#
#class MainWindow(QMainWindow):
#    def __init__(self):
#        super().__init__()
#        label = QLabel("Testing PyQt5", self)
#        self.setCentralWidget(label)
#        self.resize(300, 200)
#
#def main():
#    app = QApplication(sys.argv)
#    window = MainWindow()
#    window.show()
#    sys.exit(app.exec_())
#
#if __name__ == "__main__":
#    main()