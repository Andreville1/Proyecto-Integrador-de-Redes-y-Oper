#ifndef PAGE_REPLACEMENT_HPP
#define PAGE_REPLACEMENT_HPP

#include <vector>

#include "ManejoMemoria.h"

class PageReplacement {
private:
    int pointer = 0;
    int num_frames = 4;
    std::vector<int> pages {};
    std::vector<bool> secondChances {};

	ManejoMemoria* mmu;

    bool pagePresent(int page);

    void giveSecondChance(int page);

    void replacePage(int page);
	

public:
    PageReplacement();

    int calculateFrame(int page);
	void setMMU(ManejoMemoria *mmu);
};

#endif
