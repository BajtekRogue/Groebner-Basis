#include <gtest/gtest.h>
#include "polynomial.hpp"
#include "groebnerBasis.hpp"
#include "monomialOrders.hpp"
#include "utility.hpp"
#include "rational.hpp"
#include <vector>

TEST(GroebnerBasis, DefineVariable) {
    auto x = defineVariable<Rational<int>>('x');
    Polynomial<Rational<int>> p({{Monomial({{'x', 1}}), 1}});
    EXPECT_EQ(p, x);
}

TEST(GroebnerBasis, PolynomialReduce1) {
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    Polynomial<Rational<int>> f = (x^3) + x * (y^2) + 5;
    Polynomial<Rational<int>> g1 = x * (y^2) - 5;
    Polynomial<Rational<int>> g2 = (x^2) + 3 * (y^2);
    std::vector<Polynomial<Rational<int>>> G = {g1, g2};
    auto [Q, r] = polynomialReduce(f, G, LexOrder({'x', 'y'}));
    EXPECT_EQ(Q[0], -2);
    EXPECT_EQ(Q[1], x);
    EXPECT_EQ(r, -5);
}

TEST(GroebnerBasis, PolynomialReduce2) {
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    Polynomial<Rational<int>> f = (x^2)*y + 1;
    Polynomial<Rational<int>> g1 = x * y + 1;
    Polynomial<Rational<int>> g2 = y + 1;
    std::vector<Polynomial<Rational<int>>> G = {g1, g2};
    auto [Q, r] = polynomialReduce(f, G, LexOrder({'x', 'y'}));
    EXPECT_EQ(Q[0], x);
    EXPECT_EQ(Q[1], 0);
    EXPECT_EQ(r, -x + 1);
}

TEST(GroebnerBasis, PolynomialReduce3) {
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    Polynomial<Rational<int>> f = (x^2)*y + x*(y^2) + (y^2);
    Polynomial<Rational<int>> g1 = x * y - 1;
    Polynomial<Rational<int>> g2 = (y^2) - 1;
    std::vector<Polynomial<Rational<int>>> G = {g1, g2};
    auto [Q, r] = polynomialReduce(f, G, LexOrder({'x', 'y'}));
    EXPECT_EQ(Q[0], x + y);
    EXPECT_EQ(Q[1], 1);
    EXPECT_EQ(r, x + y + 1);
}

TEST(GroebnerBasis, PolynomialReduce4) {
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    Polynomial<Rational<int>> f = (x^2)*y + 1;
    Polynomial<Rational<int>> g2 = x * y + 1;
    Polynomial<Rational<int>> g1 = y + 1;
    std::vector<Polynomial<Rational<int>>> G = {g1, g2};
    auto [Q, r] = polynomialReduce(f, G, LexOrder({'x', 'y'}));
    EXPECT_EQ(Q[0], x^2);
    EXPECT_EQ(Q[1], 0);
    EXPECT_EQ(r, -(x^2) + 1);
}

TEST(GroebnerBasis, PolynomialReduce5) {
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    auto z = defineVariable<Rational<int>>('z');
    Polynomial<Rational<int>> f = (x^5) + (y^5)+ (z^5) - 1;
    Polynomial<Rational<int>> g1 = (x^4) + y + z;
    Polynomial<Rational<int>> g2 = (x^2) + (y^2) + (z^2);
    Polynomial<Rational<int>> g3 = x + (y^3) + (z^3);
    std::vector<Polynomial<Rational<int>>> G = {g1, g2, g3};
    auto [Q, r] = polynomialReduce(f, G, LexOrder({'x', 'y', 'z'}));
    EXPECT_EQ(Q[0], x);
    EXPECT_EQ(Q[1], 0);
    EXPECT_EQ(Q[2], -y - z);
    EXPECT_EQ(r, (y^5) + (z^5) + (y^4) + (z^4) + (y^3) * z + y * (z^3) - 1);
}

TEST(GroebnerBasis, GroebnerBasis1) {
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');

    auto f1 = (x^3) - 2*x*y;
    auto f2 = (x^2)*y - 2*(y^2) + x;
    std::vector<Polynomial<Rational<int>>> F = {f1, f2};
    std::vector<Polynomial<Rational<int>>> G = calculateGroebnerBasis(F, GradedLexOrder({'x', 'y'}));

    auto g1 = (x^2);
    auto g2 = x*y;
    auto g3 = (y^2) - Rational<int>(1, 2) * x;
    std::vector<Polynomial<Rational<int>>> expectedG = {g1, g2, g3};
    EXPECT_EQ(G, expectedG);   
}

