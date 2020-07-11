"""Generate Model view 
    Inputs:
        AlpacaStaticOutput: Output of solver on static Analyses.

        direction : view relative color of the traslation:
            '0' view traslation X.
            '1' view traslation Y.
            '2' view traslation Z.

        scale: number that multiplies the real displacements. 

        modelExstrud : 'True' = view exstrude model, 'False' = view analitic model. 

    Output:
       ModelDisp: view deformed model :
       beam --> polyline;
       shell --> mesh;
       brick --> solid .
       ModelCurve : analitic line ( polyline) of the beam or truss Element .
       max_min : max end min of displacement of the structure .
       """

import Rhino.Geometry as rg
import math as mt
import ghpythonlib.treehelpers as th # per data tree
#import ghpythonlib.components as ghcomp
import Grasshopper as gh
#import System as sy #DV
import sys
import rhinoscriptsyntax as rs
import Rhino.Display as rd
from scriptcontext import doc

'''
ghFilePath = ghenv.LocalScope.ghdoc.Path
ghFileName = ghenv.LocalScope.ghdoc.Name
folderNameLength = len(ghFilePath)-len(ghFileName)-2 #have to remove '.gh'
ghFolderPath = ghFilePath[0:folderNameLength]

outputPath = ghFolderPath + 'assembleData'
wrapperFile = ghFolderPath + 'assembleData\\openSeesModel.txt'

userObjectFolder = Grasshopper.Folders.DefaultUserObjectFolder
fileName = userObjectFolder + 'Alpaca'
'''
fileName = r'C:\GitHub\Alpaca4d\PythonScript\function'
sys.path.append(fileName)
# importante mettere import 'import Rhino.Geometry as rg' prima di importatre DomeFunc
import DomeFunc as dg 

#---------------------------------------------------------------------------------------#
## Funzione cerchio ##
def AddCircleFromCenter( plane, radius):
    t = dg.linspace( 0 , 1.80*mt.pi, 16 )
    a = []
    for ti in t:
        x = radius*mt.cos(ti)
        y = radius*mt.sin(ti)
        a.append( plane.PointAt( x, y ) )
    #circle = rg.PolylineCurve( a )
    circle  = a 
    return circle

def AddIFromCenter(plane, Bsup, tsup, Binf, tinf, H, ta, yg):
    #-------------------1---------2 #
    '''
    p1 = plane.PointAt(ta/2, -(yg - tinf) )
    p2 = plane.PointAt( Binf/2,  -(yg - tinf) )
    p3 = plane.PointAt( Binf/2,  -yg )
    p4 = plane.PointAt( -Binf/2,  -yg )
    p5 = plane.PointAt( -Binf/2, -(yg - tinf) ) 
    p6 = plane.PointAt( -ta/2,  -(yg - tinf) )
    p7 = plane.PointAt( -ta/2,  (H - yg - tsup))
    p8 = plane.PointAt( -Bsup/2,  (H - yg - tsup) )
    p9 = plane.PointAt( -Bsup/2,  (H - yg ) )
    p10 = plane.PointAt( Bsup/2,  (H - yg ) )
    p11 = plane.PointAt( Bsup/2,  (H - yg - tsup) )
    p12 = plane.PointAt( ta/2,  (H - yg - tsup) )
    '''
    p1 = plane.PointAt( -(yg - tinf), ta/2 )
    p2 = plane.PointAt( -(yg - tinf), Binf/2 )
    p3 = plane.PointAt( -yg, Binf/2 )
    p4 = plane.PointAt( -yg, -Binf/2 )
    p5 = plane.PointAt( -(yg - tinf), -Binf/2 ) 
    p6 = plane.PointAt( -(yg - tinf), -ta/2 )
    p7 = plane.PointAt( (H - yg - tsup), -ta/2)
    p8 = plane.PointAt( (H - yg - tsup), -Bsup/2 )
    p9 = plane.PointAt( (H - yg ), -Bsup/2 )
    p10 = plane.PointAt( (H - yg ), Bsup/2 )
    p11 = plane.PointAt( (H - yg - tsup), Bsup/2 )
    p12 = plane.PointAt( (H - yg - tsup), ta/2 )

    wirframe  = [ p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12 ] 
    return wirframe

