#ifndef IDEAL_HPP
#define IDEAL_HPP

#include <iostream>
#include "groebnerBasis.hpp"
#include "monomialOrders.hpp"

/**
 * @brief Represents an ideal of a polynomial ring over a field `T`. Stores a list of generators.
 * 
 *  @tparam `T` coefficient type, must form a field 
 */
template <typename T>
class Ideal {

public:
    Ideal() {_generators.push_back(Polynomial<T>());}
    Ideal(const std::vector<Polynomial<T>> generators) : _generators(generators) {
        if (_generators.empty()) {
            _generators.push_back(Polynomial<T>());
        }

        std::set<char> variablesSet;
        for (const auto& generator : _generators) {
            std::vector<char> generatorVariables = generator.getVariables();
            variablesSet.insert(generatorVariables.begin(), generatorVariables.end());
        }
        _variables = std::vector<char>(variablesSet.begin(), variablesSet.end());
    }
    Ideal(const Ideal<T>& I) : _generators(I.getGenerators()), _variables(I.getVariables()) {}
    
    std::vector<char> getVariables() const {
        return _variables;
    }

    std::vector<Polynomial<T>> getGenerators() const {
        return _generators;
    }

    /**
     * Gets the current Groebnar basis of the ideal. If it is not already calculated, it calculates it using graded reverse lexicographic order.
     */
    std::vector<Polynomial<T>> getGroebnerBasis()  {
        if (_groebnerBasis.empty()) {
            _groebnerBasis = calculateGroebnerBasis(_generators, GradedRevLexOrder(_variables));
        }
        return _groebnerBasis;
    }

    /**
     * Calculates Groebnar basis of the ideal using lexicographic order determined byt `permutation`.
     */
    std::vector<Polynomial<T>> getGroebnerBasis(std::vector<char> permutation) {
        _groebnerBasis = calculateGroebnerBasis(_generators, LexOrder(permutation));
        return _groebnerBasis;
    }

    Ideal<T>& operator=(const Ideal<T>& other) {
        if (this != &other) {
            _generators = other._generators;
            _groebnerBasis = other._groebnerBasis;
            _variables = other._variables;
        }
        return *this;
    }

    Ideal<T> operator+(const Ideal<T>& other) const {
        return Ideal::algebraicSum(*this, other);
    }

    Ideal<T> operator+=(const Ideal<T>& other) {
        *this = *this + other;
        return *this;
    }

    Ideal<T> operator-(const Ideal<T>& other) const {
        return *this + other;
    }

    Ideal<T> operator-=(const Ideal<T>& other) {
        *this = *this + other;
        return *this;
    }

    Ideal<T> operator*(const Ideal<T>& other) const {
        return Ideal::algebraicProduct(*this, other);
    }

    Ideal<T> operator*=(const Ideal<T>& other) {
        *this = *this * other;
        return *this;
    }

    Ideal<T> operator+() const {
        return *this;
    }

    Ideal<T> operator-() const {
        return *this;
    }

    bool operator==(const Ideal<T>& other) const {
        if (_groebnerBasis.empty()) {
            _groebnerBasis = getGroebnerBasis();
        }
        if (other._groebnerBasis.empty()) {
            other._groebnerBasis = other.getGroebnerBasis();
        }
        std::set<Polynomial<T>> groebnerBasisSet(_groebnerBasis.begin(), _groebnerBasis.end());
        std::set<Polynomial<T>> otherGroebnerBasisSet(other._groebnerBasis.begin(), other._groebnerBasis.end());
        return groebnerBasisSet == otherGroebnerBasisSet;
    }

    bool operator!=(const Ideal<T>& other) const {
        return !(*this == other);
    }

    bool operator<(const Ideal<T>& other) const {
        return !(*this >= other);
    }

    bool operator>(const Ideal<T>& other) const {
        return !(*this <= other);
    }

    bool operator<=(const Ideal<T>& other) const {
        return Ideal::isSubset(*this, other);
    }

    bool operator>=(const Ideal<T>& other) const {
        return other <= *this;
    }

    friend std::ostream& operator<<(std::ostream& os, const Ideal<T>& I) {
        os << I.toString();
        return os;
    }

