#include "ManejoMemoria.h"

#include "Disco.h"
#include "Memoria.h"
#include "PageTable.h"
#include "PageReplacement.hpp"

int main(int argc, char const *argv[])
{
    Disco* disk = new Disco();
    Memoria* mem = new Memoria();
    PageTable* pt = new PageTable();
    PageReplacement* algorithm = new PageReplacement();
    
    ManejoMemoria mmu(disk, pt, mem, algorithm);
    mmu.agregarOperacion("2+2");
    mmu.agregarOperacion("3+2");
    mmu.agregarOperacion("5+2");
      mmu.agregarOperacion("3+2");
    mmu.agregarOperacion("5+2");
      mmu.agregarOperacion("10+2");
    mmu.agregarOperacion("15+2");
    
    return 0;
}
