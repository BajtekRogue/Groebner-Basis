#ifndef POLYNOMIAL_HPP
#define POLYNOMIAL_HPP

#include <iostream>
#include <map>
#include <complex>
#include "monomial.hpp"
#include "monomialOrders.hpp"

template <typename T>
class Polynomial {

public:
    Polynomial() {}
    Polynomial(std::map<Monomial, T> coefficients) {
        for (const auto& [monomial, coefficient] : coefficients) {
            if (!isCoefficientZero(coefficient)) {
                _coefficients[monomial] = coefficient;
            }
        }
    }
    Polynomial(const Polynomial<T>& other, bool x = true) : _coefficients(other._coefficients) {
        // if (x) {
        //     std::cout << "we coping " << other << std::endl;
        // }
    }

    std::map<Monomial, T> getCoefficients() const { return _coefficients; }

    Polynomial operator+(const Polynomial<T>& other) const {
        std::map<Monomial, T> resultCoefficients = _coefficients;
        for (const auto& [monomial, coefficient] : other._coefficients) {
            resultCoefficients[monomial] += coefficient;
            if (isCoefficientZero(resultCoefficients[monomial])) {
                resultCoefficients.erase(monomial);
            }
        }
        return Polynomial(resultCoefficients);
    }

    Polynomial operator+(T other) const {
        std::map<Monomial, T> resultCoefficients = _coefficients;
        resultCoefficients[Monomial()] += other;
        if (isCoefficientZero(resultCoefficients[Monomial()])) {
            resultCoefficients.erase(Monomial());
        }
        return Polynomial(resultCoefficients);
    }

    friend Polynomial operator+(T other, const Polynomial<T>& p) {
        return p + other;
    }

    Polynomial operator+=(const Polynomial<T>& other) {
        for (const auto& [monomial, coefficient] : other._coefficients) {
            _coefficients[monomial] += coefficient;
            if (isCoefficientZero(_coefficients[monomial])) {
                _coefficients.erase(monomial);
            }
        }
        _validLeadingTerm = false;
        return *this;
    }

    Polynomial operator+=(T other) {
        _coefficients[Monomial()] += other;
        _validLeadingTerm = false;
        return *this;
    }

    Polynomial operator-(const Polynomial<T>& other) const {
        std::map<Monomial, T> resultCoefficients = _coefficients;
        for (const auto& [monomial, coefficient] : other._coefficients) {
            resultCoefficients[monomial] -= coefficient;
            if (isCoefficientZero(resultCoefficients[monomial])) {
                resultCoefficients.erase(monomial);
            }
        }
        return Polynomial(resultCoefficients);
    }

    Polynomial operator-(T other) const {
        std::map<Monomial, T> resultCoefficients = _coefficients;
        resultCoefficients[Monomial()] -= other;
        if (isCoefficientZero(resultCoefficients[Monomial()])) {
            resultCoefficients.erase(Monomial());
        }
        return Polynomial(resultCoefficients);
    }

    friend Polynomial operator-(T other, const Polynomial<T>& p) {
        return -(p - other);
    }

    Polynomial operator-=(const Polynomial<T>& other) {
        for (const auto& [monomial, coefficient] : other._coefficients) {
            _coefficients[monomial] -= coefficient;
            if (isCoefficientZero(_coefficients[monomial])) {
                _coefficients.erase(monomial);
            }
        }
        _validLeadingTerm = false;
        return *this;
    }

    Polynomial operator-=(T other) {
        _coefficients[Monomial()] -= other;
        if (isCoefficientZero(_coefficients[Monomial()])) {
            _coefficients.erase(Monomial());
        }
        _validLeadingTerm = false;
        return *this;
    }

    Polynomial operator*(const Polynomial<T>& other) const {
        std::map<Monomial, T> resultCoefficients;
        for (const auto& [monomial1, coefficient1] : _coefficients) {
            for (const auto& [monomial2, coefficient2] : other._coefficients) {
                Monomial monomial = monomial1 * monomial2;
                resultCoefficients[monomial] += coefficient1 * coefficient2;
            }
        }

        for (const auto& [monomial, coefficient] : resultCoefficients) {
            if (isCoefficientZero(coefficient)) {
                resultCoefficients.erase(monomial);
            }
        }
        return Polynomial(resultCoefficients);
    }

