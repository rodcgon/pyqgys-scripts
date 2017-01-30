from PyQt4.QtGui import QFileDialog
#import os

projP = QgsProject.instance().readPath("./")
fileN =QFileDialog.getSaveFileName(None, "Nome de arquivo imagem para salvar a Captura de Tela:",projP,"Image Files (*.png)")
print 'file=',fileN
if fileN!='':
    qgis.utils.iface.mapCanvas().saveAsImage(fileN)
