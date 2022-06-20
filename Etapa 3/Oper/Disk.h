#ifndef DISK_H
#define DISK_H

#include <string>
#include <vector>

#define byteSize 8

class Disk {
	protected:
		std::vector<char*> operaciones;
	
	public:
		void agregarOperacion(char operacion[byteSize]);
		Disk();
};

#endif // DISK_H