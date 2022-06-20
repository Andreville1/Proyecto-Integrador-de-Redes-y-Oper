#include "PageTable.h"

#include <math.h>
#include <time.h>

PageTable::PageTable(){

}

size_t PageTable::numeroFila(size_t indice){
	return (indice - indice % 3)/3; 
}

size_t PageTable::numeroColumna(size_t indice){
	return indice % 3;
}

void PageTable::agregarEntrada(char operacion[byteSize]){
	srand( time(NULL));

	PageTableEntry entry;
	entry.setNumPag(0);
	entry.setPresente(false);
	entry.setDireccion( rand() % 10 + 1);
	entry.setOperacion(operacion);
	entry.setReferencia(false);
	
	size_t fila = this->numeroColumna(this->contador); 
	size_t columna = this->numeroColumna(this->contador);

	this->entradas[fila][columna] = entry;
}

bool PageTable::buscarOperacion(char operacion[byteSize]){
	for (size_t fila = 0; fila < this->entradas.size(); ++fila)
	{
		for(size_t col = 0; col < 3; ++col){
			if(this->entradas[fila][col].getOperacion() == operacion){
				return true;
			}
		}
	}
	return false;
}