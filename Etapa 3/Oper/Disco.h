#ifndef DISCO_H
#define DISCO_H

#include <string>
#include <vector>

#include "ManejoMemoria.h"

class ManejoMemoria;

#include <pybind11/pybind11.h>

namespace py = pybind11;

#define byteSize 8

class Disco {
	protected:
		std::vector<char*> operaciones;
		ManejoMemoria* mmu;
	
	public:
		void agregarOperacion(char operacion[byteSize]);
		Disco();
		void setMMU(ManejoMemoria* mmu);
		void print();

};

#endif // DISK_H