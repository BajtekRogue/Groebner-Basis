#include <gtest/gtest.h>
#include "monomial.hpp"

TEST(Monomial, DefaultConstructor) {
    Monomial m = Monomial();
    EXPECT_EQ(m.getDegree(), 0);
    EXPECT_EQ(m.getNumVariables(), 0);
    EXPECT_EQ(m.getVariables(), std::vector<char>{});
}

TEST(Monomial, NormalConstructor) {
    Monomial m = Monomial({{'x', 2}, {'z', 3}, {'y', 4}});
    EXPECT_EQ(m.getDegree(), 9);
    EXPECT_EQ(m.getNumVariables(), 3);
    EXPECT_EQ(m.getVariables(), (std::vector<char>{'x', 'y', 'z'}));
}

TEST(Monomial, RemoveZeroExponentsDuringConstructor) {
    Monomial m = Monomial({{'x', 2}, {'a', 0}, {'b', 4}});
    EXPECT_EQ(m.getDegree(), 6);
    EXPECT_EQ(m.getNumVariables(), 2);
    EXPECT_EQ(m.getVariables(), (std::vector<char>{'b', 'x'}));
}

TEST(Monomial, ThrowErrorNegativeExponnetsDuringConstructor) {
    EXPECT_THROW(Monomial({{'x', 2}, {'a', -1}, {'b', 4}}), std::invalid_argument);
}

TEST(Monomial, CopyConstructor) {
    Monomial m = Monomial({{'x', 2}, {'z', 3}, {'y', 4}});
    Monomial n = Monomial(m);
    EXPECT_EQ(n.getDegree(), 9);
    EXPECT_EQ(n.getNumVariables(), 3);
    EXPECT_EQ(n.getVariables(), (std::vector<char>{'x', 'y', 'z'}));
}

TEST(Monomial, GetExponent) {
    Monomial m = Monomial({{'x', 2}, {'z', 3}, {'y', 4}});
    EXPECT_EQ(m.getExponent('x'), 2);
    EXPECT_EQ(m.getExponent('y'), 4);
    EXPECT_EQ(m.getExponent('z'), 3);
    EXPECT_EQ(m.getExponent('w'), 0);
}

TEST(Monomial, Equality) {
    Monomial m = Monomial({{'x', 2}, {'z', 3}, {'y', 4}});
    Monomial n = Monomial({{'z', 3}, {'y', 4}, {'x', 2}});
    Monomial k = Monomial({{'a', 2}, {'b', 3}, {'c', 4}});
    EXPECT_EQ(m, n);
    EXPECT_NE(m, k);
}

TEST(Monomial, Comparison) {
    Monomial m = Monomial({{'x', 2}, {'y', 3}, {'z', 4}});
    Monomial n = Monomial({{'x', 3}, {'y', 4}, {'z', 10}});
    EXPECT_GE(n, m);
    EXPECT_LE(m, n);
    EXPECT_GT(n, m);
    EXPECT_LT(m, n);
}

TEST(Monomial, Multiplication1) {
    Monomial m = Monomial({{'x', 2}, {'y', 3}, {'z', 4}});
    Monomial n = Monomial({{'x', 3}, {'y', 4}, {'z', 10}});
    Monomial k = m * n;
    Monomial l = Monomial({{'x', 5}, {'y', 7}, {'z', 14}});
    EXPECT_EQ(k, l);
}

TEST(Monomial, Multiplication2) {
    Monomial m = Monomial({{'x', 2}, {'y', 3}, {'z', 4}});
    Monomial n = Monomial({{'a', 3}, {'y', 4}, {'b', 1}});
    Monomial k = m * n;
    Monomial l = Monomial({{'x', 2}, {'y', 7}, {'z', 4}, {'a', 3}, {'b', 1}});
    EXPECT_EQ(k, l);
}

TEST(Monomial, MultiplicationInPlace1) {
    Monomial m = Monomial({{'x', 2}, {'y', 3}, {'z', 4}});
    Monomial n = Monomial({{'x', 3}, {'y', 4}, {'z', 10}});
    m *= n;
    Monomial l = Monomial({{'x', 5}, {'y', 7}, {'z', 14}});
    EXPECT_EQ(m, l);
    
}

TEST(Monomial, MultiplicationInPlace2) {
    Monomial m = Monomial({{'x', 2}, {'y', 3}, {'z', 4}});
    Monomial n = Monomial({{'a', 3}, {'y', 4}, {'b', 1}});
    m *= n;
    Monomial l = Monomial({{'x', 2}, {'y', 7}, {'z', 4}, {'a', 3}, {'b', 1}});
    EXPECT_EQ(m, l);
    
}

TEST(Monomial, Division) {
    Monomial m = Monomial({{'x', 2}, {'y', 3}, {'z', 4}});
    Monomial n = Monomial({{'x', 3}, {'y', 40}, {'z', 10}});
    Monomial k = n / m;
    Monomial l = Monomial({{'x', 1}, {'y', 37}, {'z', 6}});
    EXPECT_EQ(k, l);
}

TEST(Monomial, DivisionError1) {
    Monomial m = Monomial({{'x', 2}, {'y', 3}, {'z', 4}});
    Monomial n = Monomial({{'x', 3}, {'y', 40}, {'z', 10}});
    EXPECT_THROW(m / n, std::invalid_argument);
}

TEST(Monomial, DivisionError2) {
    Monomial m = Monomial({{'x', 2}, {'y', 3}, {'z', 4}});
    Monomial n = Monomial({{'a', 3}, {'y', 4}, {'b', 1}});
    EXPECT_THROW(m / n, std::invalid_argument);
}

TEST(Monomial, DivisionInPlace) {
    Monomial m = Monomial({{'x', 2}, {'y', 3}, {'z', 4}});
    Monomial n = Monomial({{'x', 3}, {'y', 40}, {'z', 10}});
    n /= m;
    Monomial l = Monomial({{'x', 1}, {'y', 37}, {'z', 6}});
    EXPECT_EQ(n, l);
    
}

TEST(Monomial, DivisionInPlaceError) {
    Monomial m = Monomial({{'x', 2}, {'y', 3}, {'z', 4}});
    Monomial n = Monomial({{'a', 3}, {'y', 4}, {'b', 1}});
    EXPECT_THROW(n /= m, std::invalid_argument);
}

TEST(Monomial, ToString) {
    Monomial m = Monomial({{'x', 2}, {'y', 3}, {'z', 1}, {'w', 4}});
    EXPECT_EQ(m.toString(), "w⁴x²y³z");
}

TEST(Monomial, LeastCommonMultiple1) {
    Monomial m = Monomial({{'x', 2}, {'y', 3}, {'z', 1}, {'w', 4}});
    Monomial n = Monomial({{'x', 3}, {'y', 4}, {'z', 10}});
    Monomial k = Monomial::lcm(m, n);
    Monomial l = Monomial({{'x', 3}, {'y', 4}, {'z', 10}, {'w', 4}});
    EXPECT_EQ(k, l);
}

TEST(Monomial, LeastCommonMultiple2) {
    Monomial m = Monomial({{'x', 2}, {'y', 3}, {'z', 1}, {'w', 4}});
    Monomial n = Monomial({{'a', 3}, {'b', 4}, {'c', 10}, {'d', 4}});
    Monomial k = Monomial::lcm(m, n);
    Monomial l = Monomial({{'x', 2}, {'y', 3}, {'z', 1}, {'w', 4}, {'a', 3}, {'b', 4}, {'c', 10}, {'d', 4}});
    EXPECT_EQ(k, l);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}