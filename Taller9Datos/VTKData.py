import sys
import random
from vtk import *
import point as pt

data=vtkUnstructuredGrid()
pointsVTK=(pt.readPoints())
data.SetPoints(pointsVTK)

ball = vtkSphereSource()
ball.SetRadius(0.05)
ball.SetThetaResolution(12)
ball.SetPhiResolution(12)

ballGlyph = vtkGlyph3D()
ballGlyph.SetInputData(data)
ballGlyph.SetSourceConnection(ball.GetOutputPort())

ballMapper = vtkPolyDataMapper()
ballMapper.SetInputConnection(ballGlyph.GetOutputPort())

ballActor = vtkActor()
ballActor.SetMapper(ballMapper)
ballActor.GetProperty().SetColor(0.8,0.4,0.4)

arrow = vtkArrowSource()
arrow.SetTipRadius(0.2)
arrow.SetShaftRadius(0.075)

arrowGlyph = vtkGlyph3D()
arrowGlyph.SetInputData(data)
arrowGlyph.SetSourceConnection(arrow.GetOutputPort())
arrowGlyph.SetScaleFactor(0.2)

#CONVEX HULL

hull  = vtkHull()
hull.SetInputConnection(ballGlyph.GetOutputPort());
hull.AddCubeFacePlanes ();
hull.AddRecursiveSpherePlanes(5);

arrowMapper = vtkPolyDataMapper()
arrowMapper.SetInputConnection(arrowGlyph.GetOutputPort())

arrowActor = vtkActor()
arrowActor.SetMapper(arrowMapper)
arrowActor.GetProperty().SetColor(0.9,0.9,0.1)

arrowMapper1 = vtkPolyDataMapper()
arrowMapper1.SetInputConnection(hull.GetOutputPort())

arrowActor1 = vtkActor()
arrowActor1.SetMapper(arrowMapper1)
arrowActor1.GetProperty().SetColor(0.9,0.9,0.1)


#DELAUNY TRIANGULACIÒN
points = vtkPoints()
for x in range(10):
    for y in range(10):
        points.InsertNextPoint(x + random.uniform(-.25, .25), 
                               y + random.uniform(-.25, .25), 0)
 
aPolyData = vtkPolyData()
aPolyData.SetPoints(points)
 
aCellArray = vtkCellArray()
 
boundary = vtkPolyData()
boundary.SetPoints(aPolyData.GetPoints())
boundary.SetPolys(aCellArray)
delaunay = vtkDelaunay2D()
if VTK_MAJOR_VERSION <= 5:
    delaunay.SetInput(aPolyData.GetOutput())
    delaunay.SetSource(boundary)
else:
    delaunay.SetInputData(aPolyData)
    delaunay.SetSourceData(boundary)

delaunay.Update()
 
meshMapper = vtkPolyDataMapper()
meshMapper.SetInputConnection(delaunay.GetOutputPort())
 
meshActor = vtkActor()
meshActor.SetMapper(meshMapper)
meshActor.GetProperty().SetEdgeColor(0, 0, 1)
meshActor.GetProperty().SetInterpolationToFlat()
meshActor.GetProperty().SetRepresentationToWireframe()
 
boundaryMapper = vtkPolyDataMapper()
if VTK_MAJOR_VERSION <= 5:
    boundaryMapper.SetInputConnection(boundary.GetProducerPort())
else:
    boundaryMapper.SetInputData(boundary)

boundaryActor = vtkActor()
boundaryActor.SetMapper(boundaryMapper)
boundaryActor.GetProperty().SetColor(1, 0, 0)

#Find the minimal spanning tree
#COLOUR
colors = vtkNamedColors()
colors.SetColor('leftBkg', [0.6, 0.5, 0.4, 1.0])
colors.SetColor('centreBkg', [0.3, 0.1, 0.4, 1.0])
colors.SetColor('rightBkg', [0.4, 0.5, 0.6, 1.0])
colors.SetColor('downtBkg', [0.1, 0.1, 0.1, 1.0])

leftViewport = [0.0, 0.0, 0.5, 1.0]
centerViewport = [0.25, 0.0, .66, 1.0]
rightViewport = [0.50, 0.0, 1.0, 1.0]
downViewport = [0.75, 0.0, 1.0, 1.0]

camera = vtkCamera()

renderWindow = vtkRenderWindow()
renderWindow.SetSize(1200, 400)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderWindow)

leftRenderer = vtkRenderer()
renderWindow.AddRenderer(leftRenderer)
leftRenderer.SetViewport(leftViewport)
leftRenderer.SetBackground(colors.GetColor3d('leftBkg'))
#leftRenderer.SetActiveCamera(camera)

centerRenderer = vtkRenderer()
renderWindow.AddRenderer(centerRenderer)
centerRenderer.SetViewport(centerViewport)
centerRenderer.SetBackground(colors.GetColor3d('centreBkg'))
#centerRenderer.SetActiveCamera(camera)

rightRenderer = vtkRenderer()
renderWindow.AddRenderer(rightRenderer)
rightRenderer.SetViewport(rightViewport)
rightRenderer.SetBackground(colors.GetColor3d('rightBkg'))
#rightRenderer.SetActiveCamera(camera)

downRenderer = vtkRenderer()
renderWindow.AddRenderer(downRenderer)
downRenderer.SetViewport(downViewport)
downRenderer.SetBackground(colors.GetColor3d('downtBkg'))
#downRenderer.SetActiveCamera(camera)

centerRenderer.AddActor(arrowActor1)
leftRenderer.AddActor(ballActor)
leftRenderer.AddActor(arrowActor)
rightRenderer.AddActor(meshActor)
rightRenderer.AddActor(boundaryActor)
#downRenderer.AddActor(ballActor)
leftRenderer.ResetCamera()

renderWindow.Render()
interactor.Start()