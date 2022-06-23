#ifndef PAGE_REPLACEMENT_HPP
#define PAGE_REPLACEMENT_HPP

#include <vector>

#include "ManejoMemoria.h"

#include <pybind11/pybind11.h>

namespace py = pybind11;

class PageReplacement {
protected:
    int pointer = 0;
    int num_frames = 4;
    std::vector<int> pages {};
    std::vector<bool> secondChances {};

	ManejoMemoria* mmu;

    

public:
    bool pagePresent(int page);

        void giveSecondChance(int page);

        void replacePage(int page);
        
    PageReplacement();
    void print();
    int calculateFrame(int page);
	void setMMU(ManejoMemoria *mmu);
};

#endif
