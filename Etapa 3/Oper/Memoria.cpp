#include "Memoria.h"

Memoria::Memoria(){
	
}

void Memoria::agregarPagina(PageTableEntry entrada){
	for(size_t index = 0; index < 4;++ index){
		if( this->paginas[index].getPresente() == 0){
			this->paginas[index] = entrada;
		}
	}
}

void Memoria::setMMU(ManejoMemoria* mmu){
	this->mmu = mmu;
}