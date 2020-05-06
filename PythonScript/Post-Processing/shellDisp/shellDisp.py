﻿import Rhino.Geometry as rg
#---------------------------------------------------------------------------------------#

diplacementWrapper = openSeesOutputWrapper[0]
EleOut = openSeesOutputWrapper[2]

pointWrapper = []
transWrapper = []
rotWrapper = []

diplacementWrapper = openSeesOutputWrapper[0]
EleOut = openSeesOutputWrapper[2]
nodeValue = []
displacementValue = []
#ShellOut = openSeesOutputWrapper[4]

pointWrapper = []
dispWrapper = []

for index,item in enumerate(diplacementWrapper):
    nodeValue.append( item[0] )
    displacementValue.append( item[1] )
    pointWrapper.append( [index, rg.Point3d(item[0][0],item[0][1],item[0][2]) ] )
    if len(item[1]) == 3:
        dispWrapper.append( [index, rg.Point3d( item[1][0], item[1][1], item[1][2] ) ] )
    elif len(item[1]) == 6:
        dispWrapper.append( [index, [rg.Point3d(item[1][0],item[1][1],item[1][2] ), rg.Point3d(item[1][3],item[1][4],item[1][5]) ] ] )

## Dict. for point ##
pointWrapperDict = dict( pointWrapper )
pointDispWrapperDict = dict( dispWrapper )
####

    
def defShellQuadValue( ele, node, nodeDisp ):
    
    eleTag = ele[0]
    eleNodeTag = ele[1]
    
    index1 = eleNodeTag[0]
    index2 = eleNodeTag[1]
    index3 = eleNodeTag[2]
    index4 = eleNodeTag[3]
    
    trasl1 = nodeDisp.get( index1 -1 , "never")[0]
    rotate1 = nodeDisp.get( index1 -1 , "never")[1]
    
    trasl2 = nodeDisp.get( index2 -1 , "never")[0]
    rotate2 = nodeDisp.get( index2 -1 , "never")[1]
    
    trasl3 = nodeDisp.get( index3 -1 , "never")[0]
    rotate3 = nodeDisp.get( index3 -1 , "never")[1]
    
    trasl4 = nodeDisp.get( index4 -1 , "never")[0]
    rotate4 = nodeDisp.get( index4 -1 , "never")[1]
    
    return  [[trasl1, trasl2, trasl3, trasl4], [rotate1, rotate2, rotate3, rotate4]]

def defShellTriangleValue( ele, node, nodeDisp, scaleDef ):
    
    eleTag = ele[0]
    eleNodeTag = ele[1]
    index1 = eleNodeTag[0]
    index2 = eleNodeTag[1]
    index3 = eleNodeTag[2]
    
    trasl1 = nodeDisp.get( index1 -1 , "never")[0]
    rotate1 = nodeDisp.get( index1 -1 , "never")[1]
    
    trasl2 = nodeDisp.get( index2 -1 , "never")[0]
    rotate2 = nodeDisp.get( index2 -1 , "never")[1]
    
    trasl3 = nodeDisp.get( index3 -1 , "never")[0]
    rotate3 = nodeDisp.get( index3 -1 , "never")[1]
    
    return  [[trasl1, trasl2, trasl3], [rotate1, rotate2, rotate3]]


trans = []
rot = []
tag = []
for ele in EleOut :
    tagEle = ele[0]
    eleType = ele[2][0]
    nNode = len( ele[1] )
    if nNode == 4 and eleType != 'FourNodeTetrahedron':
        trasl = defShellQuadValue( ele, pointWrapperDict, pointDispWrapperDict )
        trans.append(trasl[0])
        rot.append(trasl[1])
        tag.append( tagEle )
        
    elif nNode == 3:
        trasl = defShellTriangleValue( ele, pointWrapperDict, pointDispWrapperDict )
        trans.append(trasl[0])
        rot.append(trasl[1])
        tag.append( tagEle )
        
tagElement = tag
Trans = trans
Rot = rot
