#-*- coding: utf-8 -*-
import win32clipboard, datetime
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QVariant

def pegaPtsCp():
    win32clipboard.OpenClipboard()
    dados = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    dados = dados.replace(',','').replace('\r','')
    lstDados = dados.split('\n')
    lstD = [c.split('\t') for c in lstDados if len(c)>0]
    return lstD

def criaLayPtosT(nome, lst1):
    vl = QgsVectorLayer("Point", nome, "memory")
    #pr = vl.dataProvider()
    vl.startEditing()
    vl.addAttribute(QgsField("ID Ponto", QVariant.Int))
    vl.addAttribute(QgsField("X", QVariant.Double))
    vl.addAttribute(QgsField("Y", QVariant.Double))
    vl.updateFields()
    idP = 0
    for p in lst1:
        fet = QgsFeature(vl.pendingFields())
        fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(float(p[0]),float(p[1]))))
        fields = vl.pendingFields()
        fet.setFields( fields, True )
        fet["ID Ponto"] = idP
        fet['X'] = p[0]
        fet['Y'] = p[1]
        pr = vl.dataProvider()
        pr.addFeatures( [ fet ] )
        vl.commitChanges()
        idP +=1
    QgsMapLayerRegistry.instance().addMapLayer(vl)

def criaLayLinha(nome,lstP):
    vl = QgsVectorLayer("Linestring", nome, "memory")
    #pr = vl.dataProvider()
    vl.startEditing()
    vl.addAttribute(QgsField("id", QVariant.Int))
    vl.updateFields()
    fet = QgsFeature(vl.pendingFields())
    lstPP = []
    for p in lstP:
        lstPP.append(QgsPoint(float(p[0]),float(p[1])))
    lstPP.append(QgsPoint(float(lstP[0][0]),float(lstP[0][1])))
    fet.setGeometry(QgsGeometry.fromPolyline(lstPP))
    fields = vl.pendingFields()
    fet.setFields( fields, True )
    fet['id'] = 0
    pr = vl.dataProvider()
    pr.addFeatures( [ fet ] )
    vl.commitChanges()
    QgsMapLayerRegistry.instance().addMapLayer(vl)    

############ MAIN
hora = datetime.datetime.now()
strH = hora.strftime("%d-%m-%Y %Hh%Mm")

#try:
lstP = pegaPtsCp()
intPtsT = QMessageBox.question(iface.mainWindow(),"Pontos", "Faz layer com todos os pontos abaixo?\n\n "+str(lstP),"Ok","Cancel")
if intPtsT ==0:
    criaLayPtosT('pts_'+strH, lstP)
    criaLayLinha('linha_'+strH, lstP)
#except:
#    QMessageBox.critical(iface.mainWindow(),"Erro", u"Erro na leitura do Clipboard ou criação do layer.","Fechar")
