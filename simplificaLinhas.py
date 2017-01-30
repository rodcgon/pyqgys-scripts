#-*-coding: utf-8 -*-
## Filtra linha de acordo com dist minima e angulo de deflexao minimo
from PyQt4.QtGui import QMessageBox
import math
from PyQt4.QtCore import QVariant
import datetime

dLim = 1
angL = 1
hora = datetime.datetime.now()
strH = hora.strftime("%d-%m-%Y %H:%M")
nome = 'layer_simplificado_'+strH

def simplLstP(lstP,dLim, angL):
    lstNew = [lstP[0]]
    lstAz=[]
    listDefl =[]
    for p in range(1,len(lstP)):
        dirN = lstP[p][1] - lstP[p-1][1]
        dirE = lstP[p][0] - lstP[p-1][0]
        dist = math.sqrt(dirN**2+dirE**2)
        aZ1 = (180.0/math.pi)*math.atan2(dirE,dirN)
        lstAz.append(aZ1)
        defl = 0
        if p>1:
            aZ1 = (180.0/math.pi)*math.atan2(dirE,dirN)
            defl = abs(aZ1 - lstAz[p-2])
            #print lstP[p][0], dist, defl
            if dist>dLim and defl>angL:
                lstNew.append(lstP[p])
            else:
                lstNew[-1]=lstP[p]
        else:
            if dist>dLim:
                lstNew.append(lstP[p])
        #print lstP[p][0], dist, aZ1, defl
    return lstNew

def criaLayLinhas(nome,lstEl):
    vl = QgsVectorLayer("LineString", nome, "memory")
    #pr = vl.dataProvider()
    vl.startEditing()
    vl.addAttribute(QgsField("id", QVariant.Int))
    vl.updateFields()
    for pol in range(len(lstEl)):
            fet = QgsFeature(vl.pendingFields())
            lstPP = []
            for p in lstEl[pol]:
                lstPP.append(QgsPoint(p[0],p[1]))
            fet.setGeometry(QgsGeometry.fromPolyline(lstPP))
            fields = vl.pendingFields()
            fet.setFields( fields, True )
            #fet['id'] = i
            pr = vl.dataProvider()
            pr.addFeatures( [ fet ] )
            vl.commitChanges()
    QgsMapLayerRegistry.instance().addMapLayer(vl)

################### MAIN CODE

layer = iface.activeLayer()
if layer.type() == QgsMapLayer.VectorLayer and layer.wkbType() == QGis.WKBLineString:
    intSel = QMessageBox.question(iface.mainWindow(),u"Selection", "All entities or only selected entities?","ALL","ONLY SELECTED")
    if intSel ==0:
        selection = layer.getFeatures()
    else:
        selection = layer.selectedFeatures()
    lstAllEl = []
    for s in selection:
        geom = s.geometry()
        lstPts = geom.asPolyline()
        tamAntes= len(lstPts)
        lstNew = simplLstP(lstPts,dLim, angL)
        tamDepois= len(lstNew)
        print 'Retirados ',tamAntes-tamDepois, ' vertices.'
        lstAllEl.append(lstNew)
    criaLayLinhas(nome,lstAllEl)
        
else:
    QMessageBox.critical(iface.mainWindow(),"Layer", u"Layer inválido.","Ok")
    
    