#!/usr/bin/env python
import dataStructTransfer as dt
import sys
from vtk import *

def treeCylinder(points,value):
	#Cilindro
	cylinderSource = vtkCylinderSource()
	cylinderSource.SetRadius(0.06)
	#listCylinder = dt.functionTransfer()
	#for i in listCylinder:
	if(value<30):
		cylinderSource.SetHeight(0.775)
		cylinderSource.SetCenter(0.0, 0.4, 0.0)
	else:
		cylinderSource.SetHeight(0.20)
		cylinderSource.SetCenter(0.0, 0.0, 0.0)
	cylinderSource.SetResolution(100)
	cylinderSource.CappingOn()
	

	tt = vtkTransform()
	tt.RotateWXYZ(90,360,1,0)
	tf = vtkTransformPolyDataFilter()
	tf.SetInputConnection(cylinderSource.GetOutputPort())
	tf.SetTransform(tt)
	tf.Update()

	cylinderGlyph = vtkGlyph3D()
	cylinderGlyph.SetInputData(points)
	cylinderGlyph.SetSourceConnection(tf.GetOutputPort())
	cylinderGlyph.SetScaleFactor(8.1)

	return cylinderGlyph


def treeCone(points,value):
	#Cono
	coneSource = vtkConeSource()
	coneSource.SetResolution(10)
	coneSource.SetRadius(5.025)
	coneSource.SetHeight(12.09)
	coneSource.SetCenter(11.0, 0.0, 0.0)

	tt = vtkTransform()
	tt.RotateWXYZ(90,0,-360,0)
	tf = vtkTransformPolyDataFilter()
	tf.SetInputConnection(coneSource.GetOutputPort())
	tf.SetTransform(tt)
	tf.Update()

	coneGlyph = vtkGlyph3D()
	coneGlyph.SetInputData(points)
	if(value<30):
		coneGlyph.SetSourceConnection(tf.GetOutputPort())
	return coneGlyph

def treeShere(points,value):
	ball = vtkSphereSource()
	ball.SetRadius(4.045)
	ball.SetThetaResolution(8)
	ball.SetPhiResolution(8)
	ball.SetCenter(0.0, 0.0, 10.0)

	ballGlyph = vtkGlyph3D()
	ballGlyph.SetInputData(points)
	if(value<25):
		ballGlyph.SetSourceConnection(ball.GetOutputPort())
	return ballGlyph

def pasarValor(value):
	return value
