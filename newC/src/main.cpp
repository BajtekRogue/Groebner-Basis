#include <iostream>
#include <vector>
#include <algorithm>
#include "monomial.hpp"
#include "monomialOrders.hpp"
#include "rational.hpp"
#include "polynomial.hpp"
#include "groebnerBasis.hpp"
#include "ideal.hpp"
#include "utility.hpp"
#include "solver.hpp"
#include <span>


int main() {
    using Rational = Rational<int>;

    auto x = defineVariable<Rational>('x');
    auto y = defineVariable<Rational>('y');
    auto z = defineVariable<Rational>('z');

    auto f1 = x + y + z - 9;
    auto f2 = (x^2) + (y^2) + (z^2) - 35;
    auto f3 = (x^3) + (y^3) + (z^3) - 153;
    auto f4 = x*y*z-151;


    std::vector<Polynomial<Rational>> F = {f1, f2, f3, f4};
    std::vector<std::map<char, Rational>> X = solveSystem(F);

    for (const auto& solution : X) {
        for (const auto& [var, value] : solution) {
            std::cout << var << " = " << value << " ";
        }
        std::cout << std::endl;
    }
    return 0;
}
