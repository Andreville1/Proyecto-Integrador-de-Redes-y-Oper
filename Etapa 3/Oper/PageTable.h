#ifndef PAGETABLE_H
#define PAGETABLE_H

#include <array>
#include <vector>

#include <string>
#include "PageTableEntry.h"

#define byteSize 8

class PageTable{
	protected:
		std::vector<std::array<PageTableEntry,3>> entradas;
		size_t contador = 0;

	public:
		PageTable();
		bool buscarOperacion(char operacion[byteSize]);
		void agregarEntrada(char operacion[byteSize]);
		size_t numeroFila( size_t indice);
		size_t numeroColumna(size_t indice);
};

#endif