#include "Memoria.h"

Memoria::Memoria(){
	this->paginas = std::array<char*,4>();
	this->paginas.fill("");
}

void Memoria::agregarPagina(PageTableEntry entrada, int numPag){
	

	this->paginas[numPag]  = entrada.getOperacion();
	this->mmu->Notify("agregoMem", entrada.getOperacion(), numPag); //Actualizar en la PT 
}

void Memoria::setMMU(ManejoMemoria* mmu){
	this->mmu = mmu;
}

void Memoria::print(){
	std::cout << "Memoria class" << std::endl;
}

PYBIND11_MODULE(MEM, MEM_handle) {
  MEM_handle.doc() = "I'm a docstring hehe";
  py::class_<Memoria>(
			MEM_handle, "Memoria"
			).def(py::init<>())
      .def("imprimir", &Memoria::print)
	  .def("addPage", &Memoria::agregarPagina)
	  .def("setMMU", &Memoria::setMMU)
      ;
}