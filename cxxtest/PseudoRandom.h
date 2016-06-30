#pragma once
#include <vector>
#include <random>
#include <algorithm>
#include <ctime>
#include <set>

#define PUSH_COUNTER 1000
class PseudoRandom
{
private:

    std::mt19937_64 m_generator;
    unsigned int m_randomCount;
    unsigned int m_seed;

public:
    PseudoRandom()
        : PseudoRandom(std::time(NULL))
    {
    };

    PseudoRandom(unsigned int seed)
        : m_randomCount(PUSH_COUNTER) // move mersenne past initial instability
        , m_seed(seed)
    {
        m_generator.seed(seed);
        for (int i = 0; i <= m_randomCount; i++)
            m_generator();
    };
    ~PseudoRandom()
    {
    };

    inline unsigned int GetSeed() { return m_seed; };
    inline unsigned int GetRandomCount() { return m_randomCount; };

    template <typename T>
    T GetRandomIntValue(const T lowPointInclusive, const T highPointExclusive) {
        if (lowPointInclusive >= highPointExclusive)
            return lowPointInclusive;

        m_randomCount++;
        return (m_generator() % (highPointExclusive - lowPointInclusive)) + lowPointInclusive;
    }

    template <typename T>
    void GetRandomIntValues(const std::size_t count,
        const T lowPointInclusive,
        const T highPointExclusive,
        std::set<T> &randomInts) { // TODO somehow a multiset version of this should be made
        for (std::size_t i = 0; i < count; i++) {
            randomInts.insert(this->GetRandomIntValue(lowPointInclusive, highPointExclusive));
        }
    }

    template <typename T>
    std::set<T> SelectRandomValues(const std::size_t count, const std::set<T> &values) {
        std::set<T> output;

        // without this the while loop could spin out of control.
        if (values.size() <= count) {
            output = values;
            return output;
        }

        // using a while loop instead of for ensures that we output the entire count to a set 
        // (if a random value occurs twice then a set would only allow insertion once)
        auto it = values.begin();
        uint32_t zero, n, endIndex;
        zero = 0;
        endIndex = values.size();
        while (output.size() < count) {
            n = this->GetRandomIntValue(zero, endIndex);
            output.insert(*std::next(values.begin(), n));
        }
        return output;
    }

    template <typename Iterator>
    void Shuffle(Iterator first, Iterator last)
    {
        if (first + 1 == last)
            return;

        typename std::iterator_traits<Iterator>::difference_type i, n, d, zero;
        zero = 0;
        n = (last - first);
        for (i = n - 1; i > 0; --i)
        {
            d = this->GetRandomIntValue(zero, i + 1);
            std::swap(first[i], first[d]);
        }
    };
};


