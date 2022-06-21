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