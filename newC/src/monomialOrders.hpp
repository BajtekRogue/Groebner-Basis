#ifndef MONOMIAL_ORDERS_HPP
#define MONOMIAL_ORDERS_HPP

#include <vector>
#include <memory>
#include <limits>
#include "monomial.hpp"

/**
 *  Abstract class for the monomial ordering. Any derived class must implement the compare method that returns the value of `a < b`
 */
class MonomialOrder {
public:
    virtual ~MonomialOrder() = default;
    virtual bool compare(const Monomial& a, const Monomial& b) const = 0;
};

/**
 * @brief Lexicographic monomial ordering. Constructor receives `permutation` which is the decreasing order of the variables.
 * 
 */
class LexOrder : public MonomialOrder {

public:
    explicit LexOrder(std::vector<char> permutation) 
        : _permutation(std::move(permutation)) {}

    bool compare(const Monomial& a, const Monomial& b) const override {
        for (char var : _permutation) {
            int expA = a.getExponent(var);
            int expB = b.getExponent(var);
            if (expA != expB) {
                return expA < expB;
            }
        }
        return false;
    }

private:
    std::vector<char> _permutation;
};

/**
 * @brief Gradeded lex order. Constructor receives `permutation` which is the decreasing order of the variables it uses to break degree ties.
 * 
 */
class GradedLexOrder : public MonomialOrder {

public:
    explicit GradedLexOrder(std::vector<char> permutation) 
        : _permutation(std::move(permutation)) {}

    bool compare(const Monomial& a, const Monomial& b) const override {
        int degA = a.getDegree();
        int degB = b.getDegree();

        if (degA != degB) {
            return degA < degB;
        }

        for (char var : _permutation) {
            int expA = a.getExponent(var);
            int expB = b.getExponent(var);
            if (expA != expB) {
                return expA < expB;
            }
        }
        return false;
    }

private:
    std::vector<char> _permutation;
};

/**
 * @brief Gradeded revearsed lex order. Constructor receives `permutation` which is the decreasing order of the variables it uses to break degree ties and it then reverses the outcome value.
 * 
 */
class GradedRevLexOrder : public MonomialOrder {

public:
    explicit GradedRevLexOrder(std::vector<char> perm) 
        : _permutation(std::move(perm)) {}

    bool compare(const Monomial& a, const Monomial& b) const override {
        int degA = a.getDegree();
        int degB = b.getDegree();

        if (degA != degB) {
            return degA < degB;
        }

        for (char var : _permutation) {
            int expA = a.getExponent(var);
            int expB = b.getExponent(var);
            if (expA != expB) {
                return expA > expB;
            }
        }
        return true;
    }

private:
    std::vector<char> _permutation;
};

/**
 * @brief Uses dot prodcut with positive real vector and lex order specified by the `permutation` to break ties.
 * 
 */
class WeightedOrder : public MonomialOrder {

public:
    explicit WeightedOrder(std::vector<double> weights, std::vector<char> perm) 
        : _weights(std::move(weights)),  _permutation(std::move(perm)) {
        if (_weights.size() != _permutation.size()) {
            throw std::invalid_argument("Weights and permutation must have the same size");
        }

        for (double w : _weights) {
            if (w < 0.0) {
                throw std::invalid_argument("Weights must be non-negative");
            }
        }
    }

    bool compare(const Monomial& a, const Monomial& b) const override {

        double dotProduct = 0.0;

        for (size_t i = 0; i < _weights.size(); ++i) {
            dotProduct += _weights[i] * (a.getExponent(_permutation[i]) - b.getExponent(_permutation[i]));
        }

        if (std::abs(dotProduct) > std::numeric_limits<double>::epsilon()) {
            return dotProduct < 0.0;
        }

        for (char var : _permutation) {
            int expA = a.getExponent(var);
            int expB = b.getExponent(var);
            if (expA != expB) {
                return expA < expB;
            }
        }
        return false;
    }

private:
    std::vector<double> _weights;
    std::vector<char> _permutation;
};

#endif // MONOMIAL_ORDERS_HPP