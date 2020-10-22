import servidor as sv
import readPoints as rd
import sys
from vtk import *

data_harvest=sv.openWeather()
cursor=sv.conexion(data_harvest)

cont=0
for record in cursor:
    file=[]
    file.insert(0,record['temp'])
    file.insert(1,record['pressure'])
    file.insert(2,record['humidity'])
    file.insert(3,record['speed'])
    cont+=1

#data=vtkUnstructuredGrid()
#data.SetPoints(rd.readPoints(file))
#data.GetPointData().SetVectors(rd.readVectors(file))

point = vtkPolyData()
point.SetPoints(rd.readPoints(file))

ball = vtkSphereSource()
ball.SetRadius(0.05)
ball.SetThetaResolution(12)
ball.SetPhiResolution(12)

ballGlyph = vtkGlyph3D()
ballGlyph.SetSourceData(point) 
ballGlyph.SetSourceConnection(ball.GetOutputPort())