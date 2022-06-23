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