#include "Disk.h"

Disk::Disk(){
	this->operaciones =  std::vector<char*>();
}

void Disk::agregarOperacion(char operacion[byteSize]){
	this->operaciones.push_back(operacion);
}