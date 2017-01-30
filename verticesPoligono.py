import math

features = layer.selectedFeatures()
polygon = features[0].geometry().asPolygon()
n = len(polygon[0])
lstP = [(round(polygon[0][i][0],2),round(polygon[0][i][1],2)) for i in range(n)]
for i in range(n):
    #print polygon[0][i][0]
        p = lstP[i]
        print 'Vertice ',i+1," - %.2f , %.2f" % (round(polygon[0][i][0],2),round(polygon[0][i][1],2)),
        if i>0:
            dirN = lstP[i][1] - lstP[i-1][1]
            dirE = lstP[i][0] - lstP[i-1][0]
            dist = math.sqrt(dirN**2+dirE**2)
            aZ = (180.0/math.pi)*math.atan2(dirE,dirN)
        else:
            dirN = 0
            dirE = 0
            dist = 0
            aZ  = 0
        print ' - Dist.=',round(dist,2), ' - Azim=', aZ
