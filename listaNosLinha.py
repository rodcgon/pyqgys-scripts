import math 

layer = iface.activeLayer()
selection = layer.selectedFeatures()
geom = selection[0].geometry()
if geom.type() == QGis.Line:
    lstPts = geom.asPolyline()
elif geom.type() == QGis.Polygon:
    lstPts = geom.asPolygon()[0]
xA = None
aZ = ''
dist = ''
lstAz = []
lstR = []
lstDefl = []
lstTr=[]
strPts = ''
t = 0
for p in lstPts:
    dirL = 0
    if xA != None:
        dirN = p[1] - yA
        dirE = p[0] - xA
        dist = math.sqrt(dirN**2+dirE**2)
        aZ = (180.0/math.pi)*math.atan2(dirE,dirN)
        lstR.append(aZ)
        if aZ<1:
            aZ = aZ+360
        lstAz .append(aZ)
        azPer1 = aZ + 90
        azPer2 = aZ - 90
        if t>0:
            defl = lstAz[t]-lstAz[t-1]
            lstDefl.append(defl)
        lstTr.append([t,dist,aZ,azPer1,azPer2])
        t +=1
        print "X=%.3f" % p[0] , "Y=%.3f" % p[1], ' - Dist.: %.3f' % dist, ' - Azimute: %.2f' % aZ,' graus'
        #print 'azD =  %.2f' % azPer1, ' - azE = %.2f' % azPer2
    else:
        print "X=%.3f" % p[0] , "Y=%.3f" % p[1]
    strPts +="%.3f" % p[0] +'\t'+"%.3f" % p[1]+'\n'
    xA = p[0]
    yA = p[1]
somaDef = sum(lstDefl)
lstEdge = [((lstPts[n+1][0]-lstPts[n][0])*(lstPts[n+1][1] + lstPts[n][1])) for n in range(len(lstPts)-1)]
#print lstPts[n+1][0],lstPts[n][0],lstPts[n+1][1],lstPts[n][1],lstEdge[-1]
#print lstPts[n+1][0]-lstPts[n][0], lstPts[n+1][1]+lstPts[n][1]
#print lstDefl
if sum(lstEdge)>0:
    print 'Sentido horario'
else:
    print 'Sentido Anti-horario'
print
print strPts
