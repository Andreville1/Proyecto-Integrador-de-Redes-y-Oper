#include "Disco.h"

#include <iostream>


Disco::Disco(){
	this->operaciones =  std::vector<char*>();
}

void Disco::agregarOperacion(char operacion[byteSize]){
	this->operaciones.push_back(operacion);
	this->mmu->Notify("OPDisco", operacion, 0);
}

void Disco::setMMU(ManejoMemoria* mmu){
	this->mmu = mmu; 
}

void Disco::print(){
	std::cout << "Disk class " << std::endl;
}


// PYBIND11_MODULE(DISK, DISK_handle) {
//  DISK_handle.doc() = "I'm a docstring hehe";
//   py::class_<Disco>(
// 			DISK_handle, "Disco"
// 			).def(py::init<>())
//       .def("imprimir", &Disco::print)
// 	  .def("addOp", &Disco::agregarOperacion)
// 	  .def("setMMU", &Disco::setMMU)
//       ;
// }