def defShellQuad( ele, node, nodeDisp, scaleDef ):
    
    eleTag = ele[0]
    eleNodeTag = ele[1]
    color = ele[2][2]
    thick = ele[2][1]
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
    
    ## CREO IL MODELLO DEFORMATO  ##
    
    pointDef1 = rg.Point3d.Clone( node.get( index1 -1 , "never") )
    pointDef2 = rg.Point3d.Clone( node.get( index2 -1 , "never") )
    pointDef3 = rg.Point3d.Clone( node.get( index3 -1 , "never") )
    pointDef4 = rg.Point3d.Clone( node.get( index4 -1 , "never") )
    vectortrasl1 = rg.Transform.Translation( rg.Vector3d(trasl1.X, trasl1.Y, trasl1.Z)*scaleDef )
    pointDef1.Transform( vectortrasl1 )
    vectortrasl2 = rg.Transform.Translation( rg.Vector3d(trasl2.X, trasl2.Y, trasl2.Z)*scaleDef )
    pointDef2.Transform( vectortrasl2 )
    vectortrasl3 = rg.Transform.Translation( rg.Vector3d(trasl3.X, trasl3.Y, trasl3.Z)*scaleDef )
    pointDef3.Transform( vectortrasl3 )
    vectortrasl4 = rg.Transform.Translation( rg.Vector3d(trasl4.X, trasl4.Y, trasl4.Z)*scaleDef )
    pointDef4.Transform( vectortrasl4 )
    shellDefModel = rg.Mesh()
    shellDefModel.Vertices.Add( pointDef1 ) #0
    shellDefModel.Vertices.Add( pointDef2 ) #1
    shellDefModel.Vertices.Add( pointDef3 ) #2
    shellDefModel.Vertices.Add( pointDef4 ) #3
    
    
    shellDefModel.Faces.AddFace(0, 1, 2, 3)
    colour = rs.CreateColor( color[0], color[1], color[2] )
    shellDefModel.VertexColors.CreateMonotoneMesh( colour )

    vt = shellDefModel.Vertices
    shellDefModel.FaceNormals.ComputeFaceNormals()
    fid,MPt = shellDefModel.ClosestPoint(vt[0],0.01)
    normalFace = shellDefModel.FaceNormals[fid]
    vectormoltiplicate = rg.Vector3d.Multiply( -normalFace, thick/2 )
    trasl = rg.Transform.Translation( vectormoltiplicate )
    moveShell = rg.Mesh.DuplicateMesh(shellDefModel)
    moveShell.Transform( trasl )
    extrudeShell = rg.Mesh.Offset( moveShell, thick, True, normalFace)
    return  [shellDefModel,[trasl1, trasl2, trasl3, trasl4], [rotate1, rotate2, rotate3, rotate4], extrudeShell ]

def defShellTriangle( ele, node, nodeDisp, scaleDef ):
    
    eleTag = ele[0]
    eleNodeTag = ele[1]
    color = ele[2][1]
    index1 = eleNodeTag[0]
    index2 = eleNodeTag[1]
    index3 = eleNodeTag[2]
    
    trasl1 = nodeDisp.get( index1 -1 , "never")[0]
    rotate1 = nodeDisp.get( index1 -1 , "never")[1]
    
    trasl2 = nodeDisp.get( index2 -1 , "never")[0]
    rotate2 = nodeDisp.get( index2 -1 , "never")[1]
    
    trasl3 = nodeDisp.get( index3 -1 , "never")[0]
    rotate3 = nodeDisp.get( index3 -1 , "never")[1]
    
    ## CREO IL MODELLO DEFORMATO  ##
    pointDef1 = rg.Point3d.Clone( node.get( index1 -1 , "never") )
    pointDef2 = rg.Point3d.Clone( node.get( index2 -1 , "never") )
    pointDef3 = rg.Point3d.Clone( node.get( index3 -1 , "never") )
    vectortrasl1 = rg.Transform.Translation( rg.Vector3d(trasl1.X, trasl1.Y, trasl1.Z)*scaleDef )
    pointDef1.Transform( vectortrasl1 )
    vectortrasl2 = rg.Transform.Translation( rg.Vector3d(trasl2.X, trasl2.Y, trasl2.Z)*scaleDef )
    pointDef2.Transform( vectortrasl2 )
    vectortrasl3 = rg.Transform.Translation( rg.Vector3d(trasl3.X, trasl3.Y, trasl3.Z)*scaleDef )
    pointDef3.Transform( vectortrasl3 )
    shellDefModel = rg.Mesh()
    shellDefModel.Vertices.Add( pointDef1 ) #0
    shellDefModel.Vertices.Add( pointDef2 ) #1
    shellDefModel.Vertices.Add( pointDef3 ) #2
    
    shellDefModel.Faces.AddFace(0, 1, 2)
    colour = rs.CreateColor( color[0], color[1], color[2] )
    vt = shellDefModel.Vertices
    shellDefModel.FaceNormals.ComputeFaceNormals()
    fid,MPt = shellDefModel.ClosestPoint(vt[0],0.01)
    normalFace = shellDefModel.FaceNormals[fid]
    vectormoltiplicate = rg.Vector3d.Multiply( -normalFace, thick/2 )
    trasl = rg.Transform.Translation( vectormoltiplicate )
    moveShell = rg.Mesh.DuplicateMesh(shellDefModel)
    moveShell.Transform( trasl )
    extrudeShell = rg.Mesh.Offset( moveShell, thick, True, normalFace)
    return  [shellDefModel,[trasl1, trasl2, trasl3], [rotate1, rotate2, rotate3], extrudeShell ]

