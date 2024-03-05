import json


class Interpolation:

    def __init__(self, input_file: str):
        self.data = {}
        data = json.load(open(input_file))
        for observation in data["Data"]:
            assert type(observation[0]) in [int, float] and type(observation[1]) in [int, float]
            self.data[observation[0]] = observation[1]

    def lagrange(self, x: float):
        assert min(self.data.keys()) <= x <= max(self.data.keys()), "Input x should be between data-bounds."
        if self.data.get(x):
            return self.data[x]
        res = 0
        data_as_list = list(self.data)
        for i in range(len(data_as_list)):
            numerator = 1
            denominator = 1
            for j in range(len(data_as_list)):
                if j == i:
                    continue
                numerator *= (x - data_as_list[j])
                denominator *= (data_as_list[i] - data_as_list[j])
            res += (numerator/denominator)*self.data[data_as_list[i]]
        return res

    def neville(self, x: float):
        assert min(self.data.keys()) <= x <= max(self.data.keys()), "Input x should be between data-bounds."
        if self.data.get(x):
            return self.data[x]
        polynomials = {}
        key_list = list(self.data.keys())
        for i in range(len(key_list)):
            polynomials[str(i)] = self.data[key_list[i]]
        for i in range(len(polynomials)):
            index = str(i)
            for j in range(i - 1, -1, -1):
                index = str(j) + index
                p_numerator1 = (x - key_list[int(index[0])]) * polynomials[index[1:]]
                p_numerator2 = (x - key_list[int(index[-1])]) * polynomials[index[:-1]]
                p_denominator = key_list[int(index[-1])] - key_list[int(index[0])]
                polynomials[index] = (p_numerator1 - p_numerator2) / p_denominator
        final_index = ""
        for i in range(len(self.data.keys())):
            final_index += str(i)
        return polynomials[final_index]

    def newton_coefficients(self):
        # This function only calculates the coefficients d, the polynomial itself should be:
        # y = d0 + d1*(t - t0) + d2*(t - t0)*(t - t1) ...
        # -> Until coefficient dn
        d = {}
        key_list = list(self.data.keys())
        for i in range(len(key_list)):
            d[str(i)] = self.data[key_list[i]]
        for i in range(len(d)):
            index = str(i)
            for j in range(i - 1, -1, -1):
                index = str(j) + index
                d[index] = ((d[index[1:]] - d[index[:-1]])/
                            (key_list[int(index[-1])] - key_list[int(index[0])]))
        index = ""
        coefficients = []
        for i in range(len(key_list)):
            index += str(i)
            coefficients.append(d[index])
        return coefficients

    def newton(self, x: float):
        # Calculation method already mentioned in function above
        coefficients = self.newton_coefficients()
        res = 0
        t = list(self.data.keys())
        for i in range(len(coefficients)):
            term = coefficients[i]
            for j in range(i):
                term *= (x - t[j])
            res += term
        return res








