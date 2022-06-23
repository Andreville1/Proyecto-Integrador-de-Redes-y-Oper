#include "ManejoMemoria.h"

#include "Disco.h"
#include "Memoria.h"
#include "PageTable.h"
#include "PageReplacement.h"
#include "PageTableEntry.h"

// #include <pybind11/pybind11.h>

// namespace py = pybind11;

#include "ManejoMemoria.h"

#include "Disco.h"
#include "Memoria.h"
#include "PageTable.h"
#include "PageReplacement.h"

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

// PYBIND11_MODULE(module_name, module_handle) {
//   module_handle.doc() = "I'm a docstring hehe";
//   py::class_<Oper>(
// 			module_handle, "Oper"
// 			).def(py::init<>())
//       .def("agregarOperacion", &Oper::agregarOperacion);
// }