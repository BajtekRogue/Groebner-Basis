#ifndef GROEBNER_BASIS_HPP
#define GROEBNER_BASIS_HPP

#include "monomial.hpp"
#include "polynomial.hpp"
#include "monomialOrders.hpp"

/**
 * @brief Division algorithm for multivariable polynomials. Size of quotient vector is equal to the size of the divisor vector. Note that the result depends in general on the order of elements in `G` as well as the monomial order choosen.
 * 
 * @tparam `T` field of coefficients
 * @param f Polynomial to be reduced
 * @param G Vector of polynomials to divide by
 * @param order Monomial order used to determine the leading term
 * @return `std::pair<std::vector<Polynomial<T>>, Polynomial<T>>` where the first element is the vector of quotients and the second element is the remainder 
 */
template <typename T>
std::pair<std::vector<Polynomial<T>>, Polynomial<T>> polynomialReduce(const Polynomial<T>& f, const std::vector<Polynomial<T>>& G, const MonomialOrder& order) {
    
    const int n = G.size();
    Polynomial<T> p(f);
    Polynomial<T> r;
    std::vector<Polynomial<T>> Q(n);

    // Reduction process
    while (!p.isZeroPolynomial()) {

        const Monomial& p_leadingMonomial = p.leadingMonomial(order);
        const T p_leadingCoefficient = p.leadingCoefficient(order);
        bool somethingDivided = false;

        for (int i = 0; i < n; i++) {

            const Polynomial<T>& g = G[i];
            const Monomial& g_leadingMonomial = g.leadingMonomial(order);
            T g_leadingCoefficient = g.leadingCoefficient(order);

            // Check if something divides the leading term of p
            if (Monomial::divides(p_leadingMonomial, g_leadingMonomial)) {

                Monomial divisionMonomial = p_leadingMonomial / g_leadingMonomial;
                T divisionCoefficient = p_leadingCoefficient / g_leadingCoefficient;

                Polynomial<T> divisionMonomialPolynomial({{divisionMonomial, divisionCoefficient}});
                p -= divisionMonomialPolynomial * g;
                Q[i] += divisionMonomialPolynomial;
                somethingDivided = true;

                break;
            }
        }

        // Nothing divided so reduce p and update r
        if (!somethingDivided) {
            Polynomial<T> divisionMonomialPolynomial({{p_leadingMonomial, p_leadingCoefficient}});
            p -= divisionMonomialPolynomial;
            r += divisionMonomialPolynomial;
        }
    }

    return {Q, r};
}

/**
 * Calculates `S(f, g) = lcm(LM(f), LM(g)) * (f / LT(f)  - g / LT(g))`
 */
template <typename T>
Polynomial<T> syzygy(const Polynomial<T>& f, const Polynomial<T>& g, const MonomialOrder& order) {

    const Monomial& f_leadingMonomial = f.leadingMonomial(order);
    T f_leadingCoefficient = f.leadingCoefficient(order);

    const Monomial& g_leadingMonomial = g.leadingMonomial(order);
    T g_leadingCoefficient = g.leadingCoefficient(order);

    Monomial lcm = Monomial::lcm(f_leadingMonomial, g_leadingMonomial);
    Polynomial<T> u({{lcm / f_leadingMonomial, T(1) / f_leadingCoefficient}});
    Polynomial<T> v({{lcm / g_leadingMonomial, T(1) / g_leadingCoefficient}});

    return u * f - v * g;
}

/**
 * Checks if monomials satisfy the lcm criterion in Buchberger's algorithm. That occurs when they are relativly prime and so `lcm(a, b) = a * b`
 */ 
bool lcmCriterion(const Monomial& a, const Monomial& b) {
    return Monomial::lcm(a, b) == a * b;
}

/**
 * Checks if monomials satisfy the chain criterion in Buchberger's algorithm. That occurs when there is a third monomial that divides the lcm of the two monomials
 */
bool chainCriterion(const Monomial& a, const Monomial& b, const std::vector<Monomial>& remainingMonomials) {
    for (const auto& monomial : remainingMonomials) {
        if (Monomial::divides(Monomial::lcm(a, b), monomial)) {
            return true;
        }
    }
    return false;
}

/**
 * @brief Extends set `F` to a Groebner basis using Buchberger's algorithm
 * 
 * @tparam `T` field of coefficients 
 * @param F set of polynomials
 * @param order Monomial order used to determine the leading term
 * @return `std::vector<Polynomial<T>>` Groebner basis 
 */
