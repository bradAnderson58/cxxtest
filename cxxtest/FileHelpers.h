#pragma once

#include "PseudoRandom.h"

#include <fstream>
#include <random>
#include <memory>
#include <regex>
#include <iterator>
#include <set>

#include <dirent.h>

class FileHelpers {
public:
    static std::vector<std::string> GetFiles(const char *inputDirectory) {
        std::regex emptyRegex;
        return GetFiles(inputDirectory, emptyRegex);
    };

    static std::vector<std::string> GetFiles(const char *inputDirectory, std::regex &inclusionFilter) {
        DIR *dpdf;
        struct dirent *epdf;
        std::vector<std::string> filenames;
        std::smatch res;
        dpdf = opendir(inputDirectory);
        if (dpdf != NULL) {
            while (epdf = readdir(dpdf)) {
                std::string filename = std::string() + inputDirectory + epdf->d_name;
                if (std::regex_search(filename, res, inclusionFilter))
                    filenames.push_back(filename);
            }
        }

        return filenames;
    }

    static std::vector<std::string> GetRandomLines(
        const std::string &filename,
        const int count,
        const bool bShuffled,
        std::regex &lineFilter,
        std::shared_ptr<PseudoRandom> pseudoRandom)
    {
        std::ifstream textFile(filename);

        // new lines will be skipped unless we stop it from happening:    
        textFile.unsetf(std::ios_base::skipws);

        // count the newlines with an algorithm specialized for counting:
        std::string line;
        std::set<uint32_t> mathcedIndices;
        std::smatch res;
        uint32_t lineCount = 0;
        while (std::getline(textFile, line)) {
            if (std::regex_search(line, res, lineFilter))
                mathcedIndices.insert(lineCount++);
        }

        // reset file state
        textFile.clear();
        textFile.seekg(0, std::ios::beg);

        // use set so there aren't any repeated lines
        // also insures that they're sorted (since stl is weird and makes set sorted)
        std::set<uint32_t> lineIndices = pseudoRandom->SelectRandomValues(count, mathcedIndices);

        // we could have just selected lines in the above while loop and then randomly picked 
        // some of them, but this would mean keeping a whole lot of lines in memory, instead we 
        // are only keeping the line indices in memory.
        std::vector<std::string> randomLines;
        uint32_t line_number = 0;
        for (auto iter = lineIndices.begin(); iter != lineIndices.end(); iter++) {
            while (std::getline(textFile, line)) {
                if (*iter == line_number++) {
                    std::regex_search(line, res, lineFilter);
                    randomLines.push_back(res[1]);
                    break;
                }
            }
        }

        // set, is sorted by definition. (this helps with the line selection as we iterate from low line numbers up)
        // if the output should be lines in random order then they need to be shuffled
        if (bShuffled)
            pseudoRandom->Shuffle(randomLines.begin(), randomLines.end());

        return randomLines;
    }
};
