#ifndef UTILITY_HPP
#define UTILITY_HPP

#include "monomial.hpp"
#include "polynomial.hpp"
#include "ideal.hpp"
#include "groebnerBasis.hpp"
#include "monomialOrders.hpp"

/**
 * @brief Returns a polynomial `var ^ exp` over field `T`. Default value of `exp` is `1`.
 * @tparam `T` resulting polynomial field
 */
template <typename T>
Polynomial<T> defineVariable(char var, int exp = 1) {
    Monomial monomial({{var, exp}});
    return Polynomial<T>({{monomial, T(1)}});
}

/**
 * @brief Takes map of variables and their corresponding parametirc equations and returns the implicitization of the curve they form. Requires calculation of Groebner basis.
 * @tparam `T` field of calculation
 * @param parametricEquations 
 * @return `std::vector<Polynomial<T>>` implicitization of the curve (might be of size 1) 
 */
template <typename T>
std::vector<Polynomial<T>> polynomialImplicitization(const std::map<char, Polynomial<T>>& parametricEquations) {

    std::set<char> parameters;
    std::vector<char> variables;

    for (const auto& [var, f] : parametricEquations) {
        std::vector<char> f_Vars = f.getVariables();
        parameters.insert(f_Vars.begin(), f_Vars.end());
        variables.push_back(var);
    }

    std::vector<char> parameters_ = std::vector<char>(parameters.begin(), parameters.end());
    std::vector<char> permutation = parameters_;
    permutation.insert(permutation.end(), variables.begin(), variables.end());

    std::vector<Polynomial<T>> generators;
    for (const auto& [var, f] : parametricEquations) {
        generators.push_back(f - defineVariable<T>(var));
    }

    std::vector<Polynomial<T>> G = calculateGroebnerBasis(generators, LexOrder(permutation));
    Ideal<T> I = Ideal<T>::eliminationIdeal(G, variables);
    return I.getGenerators();
}

/**
 * @brief Takes map of variables and their corresponding parametirc rational equations and returns the implicitization of the curve they form. Requires calculation of Groebner basis. The map strucutre is as follows: `{{'x', {f, g}}}` means that the equation is `x = f / g`.
 * @tparam `T` field of calculation
 * @param parametricEquations 
 * @return `std::vector<Polynomial<T>>` implicitization of the curve (might be of size 1) 
 */
template <typename T>
std::vector<Polynomial<T>> rationalImplicitization(const std::map<char, std::pair<Polynomial<T>, Polynomial<T>>>& parametricEquations) {

    std::set<char> parameters;
    std::vector<char> variables;

    for (const auto& [var, eq] : parametricEquations) {
        const Polynomial<T>& f = eq.first;
        const Polynomial<T>& g = eq.second;

        std::vector<char> f_Vars = f.getVariables();
        std::vector<char> g_Vars = g.getVariables();
        parameters.insert(f_Vars.begin(), f_Vars.end());
        parameters.insert(g_Vars.begin(), g_Vars.end());
        variables.push_back(var);
    }

    std::vector<char> parameters_ = std::vector<char>(parameters.begin(), parameters.end());
    std::vector<char> permutation = parameters_;
    permutation.insert(permutation.end(), variables.begin(), variables.end());
    permutation.insert(permutation.begin(), '\n');  

    std::vector<Polynomial<T>> generators;
    for (const auto& [var, eq] : parametricEquations) {
        const Polynomial<T>& f = eq.first;
        const Polynomial<T>& g = eq.second;

        generators.push_back(f - g * defineVariable<T>(var));
    }

    Polynomial<T> denominator = defineVariable<T>('\n');
    for (const auto& [var, eq] : parametricEquations) {
        const Polynomial<T>& g = eq.second;
        denominator *= g;
    }
    denominator = 1 - denominator;
    generators.push_back(denominator);

    std::vector<Polynomial<T>> G = calculateGroebnerBasis(generators, LexOrder(permutation));
    Ideal<T> I = Ideal<T>::eliminationIdeal(G, variables);
    return I.getGenerators();
}

/**
 * @brief lcm(p) = p
 */
template <typename T>
Polynomial<T> lcm(const Polynomial<T>& p) {
    return p;
}

/**
 * @brief lcm of two polynomials. Require calculation of Groebner basis.
 */
