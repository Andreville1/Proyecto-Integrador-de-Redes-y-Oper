#ifndef PAGETABLEENTRY_H
#define PAGETABLEENTRY_H

#define byteSize 8

class PageTableEntry
{
private:
	bool presente;
	int numPag;
	bool referencia;
	char operacion[byteSize];
	int direccion;

public:
	PageTableEntry();
	bool getPresente();
	void setPresente(bool flag);

	int getNumPag();
	void setNumPag(int num);
	char* getOperacion();
	void setDireccion(int direccion);
	int getDireccion();

	void reset();
};

#endif