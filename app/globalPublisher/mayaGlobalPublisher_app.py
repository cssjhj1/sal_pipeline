#
# ===== Maya Application template =====
# 

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as apiUI
import shiboken

from functools import partial
import os, sys, subprocess, time, datetime

# ============ Will change to qt.py ============
try:
	from PySide2.QtCore import *
	from PySide2.QtGui import *
	from PySide2.QtWidgets import *
	from PySide2.QtUiTools import *
	from PySide2 import __version__
	import shiboken2 as shiboken

except ImportError:
	from PySide.QtCore import *
	from PySide.QtGui import *
	from PySide.QtUiTools import *
	from PySide import __version__
	import shiboken

# project libs import
from sal_pipeline.src import env
from sal_pipeline.src import utils
reload(utils)
reload(env)

# tool libs import
import mayaGlobalPublisher_core as core
reload(core)

getEnv 	= env.getEnv()
modulepath = getEnv.modulePath()

__app_version__ = '0.1'
# V0.1

try:
	myInfo = env.getInfo()
except KeyError :
	raise IOError("This file is not in pipeline. please check your file.")

class mayaGlobalPublisher( QMainWindow ):

	_pubThumbnail_Path = ''

	def __init__(self, parent=None):
		""" Description """
		QMainWindow.__init__(self, parent)

		_uiFilename_ = 'Maya_GlobalPublish.ui'
		_uiFilePath_ = modulepath + '/ui/' + _uiFilename_		

		# Check is ui file exists?
		if not os.path.isfile( _uiFilePath_ ):
			cmds.error( 'File ui not found.' )

		# ---- LoadUI -----
		loader = QUiLoader()
		currentDir = os.path.dirname(__file__)
		file = QFile( _uiFilePath_ )
		file.open(QFile.ReadOnly)
		self.ui = loader.load(file, parentWidget=self)
		file.close()
		# -----------------

		self.ui.setWindowTitle('Maya global publisher v.' + str(__app_version__))

		self._initUI()
		self.ui.show()

	def _initUI(self):
		self.ui.lineEdit_publisher.setText( myInfo.getUsername() )
		self.ui.label_pubFileName.setText(  myInfo.get_pubName() )
		self.ui.label_filePath.setText( cmds.file(q=True, sn=True) )
		self.ui.label_dateTime.setText( str(time.strftime("%d/%m/%Y %H:%M %p",time.localtime())))

		self.ui.comboBox_pipelineStep.addItem("model")

		# capture viewport
		self.setThumbnail( self.captureViewport() )

	def _initConnect(self):
		pass

	def captureViewport(self):

		filePath = cmds.file(q=True, sn=True)
		if myInfo.isType() == 'shot':
			workspace = '/'.join( filePath.split('/')[:-2] )
		else :
			workspace = '/'.join( filePath.split('/')[:-3] )

		# generate unique filename
		_pubThumbnail_Path 	= "{0}/_thumbnail".format(workspace)
		thumbnail_file		= "pub_temp"

		#capture
		self._pubThumbnail_Path = utils.utils().captureViewport( outputdir = _pubThumbnail_Path, filename = thumbnail_file )
		
		return self._pubThumbnail_Path

	def setThumbnail(self, imagePath):

		if not os.path.exists(imagePath):
			imagePath = ''
			self.pixmap_Placeholder.setText(imagePath)
			return

		pixmap = QPixmap( imagePath )
		pixmap = pixmap.scaledToWidth(240)
		self.ui.label_imagePlaceHolder.setPixmap(pixmap)


#####################################################################

def openExplorer(filePath):
	"""Open File explorer after finish."""
	win_publishPath = filePath.replace('/', '\\')
	subprocess.Popen('explorer \/select,\"%s\"' % win_publishPath)

def getMayaWindow():
	"""
	Get the main Maya window as a QMainWindow instance
	@return: QMainWindow instance of the top level Maya windows
	"""
	ptr = apiUI.MQtUtil.mainWindow()
	if ptr is not None:
		return shiboken.wrapInstance(long(ptr), QWidget)

def clearUI():
	if cmds.window('sal_globalPublisher',exists=True):
		cmds.deleteUI('sal_globalPublisher')
		clearUI()

def run():
	clearUI()
	app = mayaGlobalPublisher( getMayaWindow() )
	# pass

if __name__ == '__main__':
	run()