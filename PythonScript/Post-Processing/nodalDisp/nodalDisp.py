﻿"""Generate Model view 
    Inputs:
        AlpacaStaticOutput: Static Analyses output solver.
    Output:
       Points : points of the model .
       Trans : Translation of the model points.
       Rot : Rotation of the model points.
       """

import Rhino.Geometry as rg
import Grasshopper as gh
#---------------------------------------------------------------------------------------#
def NodeDisp( AlpacaStaticOutput ):
        # define output

    global Points
    global Trans
    global Rot
    
    diplacementWrapper = AlpacaStaticOutput[0]
    EleOut = AlpacaStaticOutput[2]

    pointWrapper = []
    transWrapper = []
    rotWrapper = []
    #print(diplacementWrapper[0])
    for index,item in enumerate(diplacementWrapper):
        pointWrapper.append(  rg.Point3d(item[0][0],item[0][1],item[0][2])  )
        if len(item[1]) == 3:
            transWrapper.append(  rg.Vector3d( item[1][0], item[1][1], item[1][2] ) )
            rotWrapper.append(   rg.Vector3d( 0,0,0 )  )
    
        elif len(item[1]) == 6:
            transWrapper.append(  rg.Vector3d( item[1][0], item[1][1], item[1][2] ) )
            rotWrapper.append(   rg.Vector3d( item[1][3],item[1][4],item[1][5] )  )
    
    Points = pointWrapper
    Trans = transWrapper 
    Rot = rotWrapper 

    return Points, Trans, Rot


checkData = True

if not AlpacaStaticOutput :
    checkData = False
    msg = "input 'AlpacaStaticOutput' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if checkData != False:
    Points, Trans, Rot = NodeDisp( AlpacaStaticOutput )