#ifndef DISCO_H
#define DISCO_H

#include <string>
#include <vector>

#include "ManejoMemoria.h"

#define byteSize 8

class Disco {
	protected:
		std::vector<char*> operaciones;
		ManejoMemoria* mmu;
	
	public:
		void agregarOperacion(char operacion[byteSize]);
		Disco();
		

};

#endif // DISK_H