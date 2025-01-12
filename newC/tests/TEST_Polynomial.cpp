#include <gtest/gtest.h>
#include "polynomial.hpp"
#include "polynomialMethods.hpp"

TEST(Polynomial, DefaultConstructor) {
    Polynomial<Rational<int>> p = Polynomial<Rational<int>>();
    EXPECT_TRUE(p.isZeroPolynomial());
}

TEST(Polynomial, Constructor) {
    std::map<Monomial, Rational<int>> coefficients = {
        {Monomial(), Rational<int>(1)},
        {Monomial({{'x', 1}}), Rational<int>(2)},
        {Monomial({{'y', 2}}), Rational<int>(3)}
    };
    Polynomial<Rational<int>> p = Polynomial<Rational<int>>(coefficients);
    EXPECT_EQ(p.getCoefficients(), coefficients);
}

TEST(Polynomial, Add1) {
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    Polynomial<Rational<int>> p = x * 2 + y * 3;
    std::map<Monomial, Rational<int>> coefficients = {
        {Monomial({{'x', 1}}), 2},
        {Monomial({{'y', 1}}), 3}
    };
    Polynomial<Rational<int>> q = Polynomial<Rational<int>>(coefficients);
    EXPECT_EQ(p, q);
}

TEST(Polynomial, Add2) {
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    Polynomial<Rational<int>> p = (x^2) + (y^2) + 5;
    Polynomial<Rational<int>> q = -(x * x) + 3 * y * y;
    EXPECT_EQ(p + q, 4 * y * y + 5);
}

TEST(Polynomial, AddInPlace) {
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    Polynomial<Rational<int>> p = (x^3) + x * y * y + 5;
    p += x * y * y - 5;
    EXPECT_EQ(p, (x^3) + 2 * x * y * y);
}

TEST(Polynomial, Sub1) {
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    Polynomial<Rational<int>> p = x * 2 - y * 3;
    std::map<Monomial, Rational<int>> coefficients = {
        {Monomial({{'x', 1}}), 2},
        {Monomial({{'y', 1}}), -3}
    };
    Polynomial<Rational<int>> q = Polynomial<Rational<int>>(coefficients);
    EXPECT_EQ(p, q);
}

TEST(Polynomial, Sub2) {
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    Polynomial<Rational<int>> p = (x^2) + (y^2) + 5;
    Polynomial<Rational<int>> q = (x * x) + 3 * y * y;
    EXPECT_EQ(p - q, -2 * y * y + 5);
}

TEST(Polynomial, SubInPlace) {
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    Polynomial<Rational<int>> p = (x^3) + x * y * y + 5;
    p -= x * y * y - 5;
    EXPECT_EQ(p, (x^3) + 10);
}

TEST(Polynomial, Multiplication1) {
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    auto p = ((x^2) + 3 * (y^2) + 5) * (x + y);
    auto q = (x^3) + (x^2) * y + 3 * x * (y^2) + 5 * x + 5 * y + 3*(y^3);
    EXPECT_EQ(p, q);
}

TEST(Polynomial, Multiplication2) {
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    auto p = ((x^2) + 3 * (y^2) + 5) * 6;
    auto q = 6*(x^2) + 18 * (y^2) + 30;
    EXPECT_EQ(p, q);
}

TEST(Polynomial, Multiplication3) {
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    auto p = ((x^2) + 3 * (y^2) + 5) * 0;
    EXPECT_EQ(p, 0);
}

TEST(polynomial, MultiplicationInPlace) {
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    Polynomial<Rational<int>> p = (x^3) + x * y * y + 5;
    p *= x * y * y - 5;
    EXPECT_EQ(p, (x^4)*(y^2)-5*(x^3)+(x^2)*(y^4)-25);
}

TEST(Polynomial, EvaluateError) {
    std::map<char, Rational<int>> values = {{'x', 1}};
    auto y = defineVariable<Rational<int>>('y');
    Polynomial<Rational<int>> p = y;
    EXPECT_THROW(p.evaluate(values), std::invalid_argument);
}

TEST(Polynomial, Evaulate) {
    std::map<char, Rational<int>> values = {{'x', 1}, {'y', 2}, {'z', 0}};
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    auto z = defineVariable<Rational<int>>('z');
    Polynomial<Rational<int>> p = -4 * (x^2) + 30 * x * y * z + (z^111) + 5 * x * y;
    EXPECT_EQ(p.evaluate(values), 6);
}

TEST(Polynomial, TotalDegree) {
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    auto z = defineVariable<Rational<int>>('z');
    Polynomial<Rational<int>> p = (x^2) + x * y * z + (z^111) + 5 * x * y;
    EXPECT_EQ(p.totalDegree(), 111);
}

TEST(Polynomial, SubstituteError) {
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    Polynomial<Rational<int>> p = (x^2) + x * y + 5;
    EXPECT_THROW(p.substitute('z', 1), std::invalid_argument);
}

TEST(Polynomial, Substitute) {
    auto x = defineVariable<Rational<int>>('x');
    auto y = defineVariable<Rational<int>>('y');
    Polynomial<Rational<int>> p = (x^2) + x * y + 5;
    Polynomial<Rational<int>> q = 3*y + 14;
    EXPECT_EQ(p.substitute('x', 3), q);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}