def defSolid( ele, node, nodeDisp, scaleDef ):
    
    eleTag = ele[0]
    eleNodeTag = ele[1]
    color = ele[2][1]
    thick = ele[2][1]
    #print( eleNodeTag )
    index1 = eleNodeTag[0]
    index2 = eleNodeTag[1]
    index3 = eleNodeTag[2]
    index4 = eleNodeTag[3]
    index5 = eleNodeTag[4]
    index6 = eleNodeTag[5]
    index7 = eleNodeTag[6]
    index8 = eleNodeTag[7]
    
    trasl1 = nodeDisp.get( index1 -1 , "never")
    trasl2 = nodeDisp.get( index2 -1 , "never")
    trasl3 = nodeDisp.get( index3 -1 , "never")
    trasl4 = nodeDisp.get( index4 -1 , "never")
    trasl5 = nodeDisp.get( index5 -1 , "never")
    trasl6 = nodeDisp.get( index6 -1 , "never")
    trasl7 = nodeDisp.get( index7 -1 , "never")
    trasl8 = nodeDisp.get( index8 -1 , "never")
    #print( trasl1 )
    ## CREO IL MODELLO DEFORMATO  ##
    pointDef1 = rg.Point3d.Clone( node.get( index1 -1 , "never") )
    pointDef2 = rg.Point3d.Clone( node.get( index2 -1 , "never") )
    pointDef3 = rg.Point3d.Clone( node.get( index3 -1 , "never") )
    pointDef4 = rg.Point3d.Clone( node.get( index4 -1 , "never") )
    pointDef5 = rg.Point3d.Clone( node.get( index5 -1 , "never") )
    pointDef6 = rg.Point3d.Clone( node.get( index6 -1 , "never") )
    pointDef7 = rg.Point3d.Clone( node.get( index7 -1 , "never") )
    pointDef8 = rg.Point3d.Clone( node.get( index8 -1 , "never") )
    vectortrasl1 = rg.Transform.Translation( rg.Vector3d(trasl1.X, trasl1.Y, trasl1.Z)*scaleDef )
    pointDef1.Transform( vectortrasl1 )
    vectortrasl2 = rg.Transform.Translation( rg.Vector3d(trasl2.X, trasl2.Y, trasl2.Z)*scaleDef )
    pointDef2.Transform( vectortrasl2 )
    vectortrasl3 = rg.Transform.Translation( rg.Vector3d(trasl3.X, trasl3.Y, trasl3.Z)*scaleDef )
    pointDef3.Transform( vectortrasl3 )
    vectortrasl4 = rg.Transform.Translation( rg.Vector3d(trasl4.X, trasl4.Y, trasl4.Z)*scaleDef )
    pointDef4.Transform( vectortrasl4 )
    vectortrasl5 = rg.Transform.Translation( rg.Vector3d(trasl5.X, trasl5.Y, trasl5.Z)*scaleDef )
    pointDef5.Transform( vectortrasl1 )
    vectortrasl6 = rg.Transform.Translation( rg.Vector3d(trasl6.X, trasl6.Y, trasl6.Z)*scaleDef )
    pointDef6.Transform( vectortrasl2 )
    vectortrasl7 = rg.Transform.Translation( rg.Vector3d(trasl7.X, trasl7.Y, trasl7.Z)*scaleDef )
    pointDef7.Transform( vectortrasl3 )
    vectortrasl8 = rg.Transform.Translation( rg.Vector3d(trasl8.X, trasl8.Y, trasl8.Z)*scaleDef )
    pointDef8.Transform( vectortrasl4 )
    
    shellDefModel = rg.Mesh()
    shellDefModel.Vertices.Add( pointDef1 ) #0
    shellDefModel.Vertices.Add( pointDef2 ) #1
    shellDefModel.Vertices.Add( pointDef3 ) #2
    shellDefModel.Vertices.Add( pointDef4 ) #3
    shellDefModel.Vertices.Add( pointDef5 ) #4
    shellDefModel.Vertices.Add( pointDef6 ) #5
    shellDefModel.Vertices.Add( pointDef7 ) #6
    shellDefModel.Vertices.Add( pointDef8 ) #7

    shellDefModel.Faces.AddFace(0, 1, 2, 3)
    shellDefModel.Faces.AddFace(4, 5, 6, 7)
    shellDefModel.Faces.AddFace(0, 1, 5, 4)
    shellDefModel.Faces.AddFace(1, 2, 6, 5)
    shellDefModel.Faces.AddFace(2, 3, 7, 6)
    shellDefModel.Faces.AddFace(3, 0, 4, 7)
    
    colour = rs.CreateColor( color[0], color[1], color[2] )
    shellDefModel.VertexColors.CreateMonotoneMesh( colour )
    return  [shellDefModel,[trasl1, trasl2, trasl3,trasl4, trasl5, trasl6, trasl7, trasl8 ]]

def defTetraSolid( ele, node, nodeDisp, scaleDef ):
    
    eleTag = ele[0]
    eleNodeTag = ele[1]
    color = ele[2][1]
    #print( eleNodeTag )
    index1 = eleNodeTag[0]
    index2 = eleNodeTag[1]
    index3 = eleNodeTag[2]
    index4 = eleNodeTag[3]
    
    trasl1 = nodeDisp.get( index1 -1 , "never")
    trasl2 = nodeDisp.get( index2 -1 , "never")
    trasl3 = nodeDisp.get( index3 -1 , "never")
    trasl4 = nodeDisp.get( index4 -1 , "never")
    
    ## CREO IL MODELLO DEFORMATO  ##
    pointDef1 = rg.Point3d.Clone( node.get( index1 -1 , "never") )
    pointDef2 = rg.Point3d.Clone( node.get( index2 -1 , "never") )
    pointDef3 = rg.Point3d.Clone( node.get( index3 -1 , "never") )
    pointDef4 = rg.Point3d.Clone( node.get( index4 -1 , "never") )
    
    vectortrasl1 = rg.Transform.Translation( rg.Vector3d(trasl1.X, trasl1.Y, trasl1.Z)*scaleDef )
    pointDef1.Transform( vectortrasl1 )
    vectortrasl2 = rg.Transform.Translation( rg.Vector3d(trasl2.X, trasl2.Y, trasl2.Z)*scaleDef )
    pointDef2.Transform( vectortrasl2 )
    vectortrasl3 = rg.Transform.Translation( rg.Vector3d(trasl3.X, trasl3.Y, trasl3.Z)*scaleDef )
    pointDef3.Transform( vectortrasl3 )
    vectortrasl4 = rg.Transform.Translation( rg.Vector3d(trasl4.X, trasl4.Y, trasl4.Z)*scaleDef )
    pointDef4.Transform( vectortrasl4 )

    shellDefModel = rg.Mesh()
    shellDefModel.Vertices.Add( pointDef1 ) #0
    shellDefModel.Vertices.Add( pointDef2 ) #1
    shellDefModel.Vertices.Add( pointDef3 ) #2
    shellDefModel.Vertices.Add( pointDef4 ) #3
    
    
    shellDefModel.Faces.AddFace( 0, 1, 2 )
    shellDefModel.Faces.AddFace( 0, 1, 3 )
    shellDefModel.Faces.AddFace( 1, 2, 3 )
    shellDefModel.Faces.AddFace( 0, 2, 3 )
    colour = rs.CreateColor( color[0], color[1], color[2] )
    shellDefModel.VertexColors.CreateMonotoneMesh( colour )
    
    return  [shellDefModel,[trasl1, trasl2, trasl3, trasl4]]
