#ifndef POLYNOMIAL_METHODS_HPP
#define POLYNOMIAL_METHODS_HPP

#include "monomial.hpp"
#include "rational.hpp"
#include "polynomial.hpp"
#include "monomialOrders.hpp"


template <typename T>
Polynomial<T> defineVariable(char var, int exp = 1) {
    Monomial monomial({{var, exp}});
    return Polynomial<T>({{monomial, T(1)}});
}

template <typename T>
std::pair<std::vector<Polynomial<T>>, Polynomial<T>> polynomialReduce(const Polynomial<T>& f, const std::vector<Polynomial<T>*>& G, const MonomialOrder& order) {
    
    const int n = G.size();
    Polynomial<T> p = Polynomial<T>(f, false);
    Polynomial<T> r = Polynomial<T>();
    std::vector<Polynomial<T>> Q(n, Polynomial<T>());

    // Reduction process
    while (!p.isZeroPolynomial()) {

        const Monomial& p_leadingMonomial = p.leadingMonomial(order);
        const T p_leadingCoefficient = p.leadingCoefficient(order);
        bool somethingDivided = false;

        for (int i = 0; i < n; i++) {

            const Polynomial<T>* g = G[i];
            try {

                const Monomial& g_leadingMonomial = g->leadingMonomial(order);
                T g_leadingCoefficient = g->leadingCoefficient(order);
                
                Monomial divisionMonomial = p_leadingMonomial / g_leadingMonomial;
                T divisionCoefficient = p_leadingCoefficient / g_leadingCoefficient;

                Polynomial<T> divisionMonomialPolynomial({{divisionMonomial, divisionCoefficient}});
                p -= divisionMonomialPolynomial * (*g);
                Q[i] += divisionMonomialPolynomial;
                somethingDivided = true;

                break;
            } 
            catch (const std::invalid_argument&) {
                continue; // This means the divison wasn't possible as / operator throws an exception in Monomial class
            }
        }

        if (!somethingDivided) {
            p -= Polynomial<T>({{p_leadingMonomial, p_leadingCoefficient}});
            r += Polynomial<T>({{p_leadingMonomial, p_leadingCoefficient}});
        }
    }
    return {Q, r};
}


template <typename T>
Polynomial<T> syzygy(const Polynomial<T>& f, const Polynomial<T>& g, const MonomialOrder& order) {
    const Monomial& f_leadingMonomial = f.leadingMonomial(order);
    T f_leadingCoefficient = f.leadingCoefficient(order);
    const Monomial& g_leadingMonomial = g.leadingMonomial(order);
    T g_leadingCoefficient = g.leadingCoefficient(order);
    Monomial lcm = Monomial::lcm(f_leadingMonomial, g_leadingMonomial);
    Polynomial<T> u = Polynomial<T>({{lcm / f_leadingMonomial, T(1) / f_leadingCoefficient}});
    Polynomial<T> v = Polynomial<T>({{lcm / g_leadingMonomial, T(1) / g_leadingCoefficient}});
    return u * f - v * g;
}

bool lcmCriterion(const Monomial& a, const Monomial& b) {
    return Monomial::lcm(a, b) == a * b;
}

bool chainCriterion(const Monomial& a, const Monomial& b, const std::vector<Monomial>& remainingMonomials) {
    for (const auto& monomial : remainingMonomials) {
        if (Monomial::divides(Monomial::lcm(a, b), monomial)) {
            return true;
        }
    }
    return false;
}

template <typename T>
std::vector<Polynomial<T>*> extendToGroebnerBasis(const std::vector<Polynomial<T>*>& F, const MonomialOrder& order) {

    std::vector<Polynomial<T>*> G = F;

    while (true) {
        std::vector<Polynomial<T>*> H = G;
        bool somethingAdded = false;

        for (int i = 0; i < G.size(); i++) {
            for (int j = i + 1; j < G.size(); j++) {
                
                const Monomial& i_monomial = G[i]->leadingMonomial(order);
                const Monomial& j_monomial = G[j]->leadingMonomial(order);

                if (lcmCriterion(i_monomial, j_monomial)) {
                    continue;
                }

                std::vector<Monomial> remainingMonomials(G.size() - (j + 1));
                for (int k = j + 1; k < G.size(); k++) {
                    remainingMonomials[k - (j + 1)] = G[k]->leadingMonomial(order);
                }

                if (chainCriterion(i_monomial, j_monomial, remainingMonomials)) {
                    continue;
                }

                auto [_, r] = polynomialReduce(syzygy(*G[i], *G[j], order), G, order);

                if (!r.isZeroPolynomial()) {
                    H.push_back(new Polynomial<T>(r));
                    somethingAdded = true;
                }

            }
        }

        if (!somethingAdded) {
            return H;
        }
        else {
            G = std::move(H);
            std::cout << "Groebner basis size: " << G.size() << std::endl;
        }
    }
}

template <typename T>
std::vector<Polynomial<T>*> reduceGroebnerBasis(const std::vector<Polynomial<T>*>& G, const MonomialOrder& order, bool normalizedCoefficients) {

    std::vector<Polynomial<T>*> H = G;

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

        for (const auto& h : H) {
            if (Monomial::divides(g->leadingMonomial(order), h->leadingMonomial(order))) {
                inLeadingTermsIdeal = true;
                break;
            }
        }

        if (!inLeadingTermsIdeal) {
            H.push_back(new Polynomial<T>(*g));
        }
    }

    // Clear G
    // for (auto* g : G) {
    //     if (std::find(H.begin(), H.end(), g) == H.end()) {
    //         delete g;
    //     }
    // }

    const int originalSize = H.size();
    bool somethingReduced = false;

    // Second pass: Perform reductions
    while (!somethingReduced) {

        somethingReduced = true;

        for (int i = 0; i < H.size(); i++) {

            std::vector<Polynomial<T>*> F = H;
            F.erase(F.begin() + i); 
            auto [_, r] = polynomialReduce(*H[i], F, order);

            if (!r.isZeroPolynomial() && *H[i] != r) {
                delete H[i];
                H[i] = new Polynomial<T>(r);
                somethingReduced = false;
            } 
        }
    }

    // Third [optional] pass: Normalize coefficients
    if (normalizedCoefficients) {
        for (auto* h : H) {
            T leadingCoefficient = h->leadingCoefficient(order);
            *h *= T(1) / leadingCoefficient;
        }
    }
    
    return H;
}


template <typename T>
std::vector<Polynomial<T>> getGroebnerBasis(const std::vector<Polynomial<T>*>& F, const MonomialOrder& order, bool normalizedCoefficients = true) {
    std::vector<Polynomial<T>*> G = extendToGroebnerBasis(F, order);
    G = reduceGroebnerBasis(G, order, normalizedCoefficients);
    std::vector<Polynomial<T>> H;
    H.reserve(G.size());
    for (const auto* g : G) {
        H.push_back(*g);
        delete g; 
    }
    return H;
}   

#endif // POLYNOMIAL_METHODS_HPP
