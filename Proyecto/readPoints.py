import vtk

#Reading of Points
def readPoints(file):
	# Create an array of Points
	points = vtk.vtkPoints()
	while file:
		if file and file[0] !='#':
			x,y,z=float(file[0]), float(file[1]), float(file[2])
			points.InsertNextPoint(x, y, z)
			return points

def readVectors(file):
	vectors = vtk.vtkDoubleArray()
	vectors.SetNumberOfComponents(3)
	while file:
		if file and file[0] != '#':
			x, y, z = float(file[0]), float(file[1]), float(file[2])
			vectors.InsertNextTuple3(x, y, z)
			return vectors

def readScalars(file):
	scalars = vtk.vtkFloatArray()
	while file:
		if file and file[0] !='#':
			x, y=float(file[0]),float(file[1])
			z=x-y
			scalars.InsertNextValue(z)
			return scalars
