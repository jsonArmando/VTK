#!/usr/bin/env python
import servidor as sv
import readPoints as rd
import sys
from vtk import *

data_harvest=sv.openWeather()
cursor=sv.conexion(data_harvest)
dataStruct=vtkUnstructuredGrid()
def dataStructTransfer():
	cont=0
	for record in data_harvest:
	    file=[]
	    file.insert(0,data_harvest['temp'])
	    file.insert(1,data_harvest['pressure'])
	    file.insert(2,data_harvest['humidity'])
	    file.insert(3,data_harvest['speed'])
	    dataStruct.SetPoints(rd.readPoints(file))
	    dataStruct.GetPointData().SetVectors(rd.readVectors(file))
	    cont+=1
	    return dataStruct

def functionTransfer():
	for record in data_harvest:
	    file=[]
	    file.insert(0,data_harvest['temp'])
	    file.insert(1,data_harvest['pressure'])
	    file.insert(2,data_harvest['humidity'])
	    file.insert(3,data_harvest['speed'])
	return file

def pointsUbication(points):
    points_reader = vtkDelimitedTextReader()
    points_reader.SetFileName(points)
    points_reader.DetectNumericColumnsOn()
    points_reader.SetFieldDelimiterCharacters('\t')
    points_reader.SetHaveHeaders(True)

    table_points = vtkTableToPolyData()
    table_points.SetInputConnection(points_reader.GetOutputPort())
    table_points.SetXColumn('x')
    table_points.SetYColumn('y')
    table_points.SetZColumn('z')
    table_points.Update()

    points = table_points.GetOutput()
    points.GetPointData().SetActiveScalars('val')
    range = points.GetPointData().GetScalars().GetRange()
    return points

def pointsElevation(pointCone):
    points_reader = vtkDelimitedTextReader()
    points_reader.SetFileName(pointCone)
    points_reader.DetectNumericColumnsOn()
    points_reader.SetFieldDelimiterCharacters('\t')
    points_reader.SetHaveHeaders(True)

    table_points = vtkTableToPolyData()
    table_points.SetInputConnection(points_reader.GetOutputPort())
    table_points.SetXColumn('x')
    table_points.SetYColumn('y')
    table_points.SetZColumn('z')
    table_points.Update()

    points = table_points.GetOutput()
    points.GetPointData().SetActiveScalars('val')
    range = points.GetPointData().GetScalars().GetRange()

    point_mapper = vtkPointGaussianMapper()
    point_mapper.SetInputData(points)
    point_mapper.SetScalarRange(range)
    point_mapper.SetScaleFactor(0.5)
    point_mapper.EmissiveOff();
    point_mapper.SetSplatShaderCode(
        "//VTK::Color::Impl\n"
        "float dist = dot(offsetVCVSOutput.xy,offsetVCVSOutput.xy);\n"
        "if (dist > 1.0) {\n"
        "  discard;\n"
        "} else {\n"
        "  float scale = (1.0 - dist);\n"
        "  ambientColor *= scale;\n"
        "  diffuseColor *= scale;\n"
        "}\n"
    )

    return point_mapper