## node e nodeDisp son dictionary ##
def defValueTimoshenkoBeam( ele, node, nodeDisp, scaleDef ):
    #---------------- WORLD PLANE ----------------------#
    WorldPlane = rg.Plane.WorldXY
    #--------- Propriety TimoshenkoBeam  ----------------#
    TagEle = ele[0]
    propSection = ele[2]
    indexStart = ele[1][0]
    indexEnd = ele[1][1]
    color = propSection[12]
    E = propSection[1]
    G = propSection[2]
    A = propSection[3]
    Avz = propSection[4]
    Avy = propSection[5]
    Jxx = propSection[6]
    Iy = propSection[7]
    Iz = propSection[8]
    #---- traslation and rotation index start & end ------- #
    traslStart = nodeDisp.get( indexStart -1 , "never")[0]
    rotateStart = nodeDisp.get( indexStart -1 , "never")[1]
    traslEnd = nodeDisp.get( indexEnd -1 , "never")[0]
    rotateEnd = nodeDisp.get( indexEnd -1 , "never")[1]
    ##-------------------------------------------- ------------##
    pointStart = node.get( indexStart -1 , "never")
    pointEnd = node.get( indexEnd -1 , "never")
    line = rg.LineCurve( pointStart, pointEnd )
    #-------------------------versor ---------------------------#
    axis1 =  rg.Vector3d( propSection[9][0][0], propSection[9][0][1], propSection[9][0][2]  )
    axis2 =  rg.Vector3d( propSection[9][1][0], propSection[9][1][1], propSection[9][1][2]  )
    axis3 =  rg.Vector3d( propSection[9][2][0], propSection[9][2][1], propSection[9][2][2]  )
    versor = [ axis1, axis2, axis3 ] 
    #---------- WORLD PLANE on point start of line ---------------#
    traslPlane = rg.Transform.Translation( pointStart.X, pointStart.Y, pointStart.Z )
    WorldPlane.Transform( traslPlane )
    #-------------------------------------------------------------#
    planeStart = rg.Plane( pointStart, axis1, axis2 )
    #planeStart = rg.Plane(pointStart, axis3 )
    localPlane = planeStart
    xform = rg.Transform.ChangeBasis( WorldPlane, localPlane )
    localTraslStart = rg.Point3d( traslStart )
    vectorTrasform = rg.Transform.TransformList( xform, [ traslStart, rotateStart, traslEnd, rotateEnd ] )
    #print( vectorTrasform[0] )
    localTraslStart = vectorTrasform[0]
    uI1 = localTraslStart.X # spostamento in direzione dell'asse rosso 
    uI2 = localTraslStart.Y # spostamento in direzione dell'asse verde
    uI3 = localTraslStart.Z # spostamento linea d'asse
    localRotStart = vectorTrasform[1]
    rI1 = localRotStart.X # 
    rI2 = localRotStart.Y # 
    rI3 = localRotStart.Z # 
    localTraslEnd = vectorTrasform[2]
    uJ1 = localTraslEnd.X # spostamento in direzione dell'asse rosso 
    uJ2 = localTraslEnd.Y # spostamento in direzione dell'asse verde
    uJ3 = localTraslEnd.Z # spostamento linea d'asse
    localRotEnd = vectorTrasform[3]
    rJ1 = localRotEnd[0] #  
    rJ2 = localRotEnd[1]  # 
    rJ3 = localRotEnd[2]  # 
    ##------------------ displacement value -------------------------##
    Length = rg.Curve.GetLength( line )
    divideDistance = 0.5
    DivCurve = line.DivideByLength( divideDistance, True )
    if DivCurve == None:
        DivCurve = [ 0, Length]
        
    #s = dg.linspace(0,Length, len(PointsDivLength))
    AlphaY = dg.alphat( E, G, Iy, Avz )
    AlphaZ = dg.alphat( E, G, Iz, Avy )
    
    globalTransVector = []
    globalRotVector = []
    defPoint = []
    defSection = []
    #----------------------- local to global-------------------------#
    xform2 = xform.TryGetInverse()
    #----------------------------------------------------------------#
    for index, x in enumerate(DivCurve):
        beamPoint = line.PointAt(DivCurve[index]) 
        ## SPOSTAMENTO IN DIREZIONE DELL' ASSE 3 ##
        u3 = dg.spostu(x, Length, uI3, uJ3)
        u3Vector = u3*axis3
        ## SPOSTAMENTO IN DIREZIONE DELL' ASSE 1 ##
        v1 =  dg.spostv(x, Length, uI1, uJ1, rI2, rJ2, AlphaY)
        v1Vector = v1*axis1 
        ## SPOSTAMENTO IN DIREZIONE DELL' ASSE 2 ##
        v2 =  dg.spostw(x, Length, uI2, uJ2, rI1, rJ1, AlphaZ)
        v2Vector = v2*axis2 
        
        ## RISULTANTE SPOSTAMENTI ##
        transResult = v1Vector + v2Vector + u3Vector
        

        r1x =  dg.psiy(x, Length, uI2, uJ2, rI1, rJ1, AlphaZ)
        r2x =  dg.thetaz(x, Length, uI1, uJ1, rI2, rJ2, AlphaY)
        r3x = dg.phix(x, Length, rI3, rJ3)
        
        rotResult = r1x*axis1 + r2x*axis2 + r3x*axis3
        
        trasl = rg.Transform.Translation( transResult*scaleDef )
        beamPoint.Transform( trasl )
        defPoint.append( beamPoint )
        sectionPlane = rg.Plane( beamPoint, axis1, axis2 )
        sectionPlane.Rotate( scaleDef*r1x, axis1, beamPoint )
        sectionPlane.Rotate( scaleDef*r2x, axis2, beamPoint )
        sectionPlane.Rotate( scaleDef*r3x, axis3, beamPoint )
        if dimSection[0] == 'rectangular' :
            width, height = dimSection[1], dimSection[2]
            section = dg.AddRectangleFromCenter( sectionPlane, width, height )
            defSection.append( section )
        elif dimSection[0] == 'circular' :
            radius1  = dimSection[1]/2
            radius2  = dimSection[1]/2 - dimSection[2]
            section1 = AddCircleFromCenter( sectionPlane, radius1 )
            if (radius1 - radius2 ) == 0 :
                defSection.append( section1 )
            else :
                section2 = AddCircleFromCenter( sectionPlane, radius2 )
                defSection.append( [ section1, section2 ] )
        elif dimSection[0] == 'doubleT' :
            Bsup = dimSection[1]
            tsup = dimSection[2]
            Binf = dimSection[3]
            tinf = dimSection[4]
            H =  dimSection[5]
            ta =  dimSection[6]
            yg =  dimSection[7]
            section = AddIFromCenter( sectionPlane, Bsup, tsup, Binf, tinf, H, ta, yg )
            defSection.append( section )
        elif dimSection[0] == 'rectangularHollow' :
            width, height, thickness = dimSection[1], dimSection[2], dimSection[3]
            section1 = dg.AddRectangleFromCenter( sectionPlane, width, height )
            section2 = dg.AddRectangleFromCenter( sectionPlane, width - (2*thickness), height - (2*thickness) )
            defSection.append( [ section1, section2 ] )
        elif dimSection[0] == 'Generic' :
            radius  = dimSection[1]
            section = AddCircleFromCenter( sectionPlane, radius )
            defSection.append( section )
    
        globalTrasl = rg.Point3d( transResult ) 
        globalTrasl.Transform(xform2[1]) 
        globalTrasl.Transform(xform)
        globalTransVector.append( globalTrasl )

   
    defpolyline = rg.PolylineCurve( defPoint )

    if dimSection[0] == 'circular' :
        radius1  = dimSection[1]/2
        radius2  = dimSection[1]/2 - dimSection[2]
        if (radius1 - radius2 ) == 0:
            meshdef = meshLoft3( defSection,  color )
        else :
            defSection1 = [row[0] for row in defSection ]
            defSection2 = [row[1] for row in defSection ]
            meshdef = meshLoft3( defSection1,  color )
            meshdef.Append( meshLoft3( defSection2,  color ) )
    elif dimSection[0] == 'rectangularHollow' :
            defSection1 = [row[0] for row in defSection ]
            defSection2 = [row[1] for row in defSection ]
            meshdef = meshLoft3( defSection1,  color )
            meshdef.Append( meshLoft3( defSection2,  color ) )
    else  :
        meshdef = meshLoft3( defSection,  color )
    return  [  defpolyline, meshdef ,  globalTransVector, globalRotVector ] 

