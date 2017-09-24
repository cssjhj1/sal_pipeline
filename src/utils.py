import maya.cmds as cmds

import PySide.QtCore as QtCore
import PySide.QtGui	 as QtGui
import PySide.QtUiTools as QtUiTools
import os, sys, zipfile

from sal_pipeline.src import env
reload(env)

class windows(object):

	def __init__(self):
		pass

	def progressbar(self):
		pass

	def inputDialog(self, parent=None, title ='title', message='message?' ):
		'''  
			input dialog template

			@parent
			@title
			@message

			return : input message, False if cancle
		'''

		if parent == None:
			parent = QtGui.QWidget()

		text, ok = QtGui.QInputDialog.getText(parent, title, message)
		if ok:
			pass
		else:
			text = False
			print ('Cancle.')

		return text

class utils(object):

	def __init__(self):
		pass

	def jsonLoader(self):
		pass

	def jsonDumper(self):
		pass

	def unzip(self, zipPath, dest):

		if not os.path.exists(zipPath):
			print ('Zip file not fould.')
			return

		if not os.path.exists(dest):
			print('Destination folder not exists.')
			return

		try:
			zfile = zipfile.ZipFile( zipPath )
			zfile.extractall( dest )
		except Exception as e:
			raise(e)

		return dest

if __name__ == '__main__':
	
	# Test inputDialog
	#
	# app = windows()
	# gui = QtGui.QWidget()
	# app.inputDialog(parent= gui)

	# Test zipfile
	#
	zipfilePath = "D:/WORK/Programming/sal_pipeline/data/shot_template.zip"
	dest = "D:/WORK/Pipeline_projectSetup/production/film/sq20/sh300"

	app = utils()
	result = app.unzip(zipPath=zipfilePath, dest=dest)
	print result