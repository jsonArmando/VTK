#include <vtkSmartPointer.h>
#include <vtkPNGReader.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkRenderer.h>
#include <vtkPolyDataMapper.h>
#include <vtkArrowSource.h>
#include <vtkImageShiftScale.h>
#include <vtkGlyph3D.h>
#include <vtkCamera.h>
#include <vtkScalarsToColors.h>
#include <vtkLookupTable.h>


using namespace std;

int main(int argc, char* argv[])
{
  vtkSmartPointer<vtkPNGReader> readerOne=vtkSmartPointer<vtkPNGReader>::New();
  readerOne->SetFileName("images/density_bigxy_0110.png");
  readerOne->Update();
  
  vtkSmartPointer<vtkPNGReader> readerTwo=vtkSmartPointer<vtkPNGReader>::New();
  readerTwo->SetFileName("images/density_bigxy_0170.png");
  readerTwo->Update();


  vtkSmartPointer<vtkImageShiftScale> shiftScale = vtkSmartPointer<vtkImageShiftScale>::New();
  shiftScale->SetOutputScalarTypeToUnsignedChar();
  shiftScale->SetInputConnection(readerOne->GetOutputPort());
  shiftScale->SetShift(100);
  shiftScale->SetScale(1);
  shiftScale->Update();

  vtkSmartPointer<vtkArrowSource> arrow = vtkSmartPointer<vtkArrowSource>::New();
  arrow->SetTipRadius(0.1);
  arrow->SetTipLength(0.35);
  arrow->SetShaftRadius(0.03);
  arrow->Update();
  
  vtkSmartPointer<vtkLookupTable> lut = vtkSmartPointer<vtkLookupTable>::New();
  lut->SetNumberOfTableValues(256);
  lut->SetHueRange(0.6667, 0);
  lut->SetTableRange(0, 5);
  lut->Build();
  lut->SetVectorMode(vtkScalarsToColors::MAGNITUDE);
	
  vtkSmartPointer<vtkGlyph3D> glyph =vtkSmartPointer<vtkGlyph3D>::New();
  glyph->SetInputConnection(readerOne->GetOutputPort());
  glyph->SetSourceConnection(arrow->GetOutputPort());
  glyph->SetVectorModeToUseVector();
  glyph->SetColorModeToColorByScalar();
  glyph->SetScaleModeToDataScalingOff();
  glyph->OrientOn();
  glyph->SetScaleFactor(0.25);

  vtkSmartPointer<vtkPolyDataMapper>polyData = vtkSmartPointer<vtkPolyDataMapper>::New();
  polyData->SetInputConnection(glyph->GetOutputPort());
  polyData->ScalarVisibilityOn();
  polyData->SetLookupTable(lut);

  vtkSmartPointer<vtkActor> actor=vtkSmartPointer<vtkActor>::New();
  
  actor->SetMapper(polyData);

  vtkSmartPointer<vtkRenderer> renderer =
  vtkSmartPointer<vtkRenderer>::New();
  //renderer->SetViewport(originalViewport);
  renderer->AddActor(actor);
  renderer->ResetCamera();
  renderer->SetBackground(255.0,255.0,255.0);
  renderer->GetActiveCamera()->Zoom(50.5);

  //renderer->SetActiveCamera(aCamera);

  vtkSmartPointer<vtkRenderWindow> renderWindow =
  vtkSmartPointer<vtkRenderWindow>::New();
  renderWindow->AddRenderer(renderer);

  vtkSmartPointer<vtkRenderWindowInteractor> renderWindowInteractor =
  vtkSmartPointer<vtkRenderWindowInteractor>::New();

  renderWindowInteractor->SetRenderWindow(renderWindow);
  renderWindowInteractor->Initialize();
  renderWindowInteractor->Start();

  return EXIT_SUCCESS;
}
