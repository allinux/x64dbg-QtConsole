import sys
import os
import PyQt5
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.inprocess import QtInProcessKernelManager
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QEvent, QCoreApplication
from IPython.lib import guisupport

from IPython.lib.kernel import connect_qtconsole
from ipykernel.kernelapp import IPKernelApp

plugin_path = ""
if sys.platform == "win32":
	if hasattr(sys, "frozen"):
		plugin_path = os.path.join(os.path.dirname(os.path.abspath(sys.executable)), "PyQt5", "plugins")
		QCoreApplication.addLibraryPath(plugin_path)
	else:
		import site
		for dir in site.getsitepackages():
			QCoreApplication.addLibraryPath(os.path.join(dir, "PyQt5", "plugins"))

elif sys.platform == "darwin":
	plugin_path = os.path.join(QCoreApplication.getInstallPrefix(), "Resources", "plugins")

if plugin_path:
	QCoreApplication.addLibraryPath(plugin_path)


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
	PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
	PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

	
def mpl_kernel(gui):
    """Launch and return an IPython kernel with matplotlib support for the desired gui
    """
    kernel = IPKernelApp.instance()
    kernel.initialize(['python', '--matplotlib=%s' % gui,
                       #'--log-level=10'
                       ])
    return kernel
	
class JupyterWidget(RichJupyterWidget):
	def __init__(self):
		super(RichJupyterWidget, self).__init__()
		self.kernel_manager = QtInProcessKernelManager()
		self.kernel_manager.start_kernel()
		self.kernel = self.kernel_manager.kernel
		self.kernel.gui = 'qt4'
		self.kernel_client = self.kernel_manager.client()
		self.kernel_client.start_channels()
		
		def stop():
			kernel_client.stop_channels()
			kernel_manager.shutdown_kernel()
			guisupport.get_app_qt4().exit()

		self.exit_requested.connect(stop)
		
	def executeCmd(self, cmd):
		self.kernel.shell.ex(cmd)

	def evaluateCmd(self, cmd):
		self.kernel.shell.ev(cmd)

	def pushVar(self, **kwarg):
		self.kernel.shell.push(kwarg)
		
	def executeFile(self, file):
		"""Execute a Python file in the interactive namespace."""
		self.shell.safe_execfile(file, self.shell.user_global_ns)
	
	def runCell(self, *args, **kwargs):
		"""Execute a cell."""
		self.shell.run_cell(*args, **kwargs)


class InternalIPKernel(object):
    def init_ipkernel(self, backend):
        # Start IPython kernel with GUI event loop and mpl support
        self.ipkernel = mpl_kernel(backend)
        # To create and track active qt consoles
        self.consoles = []
        
        # This application will also act on the shell user namespace
        self.namespace = self.ipkernel.shell.user_ns

        # Example: a variable that will be seen by the user in the shell, and
        # that the GUI modifies (the 'Counter++' button increments it):
        self.namespace['app_counter'] = 0
        #self.namespace['ipkernel'] = self.ipkernel  # dbg

    def print_namespace(self, evt=None):
        print("\n***Variables in User namespace***")
        for k, v in self.namespace.items():
            if not k.startswith('_'):
                print('%s -> %r' % (k, v))
        sys.stdout.flush()

    def new_qt_console(self, evt=None):
        """start a new qtconsole connected to our kernel"""
        return connect_qtconsole(self.ipkernel.abs_connection_file, profile=self.ipkernel.profile)

    def count(self, evt=None):
        self.namespace['app_counter'] += 1

    def cleanup_consoles(self, evt=None):
        for c in self.consoles:
            c.kill()
			
#class MainWindow(QtWidgets.QMainWindow, InternalIPKernel):
class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		#self.textEdit = QtWidgets.QTextEdit()

		#but1 = QtWidgets.QPushButton('write')
		#but1.clicked.connect(self.but_write)

		#but2 = QtWidgets.QPushButton('read')
		#but2.clicked.connect(self.but_read)

		self.console = JupyterWidget()
		self.console.kernel_client.namespace = self
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)		# always top

		vbox = QtWidgets.QVBoxLayout()
		#hbox = QtWidgets.QHBoxLayout()
		#vbox.addWidget(self.textEdit)
		vbox.addWidget(self.console)
		vbox.setContentsMargins(0, 0, 0, 0)
		vbox.setSpacing(0)
		#hbox.addWidget(but1)
		#hbox.addWidget(but2)
		#vbox.addLayout(hbox)

		b = QtWidgets.QWidget()
		b.setLayout(vbox)
		
		
		self.setCentralWidget(b)
		
		self.setWindowTitle('QtConsole')
		#self.init_ipkernel('qt')
		#self.new_qt_console()

	def closeEvent(self, event):
		#QtWidgets.QMessageBox.information(self, 'Information', "Don't a exit QtConsole.")
		reply = QtWidgets.QMessageBox.question(self, 'Exit', "Are you sure to QtConsole quit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
		if reply == QtWidgets.QMessageBox.Yes:
			self.console.kernel_client.stop_channels()
			self.console.kernel_manager.shutdown_kernel()
			event.accept()
			#guisupport.get_app_qt().exit()
		else:
			event.ignore()
		#if result == QtWidgets.QMessageBox.Yes:
			
		#self.console.kernel_client.stop_channels()
		#self.console.kernel_manager.shutdown_kernel()
		#guisupport.get_app_qt().exit()
		#event.accept()
		#else:
		#event.ignore()
		#self.close(self)
		#self.exit_requested.connect(stop)

	#def but_read(self):
		#self.a['text'] = self.textEdit.toPlainText()
		#self.console.execute("print('a[\\\'text\\\'] = \"'+ a['text'] +'\"')")

	#def but_write(self):
		#self.textEdit.setText(self.a['text'])


if __name__ == '__main__':
	import sys
	
	app = QtWidgets.QApplication.instance()
	main = MainWindow()
	main.show()
	#main.ipkernel.start()
	#guisupport.start_event_loop_qt4(app)

