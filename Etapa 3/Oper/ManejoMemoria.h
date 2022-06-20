#ifndef MANEJOMEMORIA_H
#define MANEJOMEMORIA_H

#include <string>
#include <vector>


#include "Disco.h"
#include "PageTable.h"
#include "Memoria.h"

class Disco;

#define byteSize 8

class ManejoMemoria {
    protected:
        Disco* disco;
        PageTable* paginaTabla;
        Memoria* memoria;

    public:
        ManejoMemoria(Disco* disco, PageTable* pagina, Memoria* memoria);
        void Notify(std::string evento, char* operacion);

};

#endif // MANEJOMEMORIA_H