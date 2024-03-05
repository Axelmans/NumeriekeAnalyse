class FloatingPoint:

    def __init__(self, val: float, t: int):
        # t = amount of digits in mantissa after floating point
        self.t = t
        # mantissa requires work...
        self.mantissa = self.__mantissa(val, t)
        # determine power = amount of digits of val before its decimal point
        self.power = str(val).find(".")

    @staticmethod
    def __mantissa(val: float, t: int) -> float:
        val_as_str = str(val)
        mantissa_str = "0."
        for digit in val_as_str:
            mantissa_str += digit if digit != "." else ""
        mantissa_str = str(float(mantissa_str).__round__(t))
        while len(mantissa_str[2:]) != t:
            mantissa_str += "0"
        return float(mantissa_str)
