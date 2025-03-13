#ifndef SOLVER_HPP
#define SOLVER_HPP

#include "monomial.hpp"
#include "polynomial.hpp"
#include "groebnerBasis.hpp"
#include "monomialOrders.hpp"
#include <variant>
#include "rational.hpp"

/**
 * @brief For a system of polynomial equations `F`, returns the characteristic equations that each variable must satisfy. If the system has no solutions returns the empty map. Requires many calculations of Groebner basis.
 */
template <typename T>
std::map<char, Polynomial<T>> characteristicEquations(const std::vector<Polynomial<T>>& F) {
    
    std::map<char, Polynomial<T>> result;
    std::set<char> varSet;

    for (const auto& f : F) {
        std::vector<char> f_Vars = f.getVariables();
        varSet.insert(f_Vars.begin(), f_Vars.end());
    }

    for (char var : varSet) {
        std::vector<char> newPermutation;
        std::set<char> newVarSet = varSet;
        newVarSet.erase(var);
        newPermutation.insert(newPermutation.end(), newVarSet.begin(), newVarSet.end());

        std::vector<Polynomial<T>> G = calculateGroebnerBasis(F, LexOrder(newPermutation));
        std::vector<Polynomial<T>> H;

        for (const auto& g : G) {
            std::vector<char> g_Vars = g.getVariables();
            if(g_Vars.size() == 1 && g_Vars[0] == var) {
                H.push_back(g);
            }
        }

        if (H.size() == 0) {
            return {};
        } 
        else {
            result[var] = H[0];
        }
    }

    return result;
}

/**
 * @brief Helper function to solve system of polynomial equations
 */
template <typename T>
std::variant<std::string, std::vector<std::map<char, T>>> recursiveSolver(const std::vector<Polynomial<T>>& F, std::function<std::vector<T>(const Polynomial<T>&)> rootFinder) {

    if (F.empty()) {
        return {};
    }

    std::vector<Polynomial<T>> univaratePolynomials;
    std::vector<Polynomial<T>> constantPolynomials;

    for (const auto& f : F) {
        std::vector<char> f_vars = f.getVariables();

        if (f_vars.size() == 1) {
            univaratePolynomials.push_back(f);
        }
        else if (f_vars.size() == 0 && !f.isZeroPolynomial()) {
            constantPolynomials.push_back(f);
        }
        
    }

    if (!constantPolynomials.empty()) {
        return "No solutions found";
    }
    else if (univaratePolynomials.empty()) {
        return "There are infinitely many solutions";
    }

    Polynomial<T> f = univaratePolynomials[0];
    char var = f.getVariables()[0];
    univaratePolynomials.erase(univaratePolynomials.begin());
    std::vector<T> rootsFound = rootFinder(f);

    if (rootsFound.empty()) {
        return "No solutions found";
    }

    std::vector<std::map<char, T>> solutions;

    for (T root : rootsFound) {

        std::map<char, T> cuurentSolution = {{var, root}};
        std::vector<Polynomial<T>> G;

        for (const auto& f : F) {
            try {
                Polynomial<T> g = f.substitute(var, root);
                G.push_back(g);
            }
            catch (const std::invalid_argument& e) {
                G.push_back(f);
            }
        }

        std::vector<Polynomial<T>> H;
        for (const auto& g : G) {
            if (!g.isZeroPolynomial()) {
                H.push_back(g);
            }
        }

        if (H.empty()) {
            solutions.push_back(cuurentSolution);
        }
        else {
            std::variant<std::string, std::vector<std::map<char, T>>> extendedSolution = recursiveSolver(H, rootFinder);

            if (std::holds_alternative<std::string>(extendedSolution)) {
                std::string message = std::get<std::string>(extendedSolution);
                if (message == "No solutions found") {
                    continue;
                }
                else if (message == "There are infinitely many solutions") {
                    return "There are infinitely many solutions";
                }
            } 
            else {
                std::vector<std::map<char, T>> extendedSolutions = std::get<std::vector<std::map<char, T>>>(extendedSolution);

                for (const auto& sol : extendedSolutions) {
                    std::map<char, T> fullSolution = cuurentSolution;
                    fullSolution.insert(sol.begin(), sol.end());
                    solutions.push_back(fullSolution);
                }
            }
        }
    }

    return solutions;
}

template <typename T>
std::vector<T> divisors(T t) {

    if (t == T(0)) {
        return {T(0)};
    }

    std::vector<T> result;

    if (t > T(0)) {

        for (T i = T(1); i <= t; i++) {
            if (t % i == T(0)) {
                result.push_back(i);
                result.push_back(t / i);
            }
        }
        return result;
    }

    for (T i = T(-1); i >= t; i--) {
        if (t % i == T(0)) {
            result.push_back(i);
            result.push_back(t / i);
        }
    }
    return result;
}

