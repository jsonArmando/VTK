import vtk
import pandas as pd


url = 'https://github.com/plotly/datasets/blob/master/api_docs/3d_line_sample_data.csv?raw=true'
df = pd.read_csv(url,index_col=0)

def readPoints():
	file=(df[['x1','y1','z1']])
	for i in file.index:
		line=(df["x1"][i],df["y1"][i],df["z1"][i])
		points = vtk.vtkPoints()
		x, y, z = float(line[0]), float(line[1]), float(line[2])
		points.InsertNextPoint(x, y, z)
	return points