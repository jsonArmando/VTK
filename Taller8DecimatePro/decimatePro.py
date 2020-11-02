import vtk
from vtk.util.misc import vtkGetDataRoot

fran = vtk.vtkPolyDataReader()
fran.SetFileName("Data/fran_cut.vtk")

colors = vtk.vtkNamedColors()
backFaceColor = colors.GetColor3d("gold")
inputActorColor = colors.GetColor3d("flesh")
decimatedActorColor = colors.GetColor3d("flesh")
colors.SetColor('leftBkg', [0.6, 0.5, 0.4, 1.0])
colors.SetColor('rightBkg', [0.4, 0.5, 0.6, 1.0])

tri =vtk.vtkTriangleFilter()
tri.SetInputData(fran.GetOutput())

deci = vtk.vtkDecimatePro()
deci.SetInputConnection(fran.GetOutputPort())
deci.SetTargetReduction(0.9)
deci.PreserveTopologyOn()

leftViewport = [0.0, 0.0, 0.5, 1.0]
rightViewport = [0.5, 0.0, 1.0, 1.0]

decimate = vtk.vtkQuadricClustering()
decimate.SetNumberOfXDivisions(32)
decimate.SetNumberOfYDivisions(32)
decimate.SetNumberOfZDivisions(32)
decimate.SetInputData(tri.GetOutput())

decimatePD =vtk.vtkPolyData()
decimatePD.ShallowCopy(decimate.GetOutput())

smoother = vtk.vtkSmoothPolyDataFilter()
smoother.SetInputConnection(deci.GetOutputPort())
smoother.SetNumberOfIterations(50)

normals = vtk.vtkPolyDataNormals()
normals.SetInputConnection(smoother.GetOutputPort())
normals.FlipNormalsOn()

franMapper = vtk.vtkPolyDataMapper()
franMapper.SetInputConnection(normals.GetOutputPort())

franMapper1 = vtk.vtkPolyDataMapper()
franMapper1.SetInputData(decimatePD)

franActor = vtk.vtkActor()
franActor.SetMapper(franMapper)
franActor.GetProperty().SetColor(0.0, 0.49, 0.25)

franActor1 = vtk.vtkActor()
franActor1.SetMapper(franMapper1)
franActor1.GetProperty().SetColor(1.0, 0.49, 0.25)

renderWindow = vtk.vtkRenderWindow()
renderWindow.SetSize(600, 300)

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderWindow)

leftRenderer = vtk.vtkRenderer()
renderWindow.AddRenderer(leftRenderer)
leftRenderer.SetViewport(leftViewport)
leftRenderer.SetBackground((colors.GetColor3d('leftBkg')))

rightRenderer = vtk.vtkRenderer()
renderWindow.AddRenderer(rightRenderer)
rightRenderer.SetViewport(rightViewport)
rightRenderer.SetBackground((colors.GetColor3d('rightBkg')))

leftRenderer.AddActor(franActor)
rightRenderer.AddActor(franActor1)

camera = vtk.vtkCamera()
camera.SetPosition (0, -1, 0)
camera.SetFocalPoint (0, 0, 0)
camera.SetViewUp (0, 0, 1)
camera.Elevation(30)
camera.Azimuth(30)

leftRenderer.SetActiveCamera(camera)
rightRenderer.SetActiveCamera(camera)

leftRenderer.ResetCamera()
leftRenderer.ResetCameraClippingRange()

renderWindow.Render()
renderWindow.SetWindowName('Decimation')
interactor.Start()