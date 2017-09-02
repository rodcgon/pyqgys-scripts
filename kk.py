#kerby kirpich
from math import sqrt,atan2, degrees,sin, cos,radians
from datetime import datetime
from PyQt4.QtCore import QVariant

MDTNAME = 'arraial_srtm'

def achaRaster(layerMDTName):
    try:
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name() == layerMDTName:
                layMDT = lyr
            else:
                layMDT = Null
    except:
        print 'Nome do layers Raster (MDT) nao encontrado...'
        layMDT = Null
    return layMDT

def pegaCotas(line,nomeMDT):
    rl = achaRaster(nomeMDT)
    dp= rl.dataProvider()
    lstVal = []
    for p in line:
        val = dp.identify(QgsPoint(p),
            QgsRaster.IdentifyFormatValue).results().values()[0]
        lstVal.append(val)
    return lstVal

def criaPLay(pt):
    name = (datetime.now()).strftime('%d%m%y_%H%M')
    vl = QgsVectorLayer("Point", name, "memory") # removed "s" on Points
    pr = vl.dataProvider() # need to create a data provider
    # changes are only possible when editing the layer
    vl.startEditing()
    # add fields
    pr.addAttributes([QgsField("name", QVariant.String)])
    # add a feature
    fet = QgsFeature()
    fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(pt[0],pt[1])))
    fet.setAttributes([name, 2, 0.3])
    pr.addFeatures([fet])
    # commit to stop editing the layer
    vl.commitChanges()
    QgsMapLayerRegistry.instance().addMapLayer(vl)
    return vl

def criaPolyLay(line,prefix):
    name = prefix+'_'+(datetime.now()).strftime('%d%m%y_%H%M')
    vl = QgsVectorLayer("LineString", name, "memory") # removed "s" on Points
    pr = vl.dataProvider() # need to create a data provider
    # changes are only possible when editing the layer
    vl.startEditing()
    # add fields
    pr.addAttributes([QgsField("name", QVariant.String)])
    # add a feature
    fet = QgsFeature()
    qgsLine = [QgsPoint(p[0],p[1]) for p in line]
    fet.setGeometry(QgsGeometry.fromPolyline(qgsLine))
    fet.setAttributes([name, 2, 0.3])
    pr.addFeatures([fet])
    # commit to stop editing the layer
    vl.commitChanges()
    QgsMapLayerRegistry.instance().addMapLayer(vl)
    return vl

def sentidoPL(poly):
    pass

def dist(p1,p2):
    return sqrt((p2[0]-p1[0])**2+(p2[1]-p2[1])**2)

def bearing(p1,p2):
    #tc1=abs(atan2(sin(lon2-lon1)*cos(lat2),cos(lat1)*sin(lat2)- sin(lat1)*cos(lat2)*cos(lon2-lon1)),2*pi)
    bearing = atan2(p2[0]-p1[0],p2[1]-p1[1])
    ang = (degrees(bearing) + 360) % 360
    return ang

def quebra(p1,p2,dI):
    ang = bearing(p1,p2)
    angRad = radians(ang)
    dX = dI * sin(angRad)
    dY = dI * cos(angRad)
    print dX,dY, 'ang=',ang
    xF, yF = p1[0]+dX, p1[1]+dY
    return (xF,yF)


def separaPerf(poly):
    tamKerby = 300.0
    dA=0.0
    for i in range(len(poly)-1):
        d = dist(poly[i],poly[i+1])
        dA+=d
        print dA
        if dA>=tamKerby:
            p1 = poly[i]
            p2 = poly[i+1]
            dR = (dA - tamKerby)
            dI = dist(p1,p2)-dR
            print dI
            if dR>0:
                pSep = quebra(p1,p2,dI)
            else:
                pSep = p2
            break
    else:
        pSep = poly[-1]
        pass
    print i
    lst1 = [poly[n] for n in range(i+1)]+[pSep]
    lst2 = [pSep]+[poly[n] for n in range(i+1,len(poly))]
    criaPLay(pSep)
    return lst1, lst2

def declEq(lay,rl):
    p1 = lay.getFeatures().next().geometry().asPolyline()
    p1 = [(float(p[0]),float(p[1])) for p in p1]
    """
    0 - numero do ponto
    1 - x / long
    2 - y / lat
    3 - distancia entre pontos
    4 - cota segundo raster selecionado
    5 - declividade
    6 - Li / Di ^0.5
    """
    if len(p1)>2:
        lstDist=lstDecl=lstPond=[]
        lstCota = pegaCotas(p1,rl)
        for i in range(len(p1)):
            if i==0:
                distInc=decl=pond= Null
            else:
                distInc = dist(p1[i-1],p1[i])
                lstDist.append(distInc)
                decl = (lstCota[i-1]-lstCota[i])/distInc
                lstDecl.append(distInc)
                pond = distInc/(decl**.5)
                lstPond.append(distInc)
    tab = [lstDist,lstCota, lstDecl,lstPond]
    sEq = (sum(lstDist)/sum(lstPond))**2
    return tab, sEq


def compr(perf):
    pass

def kerby(perf,n):
    #tov= K.(Lov.n)^0,467.S^-0,235
    n=0.4
    pass

def kirpich(perf):
    #tch= K . Lch^0,77 . S^-0,385
    pass

layer = iface.activeLayer()
features = layer.selectedFeatures()
poly = features[0].geometry().asPolyline()
poly = [(float(p[0]),float(p[1])) for p in poly]
l1,l2= separaPerf(poly)
lay1= criaPolyLay(l1,'t1')
lay2 = criaPolyLay(l2,'t2')

tab1, s1 = declEq(lay1,MDTNAME)
tab2, s2 = declEq(lay2,MDTNAME)
print s1, s2