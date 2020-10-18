#include "vtkPNGReader.h"
#include "vtkImageDataGeometryFilter.h"
#include "vtkRenderWindowInteractor.h"
#include <vtkSmartPointer.h>
#include <vtkRenderWindow.h>
#include "vtkLookupTable.h"
#include "vtkRenderer.h"
#include "vtkPolyDataMapper.h"
#include "vtkWarpScalar.h"
#include "vtkPolyDataNormals.h"
#include "vtkUnsignedCharArray.h"
#include "vtkScalarBarActor.h"
#include "vtkPolyData.h"
#include <vtkImageData.h>
#include <vtkElevationFilter.h>

int main() {
	//reader
	vtkSmartPointer<vtkPNGReader> reader =
  vtkSmartPointer<vtkPNGReader>::New();
  reader->SetFileName("Untitled.png");

	vtkSmartPointer<vtkImageDataGeometryFilter> imageDataGeometryFilter =
  vtkSmartPointer<vtkImageDataGeometryFilter>::New();
  imageDataGeometryFilter->SetInputConnection(reader->GetOutputPort());
	// Create the color map
  vtkSmartPointer<vtkLookupTable> lut =
	vtkSmartPointer<vtkLookupTable>::New();
	lut->SetHueRange(0.7,0);
	lut->SetSaturationRange(1.0,0);
	lut->SetValueRange(0.5,1.0);
  lut->Build();
	//Create Scalar
	vtkSmartPointer<vtkWarpScalar> warpScalar =
	vtkSmartPointer<vtkWarpScalar>::New();
	warpScalar->SetInputConnection(imageDataGeometryFilter->GetOutputPort());
	warpScalar->SetScaleFactor(1.0);
	warpScalar->UseNormalOn();
	warpScalar->SetNormal(0, 0, 0.01);
	warpScalar->Update();

	vtkSmartPointer<vtkElevationFilter> elevationFilter=
	vtkSmartPointer<vtkElevationFilter> ::New();
	elevationFilter->SetInputConnection(warpScalar->GetOutputPort());
	elevationFilter->SetLowPoint(0.0, 0.0, 0.0);
  elevationFilter->SetHighPoint(0.0, 0.0, 1000);
	elevationFilter->SetScalarRange(0,1000);
	elevationFilter->Update();
	//Create a mapper
	vtkSmartPointer<vtkPolyDataMapper> mapper =
	vtkSmartPointer<vtkPolyDataMapper>::New();
	mapper->SetInputConnection(elevationFilter->GetOutputPort());
	mapper->SetScalarRange(0,1000);
  mapper->SetLookupTable(lut);

	vtkSmartPointer<vtkScalarBarActor> scalarBar =
	vtkSmartPointer<vtkScalarBarActor>::New();
	scalarBar->SetLookupTable(mapper->GetLookupTable());
	scalarBar->SetMaximumWidthInPixels(60);
	scalarBar->SetHeight(0.8);
	//scalarBar->SetTitle("Temperature");
	//Create Actor
  vtkSmartPointer<vtkActor> actor =
  vtkSmartPointer<vtkActor>::New();
  actor->SetMapper(mapper);
	scalarBar->SetLookupTable(lut);
  // Visualization
  vtkSmartPointer<vtkRenderer> renderer =
  vtkSmartPointer<vtkRenderer>::New();
  vtkSmartPointer<vtkRenderWindow> renderWindow =
  vtkSmartPointer<vtkRenderWindow>::New();
  renderWindow->AddRenderer(renderer);
  vtkSmartPointer<vtkRenderWindowInteractor> renderWindowInteractor =
  vtkSmartPointer<vtkRenderWindowInteractor>::New();
  renderWindowInteractor->SetRenderWindow(renderWindow);
  renderer->AddActor(actor);
	renderer->AddActor2D(scalarBar);
	renderer->GradientBackgroundOn();
	//renderer->SetBackground(0.0, 0.0, 0.0);
	//renderer->SetBackground(1.0, 1.0, 1.0);
  renderWindow->Render();
  renderWindowInteractor->Start();
}
