#include "ManejoMemoria.h"
#include <iostream>

// ManejoMemoria::ManejoMemoria(){
    
// }

ManejoMemoria::ManejoMemoria(Disco* disco, PageTable* pagina, Memoria* memoria, PageReplacement* algoritmo) 
{
    this->file.open ("archivo.txt", std::fstream::in | std::fstream::out | std::fstream::app);;

    this->disco = disco;
    this->memoria = memoria;
    this->paginaTabla = pagina;
	this->algoritmo = algoritmo;

    this->disco->setMMU(this);
    this->paginaTabla->setMMU(this);
    this->memoria->setMMU(this);
	this->algoritmo->setMMU(this);

}

ManejoMemoria::~ManejoMemoria(){
    this->file.close();
}

void ManejoMemoria::Notify(std::string evento, char* operacion, int numPag){
    if(evento == "OPDisco"){
        // Se agrego operacion al disco 
        // Agregarlo a mi pageT
        this->paginaTabla->agregarEntrada(operacion);
        this->direcciones.push_back(numPag);
        
    }
    if( evento == "OPPageTable"){
        // Se agrega operacion al PT
        // agregar a memoria
        PageTableEntry* entrada = this->paginaTabla->buscarOperacion(operacion);
        std::cout << "entrada en PT:" << *entrada << std::endl;
		
        int numPagNueva = this->algoritmo->calculateFrame(entrada->getNumPag());
        if( numPagNueva != -1){
            
            this->memoria->agregarPagina(*entrada, numPagNueva);
        }
        else{
            this->paginaTabla->setNumPag( this->paginaTabla->getNumPag() -1);
        }
    }
	if (evento == "agregoMem"){
		PageTableEntry* entrada = this->paginaTabla->buscarOperacion(operacion);

        
		entrada->setNumPag(numPag);
		entrada->setPresente(1);
		entrada->setReferencia(1);
        std::cout << "agregoMem:" <<*entrada << std::endl; 
        ExpressionParser parser;
        std::string result = parser.simplifyExpression(operacion);
        this->file << result << std::endl;
	}
}

void ManejoMemoria::agregarOperacion(char* operacion){
    this->disco->agregarOperacion(operacion);
    std::cout << operacion << std::endl;
}

void ManejoMemoria::print(){
    std::cout << "Manejo memoria class" << std::endl;
}

// PYBIND11_MODULE(MMU, MMU_handle) {
//   MMU_handle.doc() = "I'm a docstring hehe";
//   py::class_<ManejoMemoria>(
// 			MMU_handle, "ManejoMemoria"
// 			).def(py::init<Disco*, PageTable*,Memoria*, PageReplacement*>())
//       .def("imprimir", &ManejoMemoria::print)
//       .def("notificar", &ManejoMemoria::Notify)
//       .def("addOP", &ManejoMemoria::agregarOperacion)
//       ;
// }