#ifndef RATIONAL_HPP
#define RATIONAL_HPP

#include <iostream>
#include <stdexcept>
#include <numeric> 
#include <sstream>

/**
 * @brief Represents a rational number with numerator and denominator of integral type.
 * 
 * @tparam `T` integer type, must be signed 
 */
template <typename T>
class Rational {
    static_assert(std::is_integral<T>::value && std::is_signed<T>::value, "T must be a signed integer type");

public:
    Rational(T numerator = 0, T denominator = 1) : _numerator(numerator), _denominator(denominator) {
        if (denominator == 0) {
            throw std::invalid_argument("Denominator cannot be zero");
        }
        else {
            simplify();
        }
    }

    Rational(const Rational& other) : _numerator(other._numerator), _denominator(other._denominator) {}

    T getNumerator() const { return _numerator; }
    T getDenominator() const { return _denominator; }

    Rational& operator=(const Rational& other) {
        if (this != &other) {
            _numerator = other._numerator;
            _denominator = other._denominator;
        }
        return *this;
    }
    
    Rational operator+(const Rational& other) const {
        T resultNumerator = _numerator * other._denominator + other._numerator * _denominator;
        T resultDenominator = _denominator * other._denominator;
        return Rational(resultNumerator, resultDenominator);
    }

    Rational operator+(T other) const {
        T resultNumerator = _numerator + other * _denominator;
        T resultDenominator = _denominator;
        return Rational(resultNumerator, resultDenominator);
    }

    friend Rational operator+(T other, const Rational& r) {
        return r + other;
    }

    Rational operator+=(const Rational& other) {
        _numerator = _numerator * other._denominator + other._numerator * _denominator;
        _denominator = _denominator * other._denominator;
        simplify();
        return *this;
    }

    Rational operator+=(T other) {
        _numerator = _numerator + other * _denominator;
        simplify();
        return *this;
    }

    Rational operator-(const Rational& other) const {
        T resultNumerator = _numerator * other._denominator - other._numerator * _denominator;
        T resultDenominator = _denominator * other._denominator;
        return Rational(resultNumerator, resultDenominator);
    }

    Rational operator-(T other) const {
        T resultNumerator = _numerator - other * _denominator;    
        T resultDenominator = _denominator;
        return Rational(resultNumerator, resultDenominator);
    }

    friend Rational operator-(T other, const Rational& r) {
        return -(Rational(other) - r);
    }

    Rational operator-=(const Rational& other) {
        _numerator = _numerator * other._denominator - other._numerator * _denominator;
        _denominator = _denominator * other._denominator;
        simplify();
        return *this;
    }

    Rational operator-=(T other) {
        _numerator = _numerator - other * _denominator;
        simplify();
        return *this;
    }

    Rational operator*(const Rational& other) const {
        T resultNumerator = _numerator * other._numerator;
        T resultDenominator = _denominator * other._denominator;
        return Rational(resultNumerator, resultDenominator);
    }

    Rational operator*(T other) const {
        T resultNumerator = _numerator * other;
        T resultDenominator = _denominator;
        return Rational(resultNumerator, resultDenominator);
    }

    friend Rational operator*(T other, const Rational& r) {
        return r * other;
    }

    Rational operator*=(const Rational& other) {
        _numerator = _numerator * other._numerator;
        _denominator = _denominator * other._denominator;
        simplify();
        return *this;
    }

    Rational operator*=(T other) {
        _numerator = _numerator * other;
        simplify();
        return *this;
    }

    Rational operator/(const Rational& other) const {
        if (other._numerator == 0) {
            throw std::invalid_argument("Cannot divide by zero");
        }
        T resultNumerator = _numerator * other._denominator;
        T resultDenominator = _denominator * other._numerator;
        return Rational(resultNumerator, resultDenominator);
    }

    Rational operator/(T other) const {
        if (other == 0) {
            throw std::invalid_argument("Cannot divide by zero");
        }
        T resultNumerator = _numerator;
        T resultDenominator = _denominator * other;
        return Rational(resultNumerator, resultDenominator);
    }

    friend Rational operator/(T other, const Rational& r) {
        return Rational(other * r.getDenominator(), r.getNumerator());
    }

    Rational operator/=(const Rational& other) {
        if (other._numerator == 0) {
            throw std::invalid_argument("Cannot divide by zero");
        }
        _numerator = _numerator * other._denominator;
        _denominator = _denominator * other._numerator;
        simplify();
        return *this;
    }

    Rational operator/=(T other) {
        if (other == 0) {
            throw std::invalid_argument("Cannot divide by zero");
        }
        _denominator = _denominator * other;
        simplify();
        return *this;
    }

    Rational operator+() const {
        return *this;
    }

    Rational operator-() const {
        return Rational(-_numerator, _denominator);
    }

    bool operator==(const Rational& other) const {
        return _numerator == other._numerator && _denominator == other._denominator;
    }

    bool operator==(T other) const {
        return _numerator == other && _denominator == 1;
    }

    friend bool operator==(T other, const Rational& r) {
        return r == other;
    }

    bool operator!=(const Rational& other) const {
        return !(*this == other);
    }

    bool operator!=(T other) const {
        return !(*this == other);
    }

    friend bool operator!=(T other, const Rational& r) {
        return r != other;
    }

    bool operator<(const Rational& other) const {
        return _numerator * other._denominator < _denominator * other._numerator;
    }

    friend bool operator<(T other, const Rational& r) {
        return Rational(other) < r;
    }

    bool operator<(T other) const {
        return _numerator < other * _denominator;
    }

    bool operator>(const Rational& other) const {
        return other < *this;
    }

    bool operator>(T other) const {
        return other < *this;
    }

    friend bool operator>(T other, const Rational& r) {
        return r < other;
    }

    bool operator<=(const Rational& other) const {
        return !(*this > other);
    }

    bool operator<=(T other) const {
        return !(*this > other);
    }

    friend bool operator<=(T other, const Rational& r) {
        return !(other > r);
    }

    bool operator>=(const Rational& other) const {
        return !(*this < other);
    }

    bool operator>=(T other) const {
        return !(*this < other);
    }

    friend bool operator>=(T other, const Rational& r) {
        return !(other < r);
    }
    
    friend std::ostream& operator<<(std::ostream& os, const Rational& r) {
        os << r._numerator;
        if (r._denominator != 1) {
            os << "/" << r._denominator;
        }
        return os;
    }

    std::string toString() const {
        std::ostringstream oss;
        oss << _numerator;
        if (_denominator != 1) {
            oss << "/" << _denominator;
        }
        return oss.str();
    }
    
private:
    T _numerator;
    T _denominator;

    // Simplify the rational number
    void simplify() {
        if (_numerator == 0) {
            _denominator = 1;
            return;
        }
        
        if (_denominator < 0) {
            // Make the denominator positive for consistency
            _numerator = -_numerator;
            _denominator = -_denominator;
        }

        T gcd = std::gcd(_numerator, _denominator);
        _numerator /= gcd;
        _denominator /= gcd;
    }

};


#endif // RATIONAL_HPP