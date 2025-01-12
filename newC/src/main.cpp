#include <iostream>
#include <vector>
#include <algorithm>
#include "monomial.hpp"
#include "monomialOrders.hpp"
#include "rational.hpp"
#include "polynomial.hpp"
#include "polynomialMethods.hpp"

int main() {

    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    auto z = defineVariable<Rational<int>>('z');
    auto a = defineVariable<Rational<int>>('a');
    auto b = defineVariable<Rational<int>>('b');
    auto c = defineVariable<Rational<int>>('c');
    auto d = defineVariable<Rational<int>>('d');

    auto f1 = (2 + a) * c;
    auto f2 = (2 + a) * d;
    auto f3 = b;
    auto trig1 = (a^2) + (b^2) - 1;
    auto trig2 = (c^2) + (d^2) - 1;
    std::vector<Polynomial<Rational<int>>*> F = {&f1, &f2, &f3, &trig1, &trig2};

    std::vector<Polynomial<Rational<int>>> G = getGroebnerBasis(F, LexOrder({'a', 'b', 'c', 'd', 'x', 'y', 'z'}));

    std::cout << "Groebner basis G:" << std::endl;
    for (const auto& g : G) {
        std::cout << g << std::endl;
    }
    return 0;
}