/**
 * @brief Returns all rational roots of the polynomial `f`
 */
template <typename T>
std::vector<Rational<T>> findRationalRoots(const Polynomial<Rational<T>>& f) {

    std::vector<T> denominators;
    for (const auto& [monomial, coeff] : f.getCoefficients()) {
        denominators.push_back(coeff.getDenominator());
    }

    T lcm_val = denominators[0];
    for (int i = 1; i < denominators.size(); i++) {
        lcm_val = std::lcm(lcm_val, denominators[i]);
    }

    Polynomial<Rational<T>> g = f * Rational<T>(lcm_val);
    char var = g.getVariables()[0];

    std::map<Monomial, Rational<T>> coefficients = g.getCoefficients();
    Rational<T> constantTerm = coefficients.begin()->second;
    Rational<T> leadingTerm = coefficients.rbegin()->second;

    std::vector<T> P = divisors(constantTerm.getNumerator());
    std::vector<T> Q = divisors(leadingTerm.getNumerator());

    std::set<Rational<T>> candidates;  
    candidates.insert(Rational<T>(0)); 

    for (const T& p : P) {
        for (const T& q : Q) {
            candidates.insert(Rational<T>(p, q));
            candidates.insert(Rational<T>(-p, q));
        }
    }

    std::vector<Rational<T>> roots;
    for (const Rational<T>& r: candidates) {
        if (g.evaluate(std::map<char, Rational<T>>{{var, r}}) == T(0)) {
            roots.push_back(r);
        }
    }
    return roots;
}


/**
 * @brief Solve system of polynomial equations. If there are no solutions in the field returns the empty vector and if there are infinitly many solutions or no solutions in any field extension a `runtime_error` is thrown
 * 
 * @tparam `T` Field of solutions 
 * @param `F` System to solve 
 * @param `rootFinder` Function used to compute roots of a one variable polynomials
 * @return `std::vector<std::map<char, T>>` vector of key value solutions 
 */
template <typename T>
std::vector<std::map<char, T>> solveSystem(const std::vector<Polynomial<T>>& F, std::function<std::vector<T>(const Polynomial<T>&)> rootFinder){

    std::set<char> varSet;
    for (const auto& f : F) {
        std::vector<char> f_vars = f.getVariables();
        varSet.insert(f_vars.begin(), f_vars.end());
    }

    std::vector<char> variables;
    variables.insert(variables.begin(), varSet.begin(), varSet.end());

    std::vector<Polynomial<T>> G = calculateGroebnerBasis(F, LexOrder(variables));

    if (G.size() == 1 && G[0] == T(1)) {
        throw std::runtime_error("No solution exist in any field extension");
    }

    std::variant<std::string, std::vector<std::map<char, T>>> solutions = recursiveSolver(G, rootFinder);

    if (std::holds_alternative<std::string>(solutions)) {
        std::string message = std::get<std::string>(solutions);

        if (message == "There are infinitely many solutions") {
            throw std::runtime_error("There are infinitely many solutions");
        }
        else if (message == "No solutions found") {
            return {};
        }
    }

    std::vector<std::map<char, T>> X = std::get<std::vector<std::map<char, T>>>(solutions);
    return X;
}

/**
 * @brief Solve system of polynomial equations. If there are no solutions in the field returns the empty vector and if there are infinitly many solutions or no solutions in any field extension a `runtime_error` is thrown
 * 
 * @tparam `T` Field of solutions 
 * @param `F` System to solve 
 * @param `rootFinder` Function used to compute roots of a one variable polynomials
 * @return `std::vector<std::map<char, T>>` vector of key value solutions 
 */
template <typename T>
std::vector<std::map<char, T>> solveSystem(const std::vector<Polynomial<T>>& F, std::vector<T> (*rootFinder)(const Polynomial<T>&)) {
    return solveSystem(F, std::function<std::vector<T>(const Polynomial<T>&)>(rootFinder));
}


/**
 * @brief Solve system of polynomial equations over rational numbers. If there are no solutions in the rational numbers returns the empty vector and if there are infinitly many solutions or no solutions in any field extension a `runtime_error` is thrown
 * 
 * @tparam `T` Intger type used
 * @param `F` System to solve 
 * @return `std::vector<std::map<char, T>>` vector of key value solutions 
 */
template <typename T>
std::vector<std::map<char, Rational<T>>> solveSystem(const std::vector<Polynomial<Rational<T>>>& F) {
    return solveSystem(F, findRationalRoots);
}
#endif // SOLVER_HPP