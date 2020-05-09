import sys
import openseespy.opensees as ops


#filename = sys.argv[1]
filename = r'C:\Users\FORMAT\Desktop\EarthQuakeTest\assembleData\openSeesModel.txt'
inputName = filename.split("\\")[-1]


with open(filename, 'r') as f:
    lines = f.readlines()
    openSeesNode = eval( lines[0].strip() )
    GeomTransf = eval( lines[1].strip() )
    openSeesBeam = eval( lines[2].strip() )
    openSeesSupport = eval( lines[3].strip() )
    openSeesNodeLoad = eval( lines[4].strip() )
    openSeesNodalMass = eval( lines[5].strip() )
    openSeesBeamLoad = eval( lines[6].strip() )
    openSeesMatTag = eval( lines[7].strip() )
    openSeesShell = eval(lines[8].strip() )
    openSeesSecTag = eval(lines[9].strip() )
    openSeesSolid = eval(lines[10].strip() )




oNodes = openSeesNode
gT = GeomTransf
openSeesBeam = openSeesBeam
oSupport = openSeesSupport
oNodeLoad = openSeesNodeLoad
oBeamLoad = openSeesBeamLoad
MatTag = openSeesMatTag
openSeesShell = openSeesShell
openSeesSecTag = openSeesSecTag
openSeesSolid = openSeesSolid
oMass = openSeesNodalMass



ops.wipe()

# MODEL
# ------------------------------

# Create ModelBuilder (with three-dimensions and 6 DOF/node):

ops.model('BasicBuilder', '-ndm', 3, '-ndf', 6)
#model('basic', '-ndm', ndm, '-ndf', ndf=ndm*(ndm+1)/2)

##INPUT VARIABLE IS NODES CORDINATES OF STRUCTUR IN GRASSHOPER ##

## CREATE NODES IN OPENSEES ##


for i in range(0,len(oNodes)):
    nodeTag = oNodes[i][0] + 1
    ops.node( nodeTag, oNodes[i][1], oNodes[i][2], oNodes[i][3] )

## CREATE MATERIAL IN OPENSEES ##

#print(MatTag) # to adjust

for item in MatTag:
    materialDimension = item[0].split("_")[1]
    materialType = item[0].split("_")[2]
    matTag = item[1][0]
    E = item[1][1][0]
    if materialDimension == 'uniaxialMaterial':
        ops.uniaxialMaterial(materialType, matTag , E)
    elif materialDimension == 'nDMaterial':
        ops.nDMaterial('ElasticIsotropic', matTag, E, 0.3)


for item in openSeesSecTag:
    typeSection = item[0].split("_")[1]
    secTag = int(item[1][0])
    E_mod = float( item[1][1][1][1] )
    nu = float( item[1][1][1][3] )
    h = float( item[1][1][0] )
    rho = float( item[1][1][1][4] )
    if typeSection == 'ElasticMembranePlateSection':
        ops.section(typeSection, secTag, E_mod, nu, h, rho)
        #print( 'ops.section( {0}, {1}, {2}, {3}, {4}, {5})'.format( typeSection, int(secTag), float(E_mod), float(nu), float(h), float(rho) ) )
## CREATE ELEMENT IN OPENSEES ##

# Define geometric transformation:
for i in range(0, len(gT)):
    tag = gT[i][0]
    vec = gT[i][1]
    ops.geomTransf('Linear', tag , *vec)


elementProperties = []

for n in range(0, len(openSeesBeam)):

    eleTag = openSeesBeam[n][1] + 1
    eleType = openSeesBeam[n][0]
    indexStart = openSeesBeam[n][2][0] + 1
    indexEnd = openSeesBeam[n][2][1] + 1
    eleNodes = [ indexStart, indexEnd]
    
    A = openSeesBeam[n][3]
    E = openSeesBeam[n][4]
    G = openSeesBeam[n][5]
    Jxx = openSeesBeam[n][6] 
    Iy = openSeesBeam[n][7] 
    Iz = openSeesBeam[n][8]
    Avz = openSeesBeam[n][11]
    Avy = openSeesBeam[n][12]
    geomTag = int(openSeesBeam[n][9])
    massDens = openSeesBeam[n][10]
    orientVector = openSeesBeam[n][13]
    sectionGeomProperties = openSeesBeam[n][14]     # it is a list with [shape, base, height]
    matTag = openSeesBeam[n][15]
    color = openSeesBeam[n][16]   

    elementProperties.append([ eleTag, [eleType, E, G, A, Avz, Avy, Jxx, Iy, Iz, orientVector, sectionGeomProperties, matTag, color] ])


    if eleType is 'Truss':

        ops.element( eleType , eleTag , *[indexStart, indexEnd], float(A), matTag ) # TO CONTROL!!!
        

    elif eleType is 'ElasticTimoshenkoBeam':

        ops.element( eleType , eleTag , indexStart, indexEnd, E, G, A, Jxx, Iy, Iz, Avy, Avz, geomTag , '-mass', massDens,'-lMass')

