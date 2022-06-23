#include "ManejoMemoria.h"

#include "Disco.h"
#include "Memoria.h"
#include "PageTable.h"
#include "PageReplacement.h"
#include "PageTableEntry.h"

#include <pybind11/pybind11.h>

namespace py = pybind11;

int main(int argc, char const *argv[])
{
    return 0;
}

class Oper {
  Disco* disk;
  Memoria* mem;
  PageTable* pt;
  PageReplacement* algorithm;
  ManejoMemoria* mmu;
  public:
    Oper(){
      this->disk = new Disco();
      this->mem = new Memoria();
      this->pt = new PageTable();
      this->algorithm = new PageReplacement();
      mmu = new ManejoMemoria(this->disk, this->pt, this->mem, this->algorithm);
    }

    char* agregarOperacion(char* op){
      mmu->agregarOperacion(op);
      return op;
    }
};

PYBIND11_MODULE(module_name, module_handle) {
  module_handle.doc() = "I'm a docstring hehe";
  py::class_<Oper>(
			module_handle, "Oper"
			).def(py::init<>())
      .def("agregarOperacion", &Oper::agregarOperacion);
}