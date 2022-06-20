#include "Disco.h"

#include <iostream>


Disco::Disco(){
	this->operaciones =  std::vector<char*>();
}

void Disco::agregarOperacion(char operacion[byteSize]){
	this->operaciones.push_back(operacion);
	std::cout << "Disco: " << this->operaciones.back() << std::endl;
	// this->mmu->Notify("OPDisco", operacion);
}

// void Disk::setMMU(ManejoMemoria* mmu){
// 	this->mmu = mmu; 
// }