for item in openSeesShell:

    eleType = item[0]

    #print('eleType = ' + str(eleType))
    eleTag = item[1] + 1
    #print('eleTag = ' + str(eleTag))
    eleNodes = item[2]
    #print('eleNodes = ' + str(eleNodes))
    secTag = item[3]
    #print('secTag = ' + str(secTag))
    thick = item[4]
    #print('thick = ' + str(thick))
    color = item[5]

    elementProperties.append([ eleTag, [eleType, thick ,color] ])

    if (eleType == 'ShellDKGQ') or (eleType == 'ShellDKGT'):

        ops.element( eleType , eleTag, *eleNodes, secTag)

for item in openSeesSolid:

    eleType = item[0]
    #print('eleType = ' + str(eleType))
    eleTag = item[1] + 1
    #print('eleTag = ' + str(eleTag))
    eleNodes = item[2]
    #print('eleNodes = ' + str(eleNodes))
    matTag = item[3]
    #print('secTag = ' + str(secTag))
    force = item[4]
    #print( force)
    color = item[5]

    elementProperties.append([ eleTag, [eleType,color] ])

    if (eleType == 'bbarBrick') or (eleType == 'FourNodeTetrahedron'):

        ops.element( eleType , eleTag, *eleNodes, matTag, *force)                           
# transform elementproperties to  Dict to call the object by tag
elementPropertiesDict = dict(elementProperties)

# SUPPORT #

for i in range(0, len(oSupport)):
    indexSupport = oSupport[i][0] + 1

    ops.fix( indexSupport, oSupport[i][1], oSupport[i][2], oSupport[i][3], oSupport[i][4], oSupport[i][5], oSupport[i][6] )

## LOAD ##

# create TimeSeries
ops.timeSeries('Constant', 1)

# create a plain load pattern
ops.pattern('Plain', 1, 1)

## assemble load ##
for i in range(0, len(oNodeLoad)):

    nodetag = oNodeLoad[i][0] + 1
    Force = oNodeLoad[i][1]
    ops.load( nodetag, *Force )

elementLoad = []

for item in openSeesBeamLoad:
    eleTags = item[0] + 1
    Wy = item[1][0]
    Wz = item[1][1]
    Wx = item[1][2]
    loadType = item[2]
    #ops.eleLoad('-ele', eleTags,'-type', '-beamUniform', Wy, Wz, Wx) we need to understand why is wrong
    ops.eleLoad('-ele', eleTags,'-type', '-beamUniform', Wz, Wy, Wx)
    elementLoad.append([ eleTags, Wy, Wz, Wx, loadType] )

for i in range(len(oMass)):
    nodeTag = oMass[i][0] + 1
    massValues = oMass[i][1]
    ops.mass(nodeTag, *massValues)


# ------------------------------
# Start of analysis generation
# ------------------------------

ops.system("BandSPD")

ops.numberer('Plain')

# create constraint handler
ops.constraints("Transformation") # to allow Diaphgram constrain

# create integrator
ops.integrator("LoadControl",  0.1 )

# create algorithm
ops.algorithm("Newton")

# create analysis object
ops.analysis("Static")

# perform the analysis
ops.analyze(10)

print("Static Analyses Complete")
print(ops.nodeDisp(3,2))

## OUTPUT FILE ##


import ReadRecord


# Set the gravity loads to be constant & reset the time in the domain
ops.loadConst('-time', 0.0)


# Set some parameters
record = 'elCentro'

# Permform the conversion from SMD record to OpenSees record
dt, nPts = ReadRecord.ReadRecord(record+'.at2', record+'.dat')

