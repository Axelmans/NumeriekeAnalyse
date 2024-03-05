from __future__ import annotations
from copy import deepcopy


# Used to properly print exponents for polynomials
def superscript(p):
    superscripts = ["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
    return ''.join([superscripts[int(char)] for char in str(p)])


class Polynomial:

    def __init__(self, coefficients=None):
        # Default polynomial: y = x
        if coefficients is None:
            self.coefficients = [0, 1]
        # Coefficients are ordered by ascending power
        else:
            self.coefficients = coefficients

    def __call__(self, input_value: float) -> float:
        res = 0
        # Again: coefficients are ordered in ascending power
        for power in range(len(self.coefficients)):
            res += self.coefficients[power] * input_value ** power
        return res

    def __str__(self):
        res = ""
        # Main roadblocks:
        # -ignoring zero coefficients
        # -plus or minus?
        for i in range(len(self.coefficients) - 1, -1, -1):
            # Constant, no need to print an x with an exponent
            if i == 0:
                if self.coefficients[i] == 0:
                    continue
                # Abs because a necessary '+' or '-' is printed beforehand
                res += str(abs(self.coefficients[i]))
            # Non constant
            elif i == len(self.coefficients) - 1 and i != 0:
                res += str(self.coefficients[i]) + "x"
                if i != 1:
                    res += superscript(i)
            else:
                res += str(abs(self.coefficients[i])) + "x"
                if i != 1:
                    res += superscript(i)
            # For following coefficient, determine its sign and add '+' or '-' preemptively
            if i > 0:
                if self.coefficients[i - 1] < 0 and self.coefficients[i - 1] != 0:
                    res += ' - '
                elif self.coefficients[i - 1] != 0:
                    res += ' + '
        return res

    def derivative(self) -> Polynomial:
        new_coefficients = []
        # Each coefficient becomes a lower power and is multiplied by original power
        for power in range(1, len(self.coefficients)):
            new_coefficients.append(power * self.coefficients[power])
        return Polynomial(new_coefficients)

    def bisect(self, a: float, b: float, tol: float = 0.0001) -> float:
        # There must be a zero-value between a and b, can be verified by checking the signs of their function value
        assert self(a) * self(b) <= 0, "No zero-value between given a and b."
        # For safety, deep-copies are used for a and b
        a_copy = deepcopy(min(a, b))
        b_copy = deepcopy(max(a, b))
        # (b_copy - a_copy)/2 is the maximum error after executing the algorithm n steps, this must not exceed tol
        while (b_copy - a_copy) / 2 > tol:
            # Determine average and replace either a and b with it
            t = (a_copy + b_copy) / 2
            # This condition indicates the zero value is between a and the average, so b is replaced
            if self(a_copy) * self(t) <= 0:
                b_copy = t
            # Otherwise, replace a
            else:
                a_copy = t
        # Algorithm returns the average between a and b
        return (a_copy + b_copy) / 2

    def newton(self, x: float, tol: float = 0.001) -> float:
        x_k: float = x
        # Convergence depends on start-value, sometimes might be impossible
        max_iterations = 1000
        while abs(self(x_k)) > tol and max_iterations != 0:
            x_k -= self(x_k)/self.derivative()(x_k)
            max_iterations -= 1
        if max_iterations == 0:
            print("Max iterations reached, convergence might be inaccurate.")
            print("Another starting value might lead to a more accurate answer.\n")
        return x_k

    def fixed_point(self, x: float) -> float:
        # f(x) = x <-> f(x) - x = 0
        new_polynomial = deepcopy(self)
        new_polynomial.coefficients[1] -= 1
        # Newton can be used to find zero point of the new polynomial
        return new_polynomial.newton(x)