TEST(GroebnerBasis, GroebnerBasis2) {
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    auto z = defineVariable<Rational<int>>('z');

    auto f1 = x + y + z - 1;
    auto f2 = (x^2) + (y^2) + (z^2) - 3;
    auto f3 = (x^3) + (y^3) + (z^3) - 4;
    std::vector<Polynomial<Rational<int>>> F = {f1, f2, f3};
    std::vector<Polynomial<Rational<int>>> G = calculateGroebnerBasis(F, LexOrder({'x', 'y', 'z'}));

    auto g1 = x + y + z - 1;
    auto g2 = (y^2) + (z^2) + y*z - y - z - 1;
    auto g3 = (z^3) - (z^2) - z;
    std::vector<Polynomial<Rational<int>>> expectedG = {g1, g2, g3};
    EXPECT_EQ(G, expectedG);   
}

TEST(GroebnerBasis, GroebnerBasis3) {
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    auto z = defineVariable<Rational<int>>('z');
    auto u = defineVariable<Rational<int>>('u');
    auto v = defineVariable<Rational<int>>('v');

    auto f1 = 3*u+3*u*v*v-u*u*u-x;
    auto f2 = 3*v+3*u*u*v-v*v*v-y;
    auto f3 = 3*u*u-3*v*v-z;
    std::vector<Polynomial<Rational<int>>> F = {f1, f2, f3};
    std::vector<Polynomial<Rational<int>>> G = calculateGroebnerBasis(F, LexOrder({'u', 'v', 'x', 'y', 'z'}));

    auto g = (-Rational<int>(64, 19683) * (z ^ 9)) +
             (Rational<int>(16, 243) * (x ^ 2) * (z ^ 6)) -
             (Rational<int>(16, 243) * (y ^ 2) * (z ^ 6)) +
             (Rational<int>(5, 9) * (x ^ 4) * (z ^ 3)) +
             (Rational<int>(26, 9) * (x ^ 2) * (y ^ 2) * (z ^ 3)) +
             (Rational<int>(16, 9) * (x ^ 2) * (z ^ 5)) +
             (Rational<int>(5, 9) * (y ^ 4) * (z ^ 3)) +
             (Rational<int>(16, 9) * (y ^ 2) * (z ^ 5)) +
             (Rational<int>(128, 243) * (z ^ 7)) +
             (x ^ 6) -
             (3 * (x ^ 4) * (y ^ 2)) +
             (6 * (x ^ 4) * (z ^ 2)) +
             (3 * (x ^ 2) * (y ^ 4)) +
             (Rational<int>(80, 9) * (x ^ 2) * (z ^ 4)) -
             (y ^ 6) -
             (6 * (y ^ 4) * (z ^ 2)) -
             (Rational<int>(80, 9) * (y ^ 2) * (z ^ 4)) -
             (3 * (x ^ 4) * z) +
             (6 * (x ^ 2) * (y ^ 2) * z) -
             (16 * (x ^ 2) * (z ^ 3)) -
             (3 * (y ^ 4) * z) -
             (16 * (y ^ 2) * (z ^ 3)) -
             (Rational<int>(64, 3) * (z ^ 5));

    EXPECT_TRUE(std::find(G.begin(), G.end(), g) != G.end());
}

TEST(GroebnerBasis, GroebnerBasis4) {
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    auto z = defineVariable<Rational<int>>('z');
    auto u = defineVariable<Rational<int>>('u');
    auto t = defineVariable<Rational<int>>('t');

    auto f1 = t + u - x;
    auto f2 = (t^2) + 2*t*u - y;
    auto f3 = (t^3) +3 * (t^2) * u - z;
    std::vector<Polynomial<Rational<int>>> F = {f1, f2, f3};
    std::vector<Polynomial<Rational<int>>> G = calculateGroebnerBasis(F, LexOrder({'t', 'u', 'x', 'y', 'z'}));

    auto g = (x^3) * z - Rational<int>(3, 4) * (x^2) * (y^2) - Rational<int>(3, 2)*x*y*z + (y^3) + Rational<int>(1, 4) * (z^2);
    EXPECT_EQ(G.size() , 7);
    EXPECT_TRUE(std::find(G.begin(), G.end(), g) != G.end());
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}