#ifndef MEMORIA_H
#define MEMORIA_H

#include "PageTableEntry.h"
#include "ManejoMemoria.h"
#include <array>

class Memoria{
	protected:
		std::array<PageTableEntry, 4> paginas;
		ManejoMemoria* mmu;

	public:
		Memoria();
		void agregarPagina(PageTableEntry entrada);
		void setMMU(ManejoMemoria* mmu);
};

#endif