    std::string toString() const {
        std::ostringstream oss;
        oss << "<";
        for (const auto& generator : _generators) {
            oss << generator.toString() << ", ";
        }
        if (!_generators.empty()) {
            oss.seekp(-2, std::ios_base::end);
        }
        oss << ">";
        return oss.str();
    }
    
    /**
     * Returns `true` if `f` is in the ideal. Requires calculation of Groebner basis.
     */
    bool isInIdeal(const Polynomial<T>& f) const {
        if (_groebnerBasis.empty()) {
            _groebnerBasis = getGroebnerBasis();
        }
        auto [_, r] = polynomialReduce(f, _groebnerBasis, GradedRevLexOrder(_variables));
        return r.isZeroPolynomial();
    }

    /**
     * Returns true if `I` is a subset of `J`, false otherwise. Requires calculation of Groebner basis for `J` ideal.
     */
    static bool isSubset(Ideal<T>& I, Ideal<T>& J) {
        for (const auto& generator : I.getGenerators()) {
            if (!J.isInIdeal(generator)) {
                return false;
            }
        }
        return true;
    }

    /**
     * Calculates intersection of ideal `I` and `J`. Requires calculation of Groebner in the proccess.
     */
    static Ideal<T> intersection(Ideal<T> I, Ideal<T> J) {
        Polynomial<T> t({{Monomial({{'\n', 1}}) , T(1)}});
        Polynomial<T> s = T(1) - t;
        
        std::vector<Polynomial<T>> generators_I;
        for (const auto& generator : I.getGenerators()) {
            generators_I.push_back(generator * t);
        }

        std::vector<Polynomial<T>> generators_J;
        for (const auto& generator : J.getGenerators()) {
            generators_J.push_back(generator * s);
        }

        Ideal<T> K = I + J;

        std::vector<char> variables_I = I.getVariables();
        std::vector<char> variables_J = J.getVariables();
        std::set<char> variablesSet(variables_I.begin(), variables_I.end());
        variablesSet.insert(variables_J.begin(), variables_J.end());
        std::vector<char> variables(variablesSet.begin(), variablesSet.end());
        std::vector<char> permutation = {'\n'};
        permutation.insert(permutation.end(), variables.begin(), variables.end());

        std::vector<Polynomial<T>> G = K.getGroebnerBasis(permutation);
        Ideal intersectionIdeal = Ideal::eliminationIdeal(G, variables);
        return intersectionIdeal;
    }

    /**
     * Calculates the elimination ideal of the ideal `I` and keeps only the polynomial with `variables` as variables.
     */
    static Ideal<T> eliminationIdeal(const std::vector<Polynomial<T>>& F, const std::vector<char>& variables) {

        std::set<char> variablesSet(variables.begin(), variables.end());
        std::vector<Polynomial<T>> result;

        for (const auto& f : F) {

            std::vector<char> f_Variables = f.getVariables();
            std::set<char> f_VariablesSet(f_Variables.begin(), f_Variables.end());

            if (std::includes(variablesSet.begin(), variablesSet.end(), f_VariablesSet.begin(), f_VariablesSet.end())) {
                result.push_back(f);
            }
        }

        return Ideal<T>(result);
    }

    /**
     * Calculates `I + J`
     */
    static Ideal<T> algebraicSum(const Ideal<T>& I, const Ideal<T>& J) {
        std::vector<Polynomial<T>> generators;
        std::vector<Polynomial<T>> generators_I = I.getGenerators();
        std::vector<Polynomial<T>> generators_J = J.getGenerators();
        generators.insert(generators.end(), generators_I.begin(), generators_I.end());
        generators.insert(generators.end(), generators_J.begin(), generators_J.end());
        return Ideal(generators);
    }

    /**
     * Calculates `I * J`
     */
    static Ideal<T> algebraicProduct(const Ideal<T>& I, const Ideal<T>& J) {
        std::vector<Polynomial<T>> generators;
        for (const auto& f : I.getGenerators()) {
            for (const auto& g : J.getGenerators()) {
                generators.push_back(f * g);
            }
        }
        return Ideal<T>(generators);
    }

private:
    std::vector<Polynomial<T>> _generators;
    std::vector<Polynomial<T>> _groebnerBasis;
    std::vector<char> _variables;
};


#endif // IDEAL_HPP