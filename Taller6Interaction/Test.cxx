#include <vtkMetaImageReader.h>
#include <vtkImageActor.h>
#include <vtkRenderer.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkInteractorStyleImage.h>
#include <vtkImageMapper3D.h>
#include <vtkMarchingCubes.h>
#include <vtkPolyDataMapper.h>
#include <vtkActor.h>
#include "vtkStripper.h"
#include "vtkCamera.h"
#include "vtkProperty.h"
#include "vtkPolyDataConnectivityFilter.h"
#include "vtkNamedColors.h"
#include "vtkCamera.h"
#include <vtkWorldPointPicker.h>
#include <vtkRendererCollection.h>


class MouseInteractorStyle : public vtkInteractorStyleTrackballCamera
{
public:
  static MouseInteractorStyle* New();
  vtkTypeMacro(MouseInteractorStyle, vtkInteractorStyleTrackballCamera);

  virtual void OnLeftButtonDown() override
  {
    std::cout << "Picking pixel: " << this->Interactor->GetEventPosition()[0] << " " << this->Interactor->GetEventPosition()[1] << std::endl;
    this->Interactor->GetPicker()->Pick(this->Interactor->GetEventPosition()[0], 
                                        this->Interactor->GetEventPosition()[1], 
                                        0,  // always zero.
                                        this->Interactor->GetRenderWindow()->GetRenderers()->GetFirstRenderer());
    double picked[3];
    this->Interactor->GetPicker()->GetPickPosition(picked);
    std::cout << "Picked value: " << picked[0] << " " << picked[1] << " " << picked[2] << std::endl;
    // Forward events
    vtkInteractorStyleTrackballCamera::OnLeftButtonDown();
  }

};
vtkStandardNewMacro(MouseInteractorStyle);

int main(int, char *[])
{
vtkSmartPointer<vtkNamedColors> colors =
vtkSmartPointer<vtkNamedColors>::New();

std::array<unsigned char , 4> skinColor{{255, 125, 64}};
colors->SetColor("SkinColor", skinColor.data());
std::array<unsigned char , 4> bkg{{51, 77, 102, 255}};
colors->SetColor("BkgColor", bkg.data());

vtkSmartPointer<vtkMetaImageReader> reader =
vtkSmartPointer<vtkMetaImageReader>::New();
reader->SetFileName("ct/training_001_ct.mhd");
reader->Update();

double originalViewport[4] = {0.0, 0.0, 0.33, 1.0};
double originalViewport1[4] = {0.33, 0.0, 0.66, 1.0};
double originalViewport2[4] = {0.66, 0.0, 1.0, 1.0};

vtkSmartPointer<vtkWorldPointPicker> worldPointPicker = 
vtkSmartPointer<vtkWorldPointPicker>::New();

vtkSmartPointer<vtkMarchingCubes> skinExtractor=
vtkSmartPointer<vtkMarchingCubes>::New();
skinExtractor->SetInputConnection(reader->GetOutputPort());
skinExtractor->SetValue(0, 500);

vtkSmartPointer<vtkMarchingCubes> boneExtractor=
vtkSmartPointer<vtkMarchingCubes>::New();
boneExtractor->SetInputConnection(reader->GetOutputPort());
boneExtractor->SetValue(0,-100);

vtkSmartPointer<vtkStripper> skinStripper =
vtkSmartPointer<vtkStripper>::New();
skinStripper->SetInputConnection(skinExtractor->GetOutputPort());
skinStripper->Update();

vtkSmartPointer<vtkStripper> boneStripper =
vtkSmartPointer<vtkStripper>::New();
boneStripper->SetInputConnection(boneExtractor->GetOutputPort());
boneStripper->Update();

vtkSmartPointer<vtkPolyDataMapper> skinMapper =
vtkSmartPointer<vtkPolyDataMapper>::New();
skinMapper->SetInputConnection(skinStripper->GetOutputPort());
skinMapper->ScalarVisibilityOff();

vtkSmartPointer<vtkPolyDataMapper> boneMapper =
vtkSmartPointer<vtkPolyDataMapper>::New();
boneMapper->SetInputConnection(boneStripper->GetOutputPort());
boneMapper->ScalarVisibilityOff();

vtkSmartPointer<vtkActor> skin =
vtkSmartPointer<vtkActor>::New();
skin->SetMapper(skinMapper);

vtkSmartPointer<vtkActor> skin1 =
vtkSmartPointer<vtkActor>::New();
skin1->SetMapper(skinMapper);
skin1->GetProperty()->SetColor(colors->GetColor3d("BkgColor").GetData());
skin1->GetProperty()->SetSpecular(.3);
skin1->GetProperty()->SetSpecularPower(20);
skin1->GetProperty()->SetOpacity(.5);

vtkSmartPointer<vtkActor> skin2 =
vtkSmartPointer<vtkActor>::New();
skin2->SetMapper(boneMapper);
skin2->GetProperty()->SetDiffuseColor(colors->GetColor3d("SkinColor").GetData());

vtkSmartPointer<vtkRenderer> renderer =
vtkSmartPointer<vtkRenderer>::New();
renderer->SetViewport(originalViewport);
renderer->AddActor(skin);
renderer->ResetCamera();

vtkSmartPointer<vtkRenderer> renderer1 =
vtkSmartPointer<vtkRenderer>::New();
renderer1->SetViewport(originalViewport1);
renderer1->AddActor(skin1);
renderer1->ResetCamera();

vtkSmartPointer<vtkCamera> aCamera =
vtkSmartPointer<vtkCamera>::New();
aCamera->SetViewUp (0, 0, -1);
aCamera->SetPosition (0, -1, 0);
aCamera->SetFocalPoint (0, 0, 0);
aCamera->ComputeViewPlaneNormal();
aCamera->Azimuth(30.0);
aCamera->Elevation(30.0);

vtkSmartPointer<vtkRenderer> renderer2 =
vtkSmartPointer<vtkRenderer>::New();
renderer2->SetViewport(originalViewport2);
renderer2->AddActor(skin);
renderer2->AddActor(skin2);
renderer2->SetActiveCamera(aCamera);
renderer2->ResetCamera();

vtkSmartPointer<vtkRenderWindow> renderWindow =
vtkSmartPointer<vtkRenderWindow>::New();
renderWindow->AddRenderer(renderer);
renderWindow->AddRenderer(renderer1);
renderWindow->AddRenderer(renderer2);

vtkSmartPointer<vtkRenderWindowInteractor> renderWindowInteractor =
vtkSmartPointer<vtkRenderWindowInteractor>::New();

vtkSmartPointer<MouseInteractorStyle> style = 
vtkSmartPointer<MouseInteractorStyle>::New();
renderWindowInteractor->SetInteractorStyle( style );
renderWindowInteractor->SetRenderWindow(renderWindow);
renderWindowInteractor->SetPicker(worldPointPicker);

renderWindowInteractor->Initialize();
renderWindowInteractor->Start();
return EXIT_SUCCESS;
}
