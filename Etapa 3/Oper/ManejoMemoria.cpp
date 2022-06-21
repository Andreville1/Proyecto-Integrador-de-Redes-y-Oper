#include "ManejoMemoria.h"
#include <iostream>

ManejoMemoria::ManejoMemoria(Disco* disco, PageTable* pagina, Memoria* memoria) 
{
    this->disco = disco;
    this->memoria = memoria;
    this->paginaTabla = pagina;

    this->disco->setMMU(this);
    this->paginaTabla->setMMU(this);
    this->memoria->setMMU(this);

}

void ManejoMemoria::Notify(std::string evento, char* operacion, int direccion){
    if(evento == "OPDisco"){
        // Se agrego operacion al disco 
        // Agregarlo a mi pageT
        this->paginaTabla->agregarEntrada(operacion);
        this->direcciones.push_back(direccion);
        
    }
    if( evento == "OPPageTable"){
        // Se agrega operacion al PT
        // agregar a memoria 
    }
}

void ManejoMemoria::agregarOperacion(char* operacion){
    this->disco->agregarOperacion(operacion);
}
