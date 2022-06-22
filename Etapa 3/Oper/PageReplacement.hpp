#ifndef PAGE_REPLACEMENT_HPP
#define PAGE_REPLACEMENT_HPP

#include <vector>

class PageReplacement {
private:
    int pointer = 0;
    int num_frames = 3;
    std::vector<int> pages {};
    std::vector<bool> secondChances {};

    bool pagePresent(int page);

    void giveSecondChance(int page);

    void replacePage(int page);

public:
    PageReplacement();

    int calculateFrame(int page);
};

#endif
