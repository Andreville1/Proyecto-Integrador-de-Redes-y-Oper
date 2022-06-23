#ifndef MEMORIA_H
#define MEMORIA_H

#include "PageTableEntry.h"
#include "ManejoMemoria.h"
#include <array>

class Memoria{
	protected:
		std::array<char*, 4> paginas;
		ManejoMemoria* mmu;
		int count = 0;

	public:
		Memoria();
		void agregarPagina(PageTableEntry entrada, int numPag);
		void setMMU(ManejoMemoria* mmu);
};

#endif