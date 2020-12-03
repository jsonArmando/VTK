#!/usr/bin/env python
from vtk import *
import random
import numpy
import treeCone as tc
import dataStructTransfer as ds
import time
import threading

def sliderMapElevation():
    slideBar = vtkSliderRepresentation2D()
    slideBar.SetMinimumValue(-5.0)
    slideBar.SetMaximumValue(45.0)

    slideBar.GetSliderProperty().SetColor(2,0,0)
    slideBar.GetTitleProperty().SetColor(2,0,0)
    slideBar.GetLabelProperty().SetColor(2,0,0)
    slideBar.GetSelectedProperty().SetColor(2,0,0)
    slideBar.GetTubeProperty().SetColor(0,2,0)
    slideBar.GetCapProperty().SetColor(2,2,0)

    slideBar.GetPoint1Coordinate().SetCoordinateSystemToDisplay()
    slideBar.GetPoint1Coordinate().SetValue(40,40)

    slideBar.GetPoint2Coordinate().SetCoordinateSystemToDisplay()
    slideBar.GetPoint2Coordinate().SetValue(350,40)
    return slideBar

def myCallback(obj,event):
        value = int (obj.GetRepresentation().GetValue())
        return values

value = int(input('Ingrese un valor de Transferencia: '))
class mainElevation(value):
    iren = vtkRenderWindowInteractor()
    NPts = 1000

    math = vtkMath()
    hMap=vtkPNGReader()
    hMap.SetFileName("image/Noruega Height Map (SRTM30 Plus).png")

    colors = vtkNamedColors()
    '''
    listCylinder = ds.functionTransfer()
    for i in listCylinder:
        listCylinder[0]
        print(listCylinder[0])'''


    lut=vtkLookupTable()
    if(value<30):
        lut.SetHueRange(1.0/3.0, 1.0/3.0)
        lut.SetSaturationRange(1.0, 1.0)
        lut.SetValueRange(0.0, 1.0)
        lut.SetAlphaRange(1.0, 1.0)
        lut.SetRampToLinear()
        lut.SetNumberOfTableValues(256)
        lut.Build()
    elif(25<value<=31):
        lut.SetHueRange(0.667,0)
        lut.SetSaturationRange(1.0,0)
        lut.SetValueRange(0.5,1.0)
        lut.SetAlphaRange(1.0, 1.0)
        lut.Build()
    else:
        lut.SetHueRange(0.1, 0.1)
        lut.SetSaturationRange(1.0, 1.0)
        lut.SetValueRange(0.0, 1.0)
        lut.SetAlphaRange(1.0, 1.0)
        lut.SetRampToLinear()
        lut.SetNumberOfTableValues(256)
        lut.Build();

    scalarBar = vtkScalarBarActor()
    # This LUT puts the lowest value at the top of the scalar bar.
    # scalarBar.SetLookupTable(lut);
    # Use this LUT if you want the highest value at the top.
    scalarBar.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport();
    scalarBar.GetPositionCoordinate().SetValue(0.1, 0.01);
    scalarBar.SetOrientationToHorizontal();
    scalarBar.SetWidth(0.8);
    scalarBar.SetHeight(0.12);   
    scalarBar.SetLookupTable(lut)
    scalarBar.SetTitle('Módulo de Deforestación en VTK y Python')
  


    lo = hMap.GetOutput().GetScalarRange()[0]
    hi = hMap.GetOutput().GetScalarRange()[1]

    geom = vtkImageDataGeometryFilter()
    geom.SetInputConnection(hMap.GetOutputPort())

    warp = vtkWarpScalar()
    warp.SetInputConnection(geom.GetOutputPort())
    warp.SetNormal(0, 0, 1.0)
    warp.UseNormalOn()
    warp.SetScaleFactor(0.01)
    warp.Update()

    bds = warp.GetOutput().GetBounds()
    center = warp.GetOutput().GetCenter()

    points = vtkPoints()
    points.SetDataTypeToFloat()
    points.SetNumberOfPoints(NPts)

    for i in range(0,NPts):
        points.SetPoint(i,math.Random(bds[0],bds[1]),math.Random(bds[2],bds[3]),0)

    source = vtkPolyData()
    source.SetPoints(points)

    points = vtkPoints() 
    sphere = vtkSphere()
    sphere.SetCenter(center[0],center[1]-7500,center[2])

    attr = vtkSampleImplicitFunctionFilter()
    attr.SetInputData(source)
    attr.SetImplicitFunction(sphere)
    attr.Update()

    # Gaussian kernel-------------------------------------------------------
    gaussianKernel = vtkGaussianKernel()
    gaussianKernel.SetSharpness(4)
    gaussianKernel.SetRadius(50)

    voronoiKernel = vtkVoronoiKernel()

    interpolator1 = vtkPointInterpolator2D()
    interpolator1.SetInputConnection(warp.GetOutputPort())
    interpolator1.SetSourceConnection(attr.GetOutputPort())
    interpolator1.SetKernel(voronoiKernel)
    interpolator1.SetNullPointsStrategyToClosestPoint()

    # Time execution
    timer = vtkTimerLog()
    timer.StartTimer()
    interpolator1.Update()
    timer.StopTimer()
    time = timer.GetElapsedTime()
    print("Interpolate Terrain Points (Gaussian): {0}".format(time))

    scalarRange = attr.GetOutput().GetScalarRange()

    srcMapper = vtkPolyDataMapper()
    srcMapper.SetLookupTable(lut)
    srcMapper.SetScalarModeToUseCellData()

    srcActor = vtkActor()
    srcActor.SetMapper(srcMapper)
    srcActor.RotateX(-45)
    srcActor.RotateZ(45)

    intMapper1 = vtkPolyDataMapper()
    intMapper1.SetInputConnection(interpolator1.GetOutputPort())
    intMapper1.SetScalarRange(scalarRange)
    intMapper1.SetLookupTable(lut)
    
    intActor1 = vtkActor()
    intActor1.SetMapper(intMapper1)

    outline1 = vtkOutlineFilter()
    outline1.SetInputConnection(warp.GetOutputPort())

    outlineMapper1 = vtkPolyDataMapper()
    outlineMapper1.SetInputConnection(outline1.GetOutputPort())
    outlineMapper1.SetLookupTable(lut)

    outlineActor1 = vtkActor()
    outlineActor1.SetMapper(outlineMapper1)

    outlineActor2 = vtkActor()
    outlineActor2.SetMapper(ds.pointsElevation('data/points.txt'))

    outlineActor3 = vtkActor()
    outlineActor3.SetMapper(ds.pointsElevation('data/pointsShere.txt'))

    #Tree form Cylinder
    glyphMapper = vtkPolyDataMapper()

    tupleTreeCylinder=tc.treeCylinder(ds.pointsUbication('data/points.txt'),value)
    glyphMapper.SetInputConnection(tupleTreeCylinder.GetOutputPort())
    glyphMapper.SetScalarModeToUsePointFieldData()
    glyphMapper.SetColorModeToMapScalars()
    glyphMapper.ScalarVisibilityOn()
    glyphMapper.SelectColorArray('Elevation')
    glyphMapper.SetScalarRange(scalarRange)

    glyphActor = vtkActor()
    glyphActor.SetMapper(glyphMapper)
    glyphActor.GetProperty().SetColor(colors.GetColor3d("Brown"))

     #Tree form Cylinder
    glyphMapper1 = vtkPolyDataMapper()
    tupleTreeCylinder1=tc.treeCylinder(ds.pointsUbication('data/pointsShere.txt'),value)
    glyphMapper1.SetInputConnection(tupleTreeCylinder1.GetOutputPort())
    glyphMapper1.SetScalarModeToUsePointFieldData()
    glyphMapper1.SetColorModeToMapScalars()
    glyphMapper1.ScalarVisibilityOn()
    glyphMapper.SelectColorArray('Elevation')
    glyphMapper1.SetScalarRange(scalarRange)

    glyphActor1 = vtkActor()
    glyphActor1.SetMapper(glyphMapper1)
    glyphActor1.GetProperty().SetColor(colors.GetColor3d("Brown"))

    #Tree from Cone
    glyphMapperCone = vtkPolyDataMapper()

    #listCylinder = dt.functionTransfer()
    #for i in listCylinder:
    
    tupleTreeCone=tc.treeCone(ds.pointsUbication('data/points.txt'),value)
    glyphMapperCone.SetInputConnection(tupleTreeCone.GetOutputPort())
    glyphMapperCone.SetScalarModeToUsePointFieldData()
    glyphMapperCone.SetColorModeToMapScalars()
    glyphMapperCone.ScalarVisibilityOn()
    glyphMapperCone.SelectColorArray('Elevation')
    glyphMapperCone.SetScalarRange(scalarRange)

    glyphActorCone = vtkActor()
    glyphActorCone.SetMapper(glyphMapperCone)
    glyphActorCone.GetProperty().SetColor(colors.GetColor3d("DarkGreen"))

    #Tree Shere
    tupleTreeShere=tc.treeShere(ds.pointsUbication('data/pointsShere.txt'),value)
    glyphMapperShere = vtkPolyDataMapper()
    
    glyphMapperShere.SetInputConnection(tupleTreeShere.GetOutputPort())
    glyphMapperShere.SetScalarModeToUsePointFieldData()
    glyphMapperShere.SetColorModeToMapScalars()
    glyphMapperShere.ScalarVisibilityOn()
    glyphMapperShere.SelectColorArray('Elevation')
    glyphMapperShere.SetScalarRange(scalarRange)

    glyphActorShere = vtkActor()
    glyphActorShere.SetMapper(glyphMapperShere)
    glyphActorShere.GetProperty().SetColor(colors.GetColor3d("DarkGreen"))

    ren0 = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren0)
    iren.SetRenderWindow(renWin)
    ren0.AddViewProp(outlineActor1)

    threadLock = threading.Lock()

    def update_visualisation(self, obj = None, event = None):
        time.sleep(0.01)
        #threadLock.acquire()
        listCylinder = ds.functionTransfer()
        #threadLock.release()

    #sliderWidget = vtkSliderWidget()
    #sliderWidget.SetInteractor(iren)
    #sliderWidget.SetRepresentation(sliderMapElevation())
    #sliderWidget.EnabledOn()

    #sliderWidget.AddObserver("InteractionEvent",myCallback)
    ren0.AddViewProp(intActor1)
    ren0.AddViewProp(outlineActor1)
    ren0.AddViewProp(outlineActor2)
    ren0.AddViewProp(outlineActor3)
    ren0.AddViewProp(glyphActor)
    ren0.AddViewProp(glyphActor1)
    ren0.AddViewProp(glyphActorCone)
    ren0.AddViewProp(glyphActorShere)
    ren0.AddActor2D(scalarBar)
    ren0.SetBackground(.1, .2, .3)
    ren0.SetBackground(0.2, 0.4, 0.8)

    renWin.SetSize(1600, 800)
    cam = ren0.GetActiveCamera()
    cam.SetFocalPoint(center)

    fp = cam.GetFocalPoint()
    cam.SetPosition(fp[0]+.2,fp[1]+.1,fp[2]+1)
    ren0.ResetCamera()

    iren.Initialize()
    renWin.Render()
    iren.Start()

    iren.AddObserver("TimerEvent", update_visualisation)
    dt = 30  # ms
    timer_id = iren.CreateRepeatingTimer(dt)


mainElevation(value)