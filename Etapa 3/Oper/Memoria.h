#ifndef MEMORIA_H
#define MEMORIA_H

#include "PageTableEntry.h"
#include <array>

class Memoria{
	protected:
		std::array<PageTableEntry, 4> paginas;

	public:
		Memoria();
		void agregarPagina(PageTableEntry entrada);
};

#endif