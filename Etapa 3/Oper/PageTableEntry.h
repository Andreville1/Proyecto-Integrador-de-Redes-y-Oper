#ifndef PAGETABLEENTRY_H
#define PAGETABLEENTRY_H

#define byteSize 8

#include <iostream>

class PageTableEntry
{
private:
	bool presente;
	int numPag;
	bool referencia;
	char* operacion;
	int direccion;

public:
	PageTableEntry();
	bool getPresente();
	void setPresente(bool flag);
	bool getReferencia();
	void setReferencia(bool flag);

	int getNumPag();
	void setNumPag(int num);
	char* getOperacion();
	void setDireccion(int direccion);
	int getDireccion();
	void setOperacion(char* operacion);

	void reset();

	friend std::ostream& operator<<(std::ostream& os, const PageTableEntry& pageTable);
};

#endif