    Polynomial operator*(T other) const {
        if (isCoefficientZero(other)) {
            return Polynomial();
        }
        std::map<Monomial, T> resultCoefficients;
        for (const auto& [monomial, coefficient] : _coefficients) {
            resultCoefficients[monomial] = coefficient * other;
            if (isCoefficientZero(resultCoefficients[monomial])) {
                resultCoefficients.erase(monomial);
            }
        }
        return Polynomial(resultCoefficients);
    }

    friend Polynomial operator*(T other, const Polynomial<T>& p) {
        return p * other;
    }

    Polynomial operator*= (const Polynomial<T>& other) {
        std::map<Monomial, T> resultCoefficients;
        for (const auto& [monomial1, coefficient1] : _coefficients) {
            for (const auto& [monomial2, coefficient2] : other._coefficients) {
                Monomial monomial = monomial1 * monomial2;
                resultCoefficients[monomial] += coefficient1 * coefficient2;
            }
        }
        for (const auto& [monomial, coefficient] : resultCoefficients) {
            if (isCoefficientZero(coefficient)) {
                resultCoefficients.erase(monomial);
            }
        }
        _validLeadingTerm = false;
        _coefficients = resultCoefficients;
        return *this;
    }

    Polynomial operator*=(T other) {
        for (auto& [monomial, coefficient] : _coefficients) {
            coefficient *= other;
        }
        for (const auto& [monomial, coefficient] : _coefficients) {
            if (isCoefficientZero(coefficient)) {
                _coefficients.erase(monomial);
            }
        }
        _validLeadingTerm = false;
        return *this;
    }

    Polynomial operator+() {
        return *this;
    }

    Polynomial operator-() {
        std::map<Monomial, T> resultCoefficients;
        for (const auto& [monomial, coefficient] : _coefficients) {
            resultCoefficients[monomial] = -coefficient;
        }
        return Polynomial(resultCoefficients);
    }

    friend std::ostream& operator<<(std::ostream& os, const Polynomial& p) {
        os << p.toString(); 
        return os;
    }

    std::string toString() const {
        if (_coefficients.empty()) {
            return "0";
        }

        std::ostringstream oss;
        bool isFirst = true;

        // Iterate in reverse order (highest degree first)
        for (auto it = _coefficients.rbegin(); it != _coefficients.rend(); ++it) {
            const auto& monomial = it->first;
            const auto& coefficient = it->second;

            std::string coeffStr = coefficient.toString();
            std::string monomStr = monomial.toString();

            // Handle the sign
            if (!isFirst) {
                if (coeffStr[0] == '-') {
                    oss << " - ";
                    coeffStr = coeffStr.substr(1);
                } else {
                    oss << " + ";
                }
            } else {
                if (coeffStr[0] == '-') {
                    oss << "-";
                    coeffStr = coeffStr.substr(1);
                }
                isFirst = false;
            }

            // Handle coefficient printing
            if (coeffStr != "1" || monomStr == "1") {
                // Don't print coefficient 1 unless it's a constant term
                if (coeffStr == "1" && monomStr == "1") {
                    oss << "1";
                } else if (coeffStr != "1") {
                    oss << coeffStr;
                }
            }

            // Handle monomial printing
            if (!monomStr.empty() && monomStr != "1") {
                if (coeffStr != "1" && !coeffStr.empty()) {
                    oss << "·"; // use middle dot for multiplication
                }
                oss << monomStr;
            }
        }

        return oss.str();
    }

    bool operator==(const Polynomial<T>& other) const {
        return (*this - other).isZeroPolynomial();
    }

    bool operator==(T other) const {
        if (_coefficients.size() == 0) {
            return isCoefficientZero(other);
        }
        else {
            return (_coefficients.size() == 1 && _coefficients.begin()->first == Monomial() && isCoefficientZero(_coefficients.begin()->second - other));
        }
    }

    bool operator!=(const Polynomial<T>& other) const {
        return !(*this == other);
    }

    bool operator!=(T other) const {
        return !(other == *this);
    }

    Polynomial operator^(int exp) const {
        if (exp < 0) {
            throw std::invalid_argument("Negative exponent is not allowed");
        }
        else if (exp == 0) {
            return Polynomial<T>({{Monomial(), T(1)}});
        }

        Polynomial<T> result = Polynomial<T>({{Monomial(), T(1)}});
        Polynomial<T> base = *this;
        while (exp > 0) {
            if (exp % 2 == 1) {
                result *= base;
            }
            base *= base;
            exp /= 2;
        }
        return result;
    }

