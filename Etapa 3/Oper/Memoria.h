#ifndef MEMORIA_H
#define MEMORIA_H

#include "PageTableEntry.h"
#include <array>

class Memory{
	protected:
		std::array<PageTableEntry, 4> paginas;

	public:
		Memory();
		void agregarPagina(PageTableEntry entrada);
};

#endif