template <typename T>
Polynomial<T> lcm(const Polynomial<T>& f, const Polynomial<T>& g) {
    std::vector<char> variables;
    std::vector<char> f_Vars = f.getVariables();
    std::vector<char> g_Vars = g.getVariables();
    variables.insert(variables.end(), f_Vars.begin(), f_Vars.end());
    variables.insert(variables.end(), g_Vars.begin(), g_Vars.end());

    std::set<char> variableSet(variables.begin(), variables.end());
    variables = std::vector<char>(variableSet.begin(), variableSet.end());

    Polynomial<T> t = defineVariable<T>('\n');
    variables.insert(variables.begin(), '\n');

    Polynomial<T> p = f * t;
    Polynomial<T> q = g * (1 - t);

    std::vector<Polynomial<T>> G = calculateGroebnerBasis(std::vector<Polynomial<T>>{p, q}, LexOrder(variables));
    variables.erase(variables.begin());

    Ideal<T> I = Ideal<T>::eliminationIdeal(G, variables);
    std::vector<Polynomial<T>> generatorsOfIdeal = I.getGenerators();
    return generatorsOfIdeal[0];
}

/**
 * @brief lcm of polynomials. Require calculation of Groebner basis.
 */
template <typename T, typename... Args>
Polynomial<T> lcm(const Polynomial<T>& first, const Polynomial<T>& second, Args... rest) {


    Polynomial<T> partial = lcm(first, second);
    
    if constexpr (sizeof...(rest) == 0) {
        return partial;
    } 

    Polynomial<T> result = lcm(partial, rest...); 
    T normalizedCoefficient = result.leadingCoefficient(GradedLexOrder(result.getVariables()));
    return result * (T(1) / normalizedCoefficient);
    
}

/**
 * @brief lcm of any polynomials. Require calculation of Groebner basis.
 */
template <typename T>
Polynomial<T> lcm(std::vector<Polynomial<T>> polynomials) {
    Polynomial<T> result = polynomials[0];
    for (int i = 1; i < polynomials.size(); i++) {
        result = lcm(result, polynomials[i]);
    }
    T normalizedCoefficient = result.leadingCoefficient(GradedLexOrder(result.getVariables()));
    return result * (T(1) / normalizedCoefficient);
}

/**
 * @brief gcd(p) = p
 */
template <typename T>
Polynomial<T> gcd(const Polynomial<T>& p) {
    return p;
}

/**
 * @brief gcd of two polynomials. Require calculation of Groebner basis.
 */
template <typename T>
Polynomial<T> gcd(const Polynomial<T>& f, const Polynomial<T>& g) {
    std::vector<char> variables;
    std::vector<char> f_Vars = f.getVariables();
    std::vector<char> g_Vars = g.getVariables();
    variables.insert(variables.end(), f_Vars.begin(), f_Vars.end());
    variables.insert(variables.end(), g_Vars.begin(), g_Vars.end());

    std::set<char> variableSet(variables.begin(), variables.end());
    variables = std::vector<char>(variableSet.begin(), variableSet.end());
    Polynomial<T> l = lcm(f, g);
    auto [Q, _] = polynomialReduce(f * g, {l}, LexOrder(variables));
    Polynomial<T> result = Q[0];
    T normalizedCoefficient = result.leadingCoefficient(GradedLexOrder(result.getVariables()));
    return result * (T(1) / normalizedCoefficient);
}

/**
 * @brief gcd of polynomials. Require calculation of Groebner basis.
 */
template <typename T, typename... Args>
Polynomial<T> gcd(const Polynomial<T>& first, const Polynomial<T>& second, Args... rest) {

    Polynomial<T> partial = gcd(first, second);
    
    if constexpr (sizeof...(rest) == 0) {
        return partial;
    } 

    Polynomial<T> result = gcd(partial, rest...); 
    T normalizedCoefficient = result.leadingCoefficient(GradedLexOrder(result.getVariables()));
    return result * (T(1) / normalizedCoefficient);
}

/**
 * @brief gcd of polynomials. Require calculation of Groebner basis.
 */
template <typename T>
Polynomial<T> gcd(std::vector<Polynomial<T>> polynomials) {
    Polynomial<T> result = polynomials[0];
    for (int i = 1; i < polynomials.size(); i++) {
        result = gcd(result, polynomials[i]);
    }
    T normalizedCoefficient = result.leadingCoefficient(GradedLexOrder(result.getVariables()));
    return result * (T(1) / normalizedCoefficient);
}



/* ADD SOLVER AND BE DONE WITH THIS*/






#endif // UTILITY_HPP