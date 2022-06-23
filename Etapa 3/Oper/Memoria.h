#ifndef MEMORIA_H
#define MEMORIA_H

#include "PageTableEntry.h"
#include "ManejoMemoria.h"
#include <array>

// #include <pybind11/pybind11.h>

// namespace py = pybind11;

class Memoria{
	protected:
		std::array<char*, 4> paginas;
		ManejoMemoria* mmu;
		int count = 0;

	public:
		Memoria();
		void agregarPagina(PageTableEntry entrada, int numPag);
		void setMMU(ManejoMemoria* mmu);
		void print();
};

#endif