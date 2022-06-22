#include "PageReplacement.hpp"
#include <algorithm>

bool PageReplacement::pagePresent(int page) {
    return std::find(pages.begin(), pages.end(), page) != pages.end();
}

void PageReplacement::giveSecondChance(int page) {
    int index = std::find(pages.begin(), pages.end(), page) - pages.begin();
    secondChances[index] = true;
}

void PageReplacement::replacePage(int page) {
    while (true) {
        if (!secondChances[pointer]) {
            pages[pointer] = page;
            pointer = ((pointer + 1) % num_frames + num_frames)
                % num_frames;
            return;
        }

        secondChances[pointer] = false;
        pointer = ((pointer + 1) % num_frames + num_frames) % num_frames;
    }
}

PageReplacement::PageReplacement() {
    pages.resize(num_frames);
    secondChances.resize(num_frames);

    std::fill(pages.begin(), pages.end(), -1);
    std::fill(secondChances.begin(), secondChances.end(), false);
}

int PageReplacement::calculateFrame(int page) {
    if (pagePresent(page)) {
        giveSecondChance(page);
        return -1;
    }

    replacePage(page);
    return ((pointer - 1) % num_frames + num_frames) % num_frames;
}

void PageReplacement::setMMU(ManejoMemoria* mmu){
	this->mmu = mmu;
}