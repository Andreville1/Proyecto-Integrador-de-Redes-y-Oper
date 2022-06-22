#include "Memoria.h"

Memoria::Memoria(){
	this->paginas = std::array<char*,3>();
	this->paginas.fill("");
}

void Memoria::agregarPagina(PageTableEntry entrada){
	
	
	std::cout << "Agregar" << std::endl;
	this->paginas[this->count]  = entrada.getOperacion();
	std::cout << "En memoria:" << this->paginas[this->count] << std::endl;
	this->mmu->Notify("agregoMem", entrada.getOperacion(), entrada.getDireccion()); //Actualizar en la PT 

	std::cout << this->count << std::endl;
	this->count++;
}

void Memoria::setMMU(ManejoMemoria* mmu){
	this->mmu = mmu;
}