﻿import Rhino.Geometry as rg
#---------------------------------------------------------------------------------------#

diplacementWrapper = openSeesOutputWrapper[0]
EleOut = openSeesOutputWrapper[2]

pointWrapper = []
transWrapper = []
rotWrapper = []

for index,item in enumerate(diplacementWrapper):
    pointWrapper.append(  rg.Point3d(item[0][0],item[0][1],item[0][2])  )
    if len(item[1]) == 3:
        dispWrapper.append(  rg.Vector3d( item[1][0], item[1][1], item[1][2] ) )
    elif len(item[1]) == 6:
        transWrapper.append(  rg.Vector3d( item[1][0], item[1][1], item[1][2] ) )
        rotWrapper.append(   rg.Vector3d( item[1][3],item[1][4],item[1][5] )  )

Points = pointWrapper
Trans = transWrapper 
Rot = rotWrapper 