## node e nodeDisp son dictionary ##
def defTruss( ele, node, nodeDisp, scale ):
    WorldPlane = rg.Plane.WorldXY
    TagEle = ele[0]
    propSection = ele[2]
    color = propSection[12]
    indexStart = ele[1][0]
    indexEnd = ele[1][1]
    E = propSection[1]
    A = propSection[3]
    
    traslStart = nodeDisp.get( indexStart -1 , "never")
    traslEnd = nodeDisp.get( indexEnd -1 , "never")
    if len( traslStart ) == 2:
        traslStart = nodeDisp.get( indexStart -1 , "never")[0]
        traslEnd = nodeDisp.get( indexEnd -1 , "never")[0]
    pointStart = node.get( indexStart -1 , "never")
    pointEnd = node.get( indexEnd -1 , "never")
    #print( traslStart[1] )
    line = rg.LineCurve( pointStart,  pointEnd )
    axis1 =  rg.Vector3d( propSection[9][0][0], propSection[9][0][1], propSection[9][0][2]  )
    axis2 =  rg.Vector3d( propSection[9][1][0], propSection[9][1][1], propSection[9][1][2]  )
    axis3 =  rg.Vector3d( propSection[9][2][0], propSection[9][2][1], propSection[9][2][2]  )
    versor = [ axis1, axis2, axis3 ] 
    #---------- WORLD PLANE on point start of line ---------------#
    traslPlane = rg.Transform.Translation( pointStart.X, pointStart.Y, pointStart.Z )
    WorldPlane.Transform( traslPlane )
    #-------------------------------------------------------------#
    planeStart = rg.Plane(pointStart, axis1, axis2 )
    #planeStart = rg.Plane(pointStart, axis3 )
    localPlane = planeStart
    xform = rg.Transform.ChangeBasis( WorldPlane, localPlane )
    localTraslStart = rg.Point3d( traslStart )
    vectorTrasform = rg.Transform.TransformList( xform, [ traslStart , traslEnd ] )
    #print( vectorTrasform[0] )
    localTraslStart = vectorTrasform[0]
    uI1 = localTraslStart.X # spostamento in direzione dell'asse rosso 
    uI2 = localTraslStart.Y # spostamento in direzione dell'asse verde
    uI3 = localTraslStart.Z # spostamento linea d'asse
    localTraslEnd = vectorTrasform[1]
    uJ1 = localTraslEnd.X # spostamento in direzione dell'asse rosso 
    uJ2 = localTraslEnd.Y # spostamento in direzione dell'asse verde
    uJ3 = localTraslEnd.Z # spostamento linea d'asse
    ##-------------- displacement value -------------------------##
    Length = rg.Curve.GetLength( line )
    divideDistance = 0.5
    DivCurve = line.DivideByLength( divideDistance, True )
    if DivCurve == None:
        DivCurve = [ 0, Length]
    defPoint = []
    defSection = []
    globalTransVector = []
    #----------------------- local to global-------------------------#
    xform2 = xform.TryGetInverse()
    #----------------------------------------------------------------#
    for index, x in enumerate(DivCurve):
        beamPoint = line.PointAt(DivCurve[index]) 
        ## SPOSTAMENTO IN DIREZIONE DELL' ASSE 3 ##
        u3 = dg.spostu(x, Length, uI3, uJ3)
        u3Vector = u3*axis3
        ## SPOSTAMENTO IN DIREZIONE DELL' ASSE 1 ##
        v1 =  x*( uJ1 - uI1 )/Length + uI1
        v1Vector = v1*axis1 
        ## SPOSTAMENTO IN DIREZIONE DELL' ASSE 2 ##
        v2 =  x*( uJ2 - uI2 )/Length + uI2
        v2Vector = v2*axis2 
        ## RISULTANTE SPOSTAMENTI ##
        transResult = v1Vector + v2Vector + u3Vector
        trasl = rg.Transform.Translation( transResult*scale )
        beamPoint.Transform( trasl )
        defPoint.append( beamPoint )
        
        sectionPlane = rg.Plane( beamPoint, axis1, axis2 )
        if dimSection[0] == 'rectangular' :
            width, height = dimSection[1], dimSection[2]
            section = dg.AddRectangleFromCenter( sectionPlane, width, height )
            defSection.append( section )
        elif dimSection[0] == 'circular' :
            radius1  = dimSection[1]/2
            radius2  = dimSection[1]/2 - dimSection[2]
            section1 = AddCircleFromCenter( sectionPlane, radius1 )
            if (radius1 - radius2 ) == 0 :
                defSection.append( section1 )
            else :
                section2 = AddCircleFromCenter( sectionPlane, radius2 )
                defSection.append( [ section1, section2 ] )
        elif dimSection[0] == 'doubleT' :
            Bsup = dimSection[1]
            tsup = dimSection[2]
            Binf = dimSection[3]
            tinf = dimSection[4]
            H =  dimSection[5]
            ta =  dimSection[6]
            yg =  dimSection[7]
            section = AddIFromCenter( sectionPlane, Bsup, tsup, Binf, tinf, H, ta, yg )
            defSection.append( section )
        elif dimSection[0] == 'rectangularHollow' :
            width, height, thickness = dimSection[1], dimSection[2], dimSection[3]
            section1 = dg.AddRectangleFromCenter( sectionPlane, width, height )
            section2 = dg.AddRectangleFromCenter( sectionPlane, width - (2*thickness), height - (2*thickness) )
            defSection.append( [ section1, section2 ] )
        elif dimSection[0] == 'Generic' :
            radius  = dimSection[1]
            section = AddCircleFromCenter( sectionPlane, radius )
            defSection.append( section )
    
        globalTrasl = rg.Point3d( transResult ) 
        globalTrasl.Transform(xform2[1]) 
        globalTrasl.Transform(xform)
        globalTransVector.append( globalTrasl )

   
    defpolyline = rg.PolylineCurve( defPoint )

    if dimSection[0] == 'circular' :
        radius1  = dimSection[1]/2
        radius2  = dimSection[1]/2 - dimSection[2]
        if (radius1 - radius2 ) == 0:
            meshdef = meshLoft3( defSection,  color )
        else :
            defSection1 = [row[0] for row in defSection ]
            defSection2 = [row[1] for row in defSection ]
            meshdef = meshLoft3( defSection1,  color )
            meshdef.Append( meshLoft3( defSection2,  color ) )
    elif dimSection[0] == 'rectangularHollow' :
            defSection1 = [row[0] for row in defSection ]
            defSection2 = [row[1] for row in defSection ]
            meshdef = meshLoft3( defSection1,  color )
            meshdef.Append( meshLoft3( defSection2,  color ) )
    else  :
        meshdef = meshLoft3( defSection,  color )

    return  [ defpolyline, meshdef, globalTransVector]

