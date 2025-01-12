#include <gtest/gtest.h>
#include "rational.hpp"

TEST(Rational, DefaultConstructor) {
    Rational<int> r = Rational<int>();
    EXPECT_EQ(r.getNumerator(), 0);
    EXPECT_EQ(r.getDenominator(), 1);
}

TEST(Rational, Constructor1) {
    Rational<int> r = Rational<int>(134);
    EXPECT_EQ(r.getNumerator(), 134);
    EXPECT_EQ(r.getDenominator(), 1);
}

TEST(Rational, Constructor2) {
    Rational<int> r = Rational<int>(-30, 5);
    EXPECT_EQ(r.getNumerator(), -6);
    EXPECT_EQ(r.getDenominator(), 1);
}

TEST(Rational, Constructor3) {
    Rational<int> r = Rational<int>(-3, -5);
    EXPECT_EQ(r.getNumerator(), 3);
    EXPECT_EQ(r.getDenominator(), 5);
}

TEST(Rational, Constructor4) {
    Rational<int> r = Rational<int>(2, -40);
    EXPECT_EQ(r.getNumerator(), -1);
    EXPECT_EQ(r.getDenominator(), 20);
}

TEST(Rational, Addition1) {
    Rational<int> r1 = Rational<int>(1, 2);
    Rational<int> r2 = Rational<int>(1, 3);
    Rational<int> r3 = r1 + r2;
    EXPECT_EQ(r3.getNumerator(), 5);
    EXPECT_EQ(r3.getDenominator(), 6);
}

TEST(Rational, Addition2) {
    Rational<int> r1 = Rational<int>(1, 2);
    Rational<int> r3 = r1 + 10;
    EXPECT_EQ(r3.getNumerator(), 21);
    EXPECT_EQ(r3.getDenominator(), 2);
}

TEST(Rational, AdditionInPlace1) {
    Rational<int> r1 = Rational<int>(1, 2);
    r1 += Rational<int>(1, 3);
    EXPECT_EQ(r1.getNumerator(), 5);
    EXPECT_EQ(r1.getDenominator(), 6);
}

TEST(Rational, AdditionInPlace2) {
    Rational<int> r1 = Rational<int>(1, 2);
    r1 += 10;
    EXPECT_EQ(r1.getNumerator(), 21);
    EXPECT_EQ(r1.getDenominator(), 2);
}

TEST(Rational, Subtraction1) {
    Rational<int> r1 = Rational<int>(1, 2);
    Rational<int> r2 = Rational<int>(1, 3);
    Rational<int> r3 = r1 - r2;
    EXPECT_EQ(r3.getNumerator(), 1);
    EXPECT_EQ(r3.getDenominator(), 6);
}

TEST(Rational, Subtraction2) {
    Rational<int> r1 = Rational<int>(1, 2);
    Rational<int> r3 = r1 - 10;
    EXPECT_EQ(r3.getNumerator(), -19);
    EXPECT_EQ(r3.getDenominator(), 2);
}

TEST(Rational, SubtractionInPlace1) {
    Rational<int> r1 = Rational<int>(1, 2);
    r1 -= Rational<int>(1, 3);
    EXPECT_EQ(r1.getNumerator(), 1);
    EXPECT_EQ(r1.getDenominator(), 6);
}

TEST(Rational, SubtractionInPlace2) {
    Rational<int> r1 = Rational<int>(1, 2);
    r1 -= 10;
    EXPECT_EQ(r1.getNumerator(), -19);
    EXPECT_EQ(r1.getDenominator(), 2);
}

TEST(Rational, Multiplication1) {
    Rational<int> r1 = Rational<int>(1, 2);
    Rational<int> r2 = Rational<int>(1, 3);
    Rational<int> r3 = r1 * r2;
    EXPECT_EQ(r3.getNumerator(), 1);
    EXPECT_EQ(r3.getDenominator(), 6);
}

TEST(Rational, Multiplication2) {
    Rational<int> r1 = Rational<int>(1, 2);
    Rational<int> r3 = r1 * 10;
    EXPECT_EQ(r3.getNumerator(), 5);
    EXPECT_EQ(r3.getDenominator(), 1);
}

