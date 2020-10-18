#include <vtkOBJReader.h>
#include <vtkPolyDataMapper.h>
#include <vtkActor.h>
#include <vtkRenderer.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkSmartPointer.h>
#include <string>
#include <vtkProperty.h>
#include <vtkLight.h>
#include <vtkCamera.h>
#include <vtkTexture.h>

int main(int, char *[])
{
	std::string filename = "XenoQueen.obj";
	vtkSmartPointer<vtkOBJReader> reader =
	vtkSmartPointer<vtkOBJReader>::New();
	reader->SetFileName(filename.c_str());
	reader->Update();
	
	vtkSmartPointer<vtkTexture> texture = 
    	vtkSmartPointer<vtkTexture>::New();
    	texture->MipmapOn();
	texture->InterpolateOn();
  	texture->SetInputConnection(reader->GetOutputPort());
	// Visualize
	vtkSmartPointer<vtkPolyDataMapper> mapper =
	vtkSmartPointer<vtkPolyDataMapper>::New();
	mapper->SetInputConnection(reader->GetOutputPort());
	
	vtkSmartPointer<vtkActor> actor =
	vtkSmartPointer<vtkActor>::New();
	//actor->SetMapper(mapper);
	actor->GetProperty()->SetColor(1.0000, 0.3882, 0.2784);
	
	vtkSmartPointer<vtkActor> sphere1 =
    	vtkSmartPointer<vtkActor>::New();
  	sphere1->SetMapper(mapper);
  	sphere1->GetProperty()->SetColor(1,1,1);
	sphere1->GetProperty()->SetAmbient(0.10);
	sphere1->GetProperty()->SetDiffuse(0.30);
  	sphere1->GetProperty()->SetSpecular(1.0);
  	sphere1->GetProperty()->SetSpecularPower(5.0);
  	
	vtkSmartPointer<vtkRenderer> renderer =
	vtkSmartPointer<vtkRenderer>::New();
	renderer->AddActor(actor);
	renderer->ResetCamera();
		
	renderer->AddActor(sphere1);
	
	vtkSmartPointer<vtkLight> light =
    	vtkSmartPointer<vtkLight>::New();
  	light->SetFocalPoint(0, 0, 1);
  	light->SetPosition(1, 0, 0);
  	light->SetColor(1, 0, 0);
  	light->SetSpecularColor(0, 0, 1.0);
  	renderer->AddLight(light);
  
  	vtkSmartPointer<vtkLight> light1 =
    	vtkSmartPointer<vtkLight>::New();
  	light1->SetFocalPoint(0, 0, 0);
  	light1->SetPosition(-1, 0, 0);
  	light1->SetColor(0, 0, 1);
  	light1->SetSpecularColor(0.5, 0, 0);
  	renderer->AddLight(light1);
  	
  	vtkSmartPointer<vtkLight> light2 =
    	vtkSmartPointer<vtkLight>::New();
  	light2->SetFocalPoint(1, 1, 1);
  	light2->SetPosition(-12, 0, 0);
  	light2->SetColor(0, 0, 0);
  	light2->SetSpecularColor(0.5, 0, 0);
  	renderer->AddLight(light2);
  	
  	/*renderer->GetActiveCamera()->SetFocalPoint(0,0,0);
  	renderer->GetActiveCamera()->SetPosition(0,0,1);
  	renderer->GetActiveCamera()->SetViewUp(0,1,0);
  	renderer->GetActiveCamera()->ParallelProjectionOn();
  	renderer->ResetCamera();
  	renderer->GetActiveCamera()->SetParallelScale(1.5);
*/
	vtkSmartPointer<vtkRenderWindow> renderWindow =
	vtkSmartPointer<vtkRenderWindow>::New();
	//renderWindow->SetSize(800, 600);
	renderWindow->AddRenderer(renderer);

	vtkSmartPointer<vtkRenderWindowInteractor> renderWindowInteractor =
	vtkSmartPointer<vtkRenderWindowInteractor>::New();
	renderWindowInteractor->SetRenderWindow(renderWindow);

	renderer->SetBackground(0.0, 0.0, 0.0);

	renderer->SetEnvironmentTexture(texture);
	
	renderWindowInteractor->Start();

	return EXIT_SUCCESS;
}
