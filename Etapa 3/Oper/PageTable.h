#ifndef PAGETABLE_H
#define PAGETABLE_H

#include <array>
#include <vector>

#include <string>
#include "ManejoMemoria.h"
#include "PageTableEntry.h"

#include <pybind11/pybind11.h>

namespace py = pybind11;

class ManejoMemoria;

#define byteSize 8

class PageTable{
	protected:
		std::vector<std::array<PageTableEntry,3>> entradas;
		size_t contador = 0;
		size_t numPag = 0;
		ManejoMemoria* mmu;

	public:
		PageTable();
		PageTableEntry* buscarOperacion(char operacion[byteSize]);
		void agregarEntrada(char operacion[byteSize]);
		size_t numeroFila( size_t indice);
		size_t numeroColumna(size_t indice);
		void setMMU(ManejoMemoria* mmu);
		void print();
		void setNumPag(size_t numPag);
		size_t getNumPag();

};



#endif