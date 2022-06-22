#ifndef MANEJOMEMORIA_H
#define MANEJOMEMORIA_H

#include <string>
#include <vector>


#include "Disco.h"
#include "PageTable.h"
#include "Memoria.h"
#include "PageReplacement.hpp"

class Disco;
class PageTable;
class Memoria;
class PageReplacement;

#define byteSize 8

class ManejoMemoria {
    protected:
        Disco* disco;
        PageTable* paginaTabla;
        Memoria* memoria;
		PageReplacement* algoritmo;
        std::vector<int> direcciones;

    public:
        ManejoMemoria(Disco* disco, PageTable* pagina, Memoria* memoria, PageReplacement* algoritmo);
        void Notify(std::string evento, char* operacion, int numPag);
        void agregarOperacion(char* operacion);
};

#endif // MANEJOMEMORIA_H