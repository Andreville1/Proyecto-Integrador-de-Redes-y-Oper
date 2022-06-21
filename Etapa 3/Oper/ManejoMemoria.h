#ifndef MANEJOMEMORIA_H
#define MANEJOMEMORIA_H

#include <string>
#include <vector>


#include "Disco.h"
#include "PageTable.h"
#include "Memoria.h"

class Disco;
class PageTable;
class Memoria;

#define byteSize 8

class ManejoMemoria {
    protected:
        Disco* disco;
        PageTable* paginaTabla;
        Memoria* memoria;
        std::vector<int> direcciones;

    public:
        ManejoMemoria(Disco* disco, PageTable* pagina, Memoria* memoria);
        void Notify(std::string evento, char* operacion, int direccion);
        void agregarOperacion(char* operacion);
};

#endif // MANEJOMEMORIA_H