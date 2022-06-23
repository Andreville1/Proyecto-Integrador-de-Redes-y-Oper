#include "PageTable.h"

#include <math.h>
#include <time.h>

#include <iostream>

PageTable::PageTable(){
	this->entradas =  std::vector<std::array<PageTableEntry,3>>();
}

size_t PageTable::numeroFila(size_t indice){
	size_t mod = indice % 3;
	size_t diff = indice - mod;
	return diff/3;
}

size_t PageTable::numeroColumna(size_t indice){
	return indice % 3;
}

void PageTable::agregarEntrada(char operacion[byteSize]){

	if(this->contador %3 == 0){
		std::array<PageTableEntry,3> ptr = std::array<PageTableEntry,3>();
		this->entradas.push_back(ptr);
	}
	
	

	PageTableEntry entry;
	entry.setNumPag(this->numPag);
	entry.setPresente(false);
	entry.setDireccion(this->contador);
	entry.setOperacion(operacion);
	entry.setReferencia(false);
	
	size_t fila = this->numeroFila(this->contador); 
	size_t columna = this->numeroColumna(this->contador);



	this->entradas[fila][columna] = entry;
	
	this->contador++;
	this->numPag++;
	this->mmu->Notify("OPPageTable", operacion, entry.getNumPag());

}

PageTableEntry* PageTable::buscarOperacion(char operacion[byteSize]){
	for (size_t fila = 0; fila < this->entradas.size(); ++fila)
	{
		for(size_t col = 0; col < 3; ++col){
			if(this->entradas[fila][col].getOperacion() == operacion){
				return &this->entradas[fila][col];
			}
		}
	}
	return NULL;
}

void PageTable::setMMU(ManejoMemoria* mmu){
	this->mmu = mmu;
}

void PageTable::print(){
	std::cout << "-----------------" << std::endl;
	for (size_t fila = 0; fila < this->entradas.size(); fila++)
	{
		for (size_t columna = 0; columna < 3; columna++)
		{
			std::cout << this->entradas[fila][columna] << std::endl;
		}
		
	}
	
	
}

void PageTable::setNumPag(size_t numPag){
	this->numPag = numPag;
}

size_t PageTable::getNumPag(){
	return this->numPag;
}

PYBIND11_MODULE(PT, PT_handle) {
  PT_handle.doc() = "I'm a docstring hehe";
  py::class_<PageTable>(
			PT_handle, "PageTable"
			).def(py::init<>())
      .def("imprimir", &PageTable::print)
	  .def("buscar", &PageTable::buscarOperacion)
	  .def("agregar", &PageTable::agregarEntrada)
	  .def("numFila", &PageTable::numeroFila)
	  .def("numCol", &PageTable::numeroColumna)
	  .def("setMMU", &PageTable::setMMU)
	  .def("setNumPag", &PageTable::setNumPag)
	  .def("getNumPag", &PageTable::agregarEntrada);
}