    bool isZeroPolynomial() const {
        for (const auto& [_, coefficient] : _coefficients) {
            if (!isCoefficientZero(coefficient)) {
                return false;
            }
        }
        return true;
    }

    /**
     * @brief Given map of variable values, evaluate the polynomial at the given point
     * @throws std::invalid_argument if a variable is not found in the polynomial
     */
    T evaluate(const std::map<char, T>& values) const {
        T result = T(0);
        for (const auto& [monomial, coefficient] : _coefficients) {
            T term = coefficient;
            for (const auto& [var, exp] : monomial.getMonomial()) {
                if (values.find(var) == values.end()) {
                    throw std::invalid_argument("Variable '" + std::string(1, var) + "' not found in the polynomial");
                }
                term *= power(values.at(var), exp);
            }
            result += term;
        }
        return result;
    }

    /**
     * @brief Calculate the total degree of the polynomial
     */
    int totalDegree() const {
        int result = 0;
        for (const auto& [monomial, _] : _coefficients) {
            result = std::max(result, monomial.getDegree());
        }
        return result;
    }

    /**
     * @brief Get the variables in the polynomial
     */
    std::vector<char> getVariables() const {
        std::set<char> variables;
        for (const auto& [monomial, _] : _coefficients) {
            for (const auto& var : monomial.getVariables()) {
                variables.insert(var);
            }
        }
        return std::vector<char>(variables.begin(), variables.end());
    }

    /**
     * @brief Substitute a variable with a value in the polynomial
     * @throws std::invalid_argument if the variable is not found in the polynomial
     */
    Polynomial substitute(char var, T val) const {
        std::vector<char> variables = getVariables();
        if (std::find(variables.begin(), variables.end(), var) == variables.end()) {
            throw std::invalid_argument("Variable '" + std::string(1, var) + "' not found in the polynomial");
        }

        std::map<Monomial, T> resultCoefficients;
        for (const auto& [monomial, coefficient] : _coefficients) {

            int currentExponent = monomial.getExponent(var);
            T newCoefficient = coefficient * power(val, currentExponent);

            std::map<char, int> newMonomial = monomial.getMonomial();
            if (newMonomial.find(var) != newMonomial.end()) {
                newMonomial.erase(var);
            }

            resultCoefficients[Monomial(newMonomial)] += newCoefficient;
        }
        return Polynomial(resultCoefficients);
    }
    /**
     * @brief Returns the leading monomial of the polynomial with respect to the given order
     */
    const Monomial& leadingMonomial(const MonomialOrder& order) const {
        cacheLeadingMonomialAndCoefficient(order);
        return _cachedLeadingMonomial;
    }

    /**
     * @brief Returns the leading coefficient of the polynomial with respect to the given order
     */
    T leadingCoefficient(const MonomialOrder& order) const {
        cacheLeadingMonomialAndCoefficient(order);
        return _cachedLeadingCoefficient;
    }

private:
    std::map<Monomial, T> _coefficients;
    mutable Monomial _cachedLeadingMonomial;
    mutable T _cachedLeadingCoefficient;
    mutable MonomialOrder const* _cachedOrder = nullptr;
    mutable bool _validLeadingTerm = false;

    T power(T base, int exp) const {
        T result = T(1);
        while (exp > 0) {
            if (exp % 2 == 1) {
                result *= base;
            }
            base *= base;
            exp /= 2;
        }
        return result;
    }

    bool isCoefficientZero(T coefficient) const {
        if constexpr (std::is_floating_point_v<T>) {
            return std::abs(coefficient) < std::numeric_limits<T>::epsilon();
        }
        else {
            return coefficient == T(0);
        }
    }

    void cacheLeadingMonomialAndCoefficient(const MonomialOrder& order) const {
        // Only recompute if the order has changed or cache is invalid
        if (_cachedOrder != &order || !_validLeadingTerm) {
            auto maxIt = std::max_element(_coefficients.begin(), _coefficients.end(),
                [&order](const auto& p1, const auto& p2) {
                    return order.compare(p1.first, p2.first);
                });
            
            if (maxIt == _coefficients.end()) {
                _cachedLeadingMonomial = Monomial();
                _cachedLeadingCoefficient = T(0);

            }
            else {
                _cachedLeadingMonomial = maxIt->first;
                _cachedLeadingCoefficient = maxIt->second;
            }

            _cachedOrder = &order;
            _validLeadingTerm = true;
        }
    }
};

#endif // POLYNOMIAL_HPP