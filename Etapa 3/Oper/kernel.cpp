#include "ManejoMemoria.h"

#include "Disco.h"
#include "Memoria.h"
#include "PageTable.h"

int main(int argc, char const *argv[])
{
    Disco* disk = new Disco();
    Memoria* mem = new Memoria();
    PageTable* pt = new PageTable();
    ManejoMemoria mmu(disk, pt, mem);
    mmu.agregarOperacion("2+2");
    mmu.agregarOperacion("3+2");
    mmu.agregarOperacion("5+2");
      mmu.agregarOperacion("3+2");
    mmu.agregarOperacion("5+2");
      mmu.agregarOperacion("3+2");
    mmu.agregarOperacion("5+2");
    
    return 0;
}