## Mesh from close section eith gradient color ##
def meshLoft3( point, color ):
    #print( point )
    meshEle = rg.Mesh()
    pointSection1 = point
    for i in range(0,len(pointSection1)):
        for j in range(0, len(pointSection1[0])):
            vertix = pointSection1[i][j]
            #print( type(vertix) )
            meshEle.Vertices.Add( vertix ) 
            #meshEle.VertexColors.Add( color[0],color[1],color[2] );
    k = len(pointSection1[0])
    for i in range(0,len(pointSection1)-1):
        for j in range(0, len(pointSection1[0])):
            if j < k-1:
                index1 = i*k + j
                index2 = (i+1)*k + j
                index3 = index2 + 1
                index4 = index1 + 1
            elif j == k-1:
                index1 = i*k + j
                index2 = (i+1)*k + j
                index3 = (i+1)*k
                index4 = i*k
            meshEle.Faces.AddFace(index1, index2, index3, index4)
            #rs.ObjectColor(scyl,(255,0,0))
    colour = rs.CreateColor( color[0], color[1], color[2] )
    meshEle.VertexColors.CreateMonotoneMesh( colour )
    meshElement = meshEle
    #meshdElement.IsClosed(True)
    
    return meshElement

def gradientJet(value, valueMax, valueMin):

    listcolo = [[0, 0, 102 ],
                [0, 0, 255],
                [0, 64, 255],
                [0, 128, 255],
                [0, 191, 255],
                [0, 255, 255],
                [0, 255, 191],
                [0, 255, 128],
                [0, 255, 64],
                [0, 255, 0],
                [64, 255, 0],
                [128, 255, 0],
                [191, 255, 0],
                [255, 255, 0],
                [255, 191, 0],
                [255, 128, 0],
                [255, 64, 0],
                [255, 0, 0],
                [230, 0, 0],
                [204, 0, 0]]

    #domain = linspace( valueMin,  valueMax, len( listcolo ) )
    n = len( listcolo )
    domain = dg.linspace( valueMin, valueMax, n)
    
    for i in range(1,n):
        if  domain[i-1] <= value <= domain[i]:
            return listcolo[ i-1 ]
        elif  valueMax <= value <= valueMax + 0.00001 :
            return listcolo[ -1 ]
        elif  valueMin - 0.00000000001 <= value <= valueMin  :
            #print( value, valueMin)
            return listcolo[ 0 ]

