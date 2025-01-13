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
#include <span>

int main() {
    using Rational = double;

    auto x = defineVariable<Rational>('x');
    auto y = defineVariable<Rational>('y');
    auto f1 = x*x - y *y;
    auto f2 = (x -y) * (x*x*x + y*y*5+4*x);
    auto f3 = (x-y) * (x*x*x+7);
    auto l = lcm(f1, f3, f2);
    std::cout << "lcm: " << l << std::endl;

    return 0;
}