template <typename T>
std::vector<Polynomial<T>> extendToGroebnerBasis(const std::vector<Polynomial<T>>& F, const MonomialOrder& order) {

    std::vector<Polynomial<T>> G = F;

    while (true) {

        const int n = G.size();
        std::vector<Polynomial<T>> H = G;
        bool somethingAdded = false;

        // Iterate over all pairs (i, j) in G
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {

                const Monomial& i_monomial = G[i].leadingMonomial(order);
                const Monomial& j_monomial = G[j].leadingMonomial(order);

                // First check lcmCriterion and chainCriterion to avoid doing division
                if (lcmCriterion(i_monomial, j_monomial)) {
                    continue;
                }

                std::vector<Monomial> remainingMonomials(n - (j + 1));
                for (int k = j + 1; k < n; k++) {
                    remainingMonomials[k - (j + 1)] = G[k].leadingMonomial(order);
                }

                if (chainCriterion(i_monomial, j_monomial, remainingMonomials)) {
                    continue;
                }

                // Need to do division. If r is not 0, add it to H
                Polynomial<T> s = syzygy(G[i], G[j], order);
                auto [_, r] = polynomialReduce(s, G, order);

                if (!r.isZeroPolynomial()) {
                    H.push_back(r);
                    somethingAdded = true;
                }

            }
        }

        // If something was added, update G and continue, otherwise return
        if (!somethingAdded) {
            return H;
        }
        else {
            G = H;
        }
    }
}

/**
 * @brief Reduces a Groebner basis
 * 
 * @tparam `T` field of coefficients 
 * @param G Groebner basis to reduce
 * @param order Monomial order used to determine the leading term 
 * @param normalizedCoefficients if `true`, the coefficients of the polynomials in the reduced Groebner basis will be normalized
 * @return `std::vector<Polynomial<T>>` the reduced Groebner basis 
 */
template <typename T>
std::vector<Polynomial<T>> reduceGroebnerBasis(const std::vector<Polynomial<T>>& G, const MonomialOrder& order, bool normalizedCoefficients) {

    std::vector<Polynomial<T>> H = G;

    // First pass: Remove elements that are in the leading terms ideal
    for (auto& g : G) {

        auto it = std::find(H.begin(), H.end(), g);
        if (it != H.end()) {
            H.erase(it);
        }
        else {
            continue;
        }

        bool inLeadingTermsIdeal = false;
        // If g is in the leading terms ideal generate by other polynomials we don't need it
        for (const auto& h : H) {
            if (Monomial::divides(g.leadingMonomial(order), h.leadingMonomial(order))) {
                inLeadingTermsIdeal = true;
                break;
            }
        }

        if (!inLeadingTermsIdeal) {
            H.push_back(g);
        }
    }

    const int currentSize = H.size();
    bool somethingReduced = false;

    // Second pass: Perform reductions
    while (!somethingReduced) {

        somethingReduced = true;
        // Reduce each polynomial in the basis by the others to simplify it
        for (int i = 0; i < currentSize; i++) {

            std::vector<Polynomial<T>> F = H;
            F.erase(F.begin() + i); 
            auto [_, r] = polynomialReduce(H[i], F, order);

            if (!r.isZeroPolynomial() && H[i] != r) {
                H[i] = r;
                somethingReduced = false;
            } 
        }
    }

    // Third [optional] pass: Normalize coefficients
    if (normalizedCoefficients) {
        for (auto& h : H) {
            T leadingCoefficient = h.leadingCoefficient(order);
            h *= T(1) / leadingCoefficient;
        }
    }
    
    return H;
}

/**
 * @brief Calculates the reduced Groebner basis of a set of polynomials
 * 
 * @tparam `T` field of coefficients 
 * @param F set of polynomials 
 * @param order Monomial order used to determine the leading term 
 * @param normalizedCoefficients if `true`, the coefficients of the polynomials in the reduced Groebner basis will be normalized 
 * @return `std::vector<Polynomial<T>>` the reduced Groebner basis 
 */
template <typename T>
std::vector<Polynomial<T>> calculateGroebnerBasis(const std::vector<Polynomial<T>>& F, const MonomialOrder& order, bool normalizedCoefficients = true) {
    std::vector<Polynomial<T>> G = extendToGroebnerBasis(F, order);
    G = reduceGroebnerBasis(G, order, normalizedCoefficients);
    return G;
}   

#endif // GROEBNER_BASIS_HPP
