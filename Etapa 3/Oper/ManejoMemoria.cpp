#include "ManejoMemoria.h"

ManejoMemoria::ManejoMemoria(Disco* disco, PageTable* pagina, Memoria* memoria) 
{
    this->disco = disco;
    this->memoria = memoria;
    this->paginaTabla = pagina;

}

void ManejoMemoria::Notify(std::string evento, char* operacion){
    if(evento == "OPDisco"){
        
    }
}