TEST(Rational, MultiplicationInPlace1) {
    Rational<int> r1 = Rational<int>(1, 2);
    r1 *= Rational<int>(1, 3);
    EXPECT_EQ(r1.getNumerator(), 1);
    EXPECT_EQ(r1.getDenominator(), 6);
}

TEST(Rational, MultiplicationInPlace2) {
    Rational<int> r1 = Rational<int>(1, 2);
    r1 *= 10;
    EXPECT_EQ(r1.getNumerator(), 5);
    EXPECT_EQ(r1.getDenominator(), 1);
}

TEST(Rational, Division1) {
    Rational<int> r1 = Rational<int>(1, 2);
    Rational<int> r2 = Rational<int>(1, 3);
    Rational<int> r3 = r1 / r2;
    EXPECT_EQ(r3.getNumerator(), 3);
    EXPECT_EQ(r3.getDenominator(), 2);
}

TEST(Rational, Division2) {
    Rational<int> r1 = Rational<int>(1, 2);
    Rational<int> r3 = r1 / 10;
    EXPECT_EQ(r3.getNumerator(), 1);
    EXPECT_EQ(r3.getDenominator(), 20);
}

TEST(Rational, DivisionInPlace1) {
    Rational<int> r1 = Rational<int>(1, 2);
    r1 /= Rational<int>(1, 3);
    EXPECT_EQ(r1.getNumerator(), 3);
    EXPECT_EQ(r1.getDenominator(), 2);
}

TEST(Rational, DivisionInPlace2) {
    Rational<int> r1 = Rational<int>(1, 2);
    r1 /= 10;
    EXPECT_EQ(r1.getNumerator(), 1);
    EXPECT_EQ(r1.getDenominator(), 20);
}

TEST(Rational, DivisionByZero) {
    Rational<int> r1 = Rational<int>(1, 2);
    Rational<int> r2 = Rational<int>(0, 1);
    EXPECT_THROW(r1 / r2, std::invalid_argument);
    EXPECT_THROW(r1 /= r2, std::invalid_argument);
    EXPECT_THROW(r1 / 0, std::invalid_argument);
}

TEST(Rational, Equality) {
    Rational<int> r1 = Rational<int>(1, 2);
    Rational<int> r2 = Rational<int>(-1, -2);
    Rational<int> r3 = Rational<int>(1, 3);
    Rational<int> r4 = Rational<int>(40, 5);
    EXPECT_TRUE(r1 == r2);
    EXPECT_FALSE(r1 == r3);
    EXPECT_TRUE(r4 == 8);
    EXPECT_FALSE(r1 == 2);
    EXPECT_FALSE(1 == r4);
    EXPECT_FALSE(2 == r1);
}

TEST(Rational, Comparison1) {
    Rational<int> r1 = Rational<int>(1, 2);
    Rational<int> r2 = Rational<int>(1, 3);
    Rational<int> r3 = Rational<int>(2, 3);
    EXPECT_TRUE(r1 < r3);
    EXPECT_FALSE(r1 < r2);
    EXPECT_TRUE(r3 > r2);
    EXPECT_FALSE(r2 > r1);
    EXPECT_TRUE(r1 <= r3);
    EXPECT_FALSE(r1 <= r2);
    EXPECT_TRUE(r3 >= r2);
    EXPECT_FALSE(r2 >= r1);
}

TEST(Rational, Comparison2) {
    Rational<int> r1 = Rational<int>(-1, 2);
    Rational<int> r2 = Rational<int>(1, 3);
    Rational<int> r3 = Rational<int>(2, -3);
    EXPECT_FALSE(r1 < r3);
    EXPECT_TRUE(r1 < r2);
    EXPECT_FALSE(r3 > r2);
    EXPECT_TRUE(r2 > r1);
    EXPECT_FALSE(r1 <= r3);
    EXPECT_TRUE(r1 <= r2);
    EXPECT_FALSE(r3 >= r2);
    EXPECT_TRUE(r2 >= r1);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}