## Mesh from close section eith gradient color ##
def meshLoft4( point, value, valueMax, valueMin ):
    meshEle = rg.Mesh()
    for i in range(0,len(point)):
        color = gradientJet( value[i], valueMax, valueMin )
        for j in range(0, len(point[0])):
            vertix = point[i][j]
            meshEle.Vertices.Add( vertix ) 
            meshEle.VertexColors.Add( color[0],color[1],color[2] );
    k = len(point[0])
    for i in range(0,len(point)-1):
        for j in range(0, len(point[0])):
            if j < k-1:
                index1 = i*k + j
                index2 = (i+1)*k + j
                index3 = index2 + 1
                index4 = index1 + 1
            elif j == k-1:
                index1 = i*k + j
                index2 = (i+1)*k + j
                index3 = (i+1)*k
                index4 = i*k
            meshEle.Faces.AddFace(index1, index2, index3, index4)
    return meshEle

#----------------------------------------------------------------------#
def defModelView(AlpacaStaticOutput, direction , scale, modelExstrud = False ):

    global ModelDisp
    global ModelCurve
    global max_min
    global dimSection

    #modelExstrud = False if modelExstrud is None else modelExstrud

    diplacementWrapper = AlpacaStaticOutput[0]
    EleOut = AlpacaStaticOutput[2]
    nodeValue = []
    displacementValue = []
    #ShellOut = openSeesOutputWrapper[4]

    pointWrapper = []
    dispWrapper = []
    #print( diplacementWrapper )
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

    ## FOR scala automatica ##
    ## nodeValue è la lista delle cordinate
    rowX = [row[0] for row in nodeValue ]
    rowY = [row[1] for row in nodeValue ]
    rowZ = [row[2] for row in nodeValue ]

    scaleMax = max( max(rowX), max(rowY), max(rowZ) )
    scaleMin = min( min(rowX), min(rowY), min(rowZ) )
    coordMax = max( mt.fabs(scaleMin),mt.fabs(scaleMax)) - mt.fabs(scaleMin)

    ## displacementValue è la lista degli spostamenti

    rowDefX = [row[0] for row in displacementValue ]
    rowDefY = [row[1] for row in displacementValue ]
    rowDefZ = [row[2] for row in displacementValue ]

    defMax = max( max(rowDefX), max(rowDefY), max(rowDefZ) )
    defMin = min( min(rowDefX), min(rowDefY), min(rowDefZ) )
    DefMax = max( mt.fabs(defMax),mt.fabs(defMin))

    if scale == None:
        scaleDef = dg.scaleAutomatic( coordMax , DefMax )

    else :
        scaleDef = scale

    modelCurve = []
    ShellDefModel = []
    ExtrudedView = []
    modelDisp = []

    traslBeamValue = []
    rotBeamValue = []

    traslShellValue = []
    rotShellValue = []
    ExtrudedShell = []

    SolidDefModel = []
    traslSolidValue = []


    for ele in EleOut :
        eleType = ele[2][0]
        nNode = len( ele[1] )
        
        if eleType == 'ElasticTimoshenkoBeam' :
            
            dimSection = ele[2][10]
            color = ele[2][12]
            valueTBeam = defValueTimoshenkoBeam( ele, pointWrapperDict, pointDispWrapperDict, scaleDef )
            defpolyline = valueTBeam[0]
            meshdef = valueTBeam[1]
            globalTrans = valueTBeam[2]
            globalRot = valueTBeam[3]
            traslBeamValue.append( globalTrans ) 
            rotBeamValue.append( globalRot )
            modelCurve.append( defpolyline )
            modelDisp.append( defpolyline )
            # estrusione della beam #
            ExtrudedView.append( meshdef )
            #doc.Objects.AddMesh( meshdef )
        elif eleType == 'Truss' :
            dimSection = ele[2][10]
            color = ele[2][12]
            #print( color )
            valueTruss = defTruss( ele, pointWrapperDict, pointDispWrapperDict, scaleDef )
            defpolyline = valueTruss[0]
            meshdef = valueTruss[1]
            globalTrans = valueTruss[2]
            traslBeamValue.append( globalTrans ) 
            modelCurve.append( defpolyline )
            modelDisp.append( defpolyline )
            ExtrudedView.append( meshdef )
            #doc.Objects.AddMesh( meshdef )

        elif nNode == 4 and eleType != 'FourNodeTetrahedron':
            shellDefModel = defShellQuad( ele, pointWrapperDict, pointDispWrapperDict, scaleDef )
            ShellDefModel.append( shellDefModel[0] )
            traslShellValue.append( shellDefModel[1] )
            rotShellValue.append( shellDefModel[2] )
            extrudeShell = shellDefModel[3]
            ExtrudedView.append( extrudeShell )
            #doc.Objects.AddMesh( extrudeShell)
            
        elif nNode == 3:
            #print( nNode )
            shellDefModel = dg.defShellTriangle( ele, pointWrapperDict, pointDispWrapperDict, scaleDef )
            ShellDefModel.append( shellDefModel[0] )
            traslShellValue.append( shellDefModel[1] )
            rotShellValue.append( shellDefModel[2] )
            extrudeShell = shellDefModel[3]
            ExtrudedView.append( extrudeShell )
            #doc.Objects.AddMesh( extrudeShell)
            
        elif nNode == 8:
            solidDefModel = defSolid( ele, pointWrapperDict, pointDispWrapperDict, scaleDef)
            SolidDefModel.append( solidDefModel[0] )
            #doc.Objects.AddMesh( solidDefModel[0] )
            traslSolidValue.append( solidDefModel[1] )
            ExtrudedView.append( solidDefModel[0] )
            
        elif  eleType == 'FourNodeTetrahedron' :
            #print(ele)
            solidDefModel = defTetraSolid( ele, pointWrapperDict, pointDispWrapperDict, scaleDef )
            SolidDefModel.append( solidDefModel[0] )
            traslSolidValue.append( solidDefModel[1] )
            ExtrudedView.append( solidDefModel[0] )

    # Max Beam #
    flattenTrasl = []
    for valuetrasl in traslBeamValue:
        for value in valuetrasl:
            flattenTrasl.append( value )

    TraslX = [row[0] for row in flattenTrasl ]
    TraslY = [row[1] for row in flattenTrasl ]
    TraslZ = [row[2] for row in flattenTrasl ]

    if len(TraslX) > 0:
        #              txMax          tyMax         tzMax
        tMax = [ max( max(rowDefX),max(TraslX)  ), max( max(rowDefY), max(TraslY) ), max( max(rowDefZ), max(TraslZ) ) ]
        #              txMin          tyMin         tzMin
        tMin = [ min( min(rowDefX), min(TraslX) ), min( min(rowDefY), min(TraslY) ), min( min(rowDefZ), min(TraslZ) ) ]
    else:
        #              txMax          tyMax         tzMax
        tMax = [  max(rowDefX)  , max(rowDefY), max(rowDefZ) ]
        #              txMin          tyMin         tzMin
        tMin = [  min(rowDefX), min(rowDefY),  min(rowDefZ)  ]

    i = direction 

    colorValor = []
    numberDivide = []
    for value in traslBeamValue :
        row = [row[i] for row in value ]
        numberDivide.append( len(row)  )
        for valor in row:
            color = gradientJet( valor, tMax[i], tMin[i] )
            colour = rs.CreateColor( color[0], color[1], color[2] )
            colorValor.append( colour )

    for shellEle, value in zip(ShellDefModel,traslShellValue) :
        shellColor = shellEle.DuplicateMesh()
        shellColor.VertexColors.Clear()
        for j in range(0,shellEle.Vertices.Count):
            jetColor = gradientJet(value[j][i], tMax[i], tMin[i])
            shellColor.VertexColors.Add( jetColor[0],jetColor[1],jetColor[2] )
        modelDisp.append( shellColor)
    #dup.VertexColors.CreateMonotoneMesh(Color.Red)
    #doc.Objects.AddMesh(dup)
    for solidEle, value in zip(SolidDefModel,traslSolidValue) :
        solidColor = solidEle.DuplicateMesh()
        solidColor.VertexColors.Clear()
        for j in range(0,solidEle.Vertices.Count):
            jetColor = gradientJet(value[j][i], tMax[i], tMin[i])
            solidColor.VertexColors.Add( jetColor[0],jetColor[1],jetColor[2] )
        modelDisp.append( solidColor)
            #rg.Collections.MeshVertexColorList.SetColor( solidEle,j, color[0], color[1], color[2] )


    if modelExstrud == False or modelExstrud == None:
        ModelDisp  = modelDisp
        ModelCurve = th.list_to_tree([ modelCurve ,numberDivide, colorValor ])
        max_min = th.list_to_tree([ tMax[i], tMin[i] ])
        
    else  :
        ModelDisp = ExtrudedView
        ModelCurve = None
        max_min = None

    return ModelDisp, ModelCurve, max_min

checkData = True

if not AlpacaStaticOutput:
    checkData = False
    msg = "input 'AlpacaStaticOutput' failed to collect data"  
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if direction is None:
    checkData = False
    msg = "input 'direction' failed to collect data"  
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if checkData != False:
    print( type(AlpacaStaticOutput), type(direction), type(scale), type( modelExstrud) )
    ModelDisp, ModelCurve, max_min = defModelView( AlpacaStaticOutput, direction , scale, modelExstrud  )