# Set time series to be passed to uniform excitation
ops.timeSeries('Trig', 2, 0, 5, 0.5, '-factor', 0.000000000001)

#ops.timeSeries('Path', 2, '-filePath', record+'.dat', '-dt', dt, '-factor', 0.000000000001)

# Create UniformExcitation load pattern
#                               tag    dir          tag timeSeries
ops.pattern('UniformExcitation',  2,   1,  '-accel', 2)

# set the rayleigh damping factors for nodes & elements
ops.rayleigh(0.0, 0.0, 0.0, 0.625)



# Delete the old analysis and all it's component objects
ops.wipeAnalysis()

# Create the system of equation, a banded general storage scheme
ops.system('BandGeneral')

# Create the constraint handler, a plain handler as homogeneous boundary
ops.constraints('Plain')

# Create the convergence test, the norm of the residual with a tolerance of 
# 1e-12 and a max number of iterations of 10
ops.test('NormDispIncr', 1.0e-15,  100 )
#ops.test('FixedNumIter', 500)

# Create the solution algorithm, a Newton-Raphson algorithm
ops.algorithm('Newton')

# Create the DOF numberer, the reverse Cuthill-McKee algorithm
ops.numberer('RCM')

# Create the integration scheme, the Newmark with alpha =0.5 and beta =.25
ops.integrator('Newmark',  0.5,  0.25 )

# Create the analysis object
ops.analysis('Transient')

# is it necessary to perform an Eigen?

# Perform an eigenvalue analysis
numEigen = 5
eigenValues = ops.eigen(numEigen)
print("eigen values at start of transient:",eigenValues)

# set some variables


tFinal = 3                # value from components
#tFinal = nPts*dt                # value from components
tCurrent = ops.getTime()
ok = 0

time = [tCurrent]
u3 = [0.0]

# Perform the transient analysis
while ok == 0 and tCurrent < tFinal:
    print(ops.nodeDisp(3,2))
    
    ok = ops.analyze(1, .005)

# if the analysis fails try initial tangent iteration
    if ok != 0:
        print("regular newton failed .. lets try an initial stiffness for this step")
        ops.test('NormDispIncr', 1.0e-12,  1000, 0)
        ops.algorithm('ModifiedNewton', '-initial')
        ok = ops.analyze( 1, .01)
        if ok == 0:
            print("that worked .. back to regular newton")
        ops.test('NormDispIncr', 1.0e-12,  1000 )
        ops.algorithm('Newton')

    tCurrent = ops.getTime()
    print(f"current time is {tCurrent}")



print("I finished")





'''

## DISPLACEMENT
nodeDisplacementWrapper = []

for i in range(1,len(ops.getNodeTags())+1):

    nodeTag = i
    Node = ops.nodeCoord( nodeTag ) # cordinate nodo
    NodeDisp = ops.nodeDisp( nodeTag ) # spostamenti e rotazioni del nodo 
    nodeDisplacementWrapper.append([Node, NodeDisp])

#-----------------------------------------------------

reactionWrapper = []
ops.reactions()
for i in range(0, len(oSupport)):
    indexSupport = oSupport[i][0] + 1
    ghTag = oSupport[i][0]
    reactionWrapper.append([ghTag, ops.nodeReaction(indexSupport)])

reactionWrapper = reactionWrapper


#-----------------------------------------------------
elementOutputWrapper = []
eleForceOutputWrapper = []



elementTagList = ops.getEleTags()

for elementTag in elementTagList:
    elementOutputWrapper.append([ elementTag, ops.eleNodes(elementTag), elementPropertiesDict.setdefault(elementTag) ])
    eleForceOutputWrapper.append([ elementTag, ops.eleForce(elementTag) ])
 # need to find a new way to add elementProperties


openSeesOutputWrapper = ([nodeDisplacementWrapper,
                        reactionWrapper,
                        elementOutputWrapper,
                        elementLoad,
                        eleForceOutputWrapper])


length = len(filename)-len(inputName)
filefolder = filename[0:length]
outputFileName = filefolder+'openSeesOutputWrapper.txt'

with open(outputFileName, 'w') as f:
    for item in openSeesOutputWrapper:
        f.write("%s\n" % item)

'''