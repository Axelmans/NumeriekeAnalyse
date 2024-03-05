from polynomial import *
from floatingpoint import *
from interpolation import *

if __name__ == '__main__':
    test = Interpolation("interpolation.json")
    coefficients = test.newton_coefficients()
    print(coefficients)
    print(test.newton(18))
