#include "Memoria.h"

Memoria::Memoria(){
	this->paginas = std::array<char*,3>();
	this->paginas.fill("");
}

void Memoria::agregarPagina(PageTableEntry entrada, int numPag){
	

	this->paginas[numPag]  = entrada.getOperacion();
	this->mmu->Notify("agregoMem", entrada.getOperacion(), entrada.getNumPag()); //Actualizar en la PT 

	std::cout << this->count << std::endl;
	this->count++;
}

void Memoria::setMMU(ManejoMemoria* mmu){
	this->mmu = mmu;
}