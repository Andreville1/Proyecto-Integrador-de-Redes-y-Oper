#include "PageTableEntry.h"

PageTableEntry::PageTableEntry(){
	this->presente = 0;
	this->numPag = 0;
	this->referencia = 0;
	this->direccion = 0;
}

bool PageTableEntry::getPresente(){
	return this->presente;
}

void PageTableEntry::setPresente(bool flag){
	this->presente = flag;
}

bool PageTableEntry::getReferencia()
{
	return this->referencia;
}

void PageTableEntry::setReferencia(bool flag)
{
	this->referencia = flag;
}

int PageTableEntry::getNumPag(){
	return this->numPag;
}

void PageTableEntry::setNumPag(int num){
	this->numPag = num;
}

char* PageTableEntry::getOperacion(){
	return this->operacion;
}

void PageTableEntry::setDireccion(int direccion){
	this->direccion = direccion;
}

int PageTableEntry::getDireccion(){
	return this->direccion;
}

void PageTableEntry::setOperacion(char* operacion){
	this->operacion = operacion;
}

void reset(){

}

std::ostream& operator<<(std::ostream& os, const PageTableEntry& dt)
{
    os << dt.operacion << '|' << dt.numPag << '|' << dt.direccion
		<< '|' << dt.presente << "|" << dt.referencia;
    return os;
}

