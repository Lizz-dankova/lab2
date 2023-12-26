class BigInt:
    def __init__(self, value=0, base=10, size=2048):
        self.size = size
        self.base = base
        self.value = [0] * size
        if isinstance(value, int):
            self.from_int(value)
        elif isinstance(value, str):
            self.from_str(value)
        elif isinstance(value, list):
            self.value = value[:]

    def from_int(self, num):
        for i in range(self.size):
            self.value[i] = num % self.base
            num //= self.base

    def from_str(self, num_str):
        num_str = num_str[::-1]
        self.value = [int(digit, self.base) for digit in num_str]

    def to_str(self):
        return ''.join([hex(digit)[2:].upper() for digit in reversed(self.value)])

    def from_small_const(self, const):
        self.from_int(const)

    def gcd(self, other):
        # GCD using Euclidean algorithm
        a = self
        b = other

        if b == BigInt():
            return a

        while b != BigInt():
            a, b = b, a % b

        return a

    def lcm(self, other):
        # LCM calculation using GCD
        gcd_ab = self.gcd(other)
        if gcd_ab == BigInt():
            return BigInt()  # LCM is not defined for 0
        else:
            return (self * other) // gcd_ab

    def mod_add(self, other, mod):
        result = self + other
        return result % mod

    def mod_sub(self, other, mod):
        result = self - other
        return result % mod

    def mod_mul(self, other, mod):
        # Modular multiplication using Barrett reduction
        reduction_param = 2
        mu = BigInt((1 << (reduction_param * self.size)) // mod.value[0])
        q1 = (self * other) >> (reduction_param * self.size)
        q2 = mu * (q1 * mod)
        result = (self * other - q2 * mod) % mod
        return result

    def mod_square(self, mod):
        # Modular squaring using Barrett reduction
        reduction_param = 2
        mu = BigInt((1 << (reduction_param * self.size)) // mod.value[0])
        q1 = (self * self) >> (reduction_param * self.size)
        q2 = mu * (q1 * mod)
        result = (self * self - q2 * mod) % mod
        return result

    def mod_pow(self, exponent, mod):
        # Exponentiation using Horner's scheme
        result = BigInt(1)
        base_power = self % mod

        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base_power) % mod
            exponent //= 2
            base_power = (base_power * base_power) % mod

        return result

    def __mod__(self, mod):
        if mod == BigInt() or mod == BigInt(0):
            raise ValueError("Cannot perform modulo operation with zero modulus")

        if self == BigInt():
            return BigInt()  # Return 0 if self is zero

        for digit in self.value:
            if digit != 0:
                break
        else:
            return BigInt()  # Return 0 if the result is zero

        result = BigInt(value=self.value)
        try:
            for j in range(self.size - 1, -1, -1):
                result.value[j] %= mod.value[j]
                if j > 0:
                    borrow = (result.value[j - 1] + result.value[j] * self.base) // mod.value[j]
                    result.value[j - 1] -= borrow
        except ZeroDivisionError:
            raise ValueError("Cannot perform modulo operation with zero modulus")

        return result

    def __add__(self, other):
        result = BigInt()
        carry = 0

        for i in range(self.size):
            temp_sum = self.value[i] + other.value[i] + carry
            result.value[i] = temp_sum % self.base
            carry = temp_sum // self.base

        return result

    def __sub__(self, other):
        result = BigInt()
        borrow = 0

        for i in range(self.size):
            temp_diff = self.value[i] - other.value[i] - borrow
            if temp_diff < 0:
                temp_diff += self.base
                borrow = 1
            else:
                borrow = 0
            result.value[i] = temp_diff

        return result

    def __mul__(self, other):
        result = BigInt()

        for i in range(self.size):
            for j in range(self.size - i):
                result.value[i + j] += self.value[i] * other.value[j]
                result.value[i + j + 1] += result.value[i + j] // self.base
                result.value[i + j] %= self.base

        return result

    def __rshift__(self, shift):
        result = BigInt(value=self.value[shift:])
        return result

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return self.to_str()

# Example usage
a = BigInt(12345)
b = BigInt("67890", base=10)

# GCD and LCM calculation
gcd_ab = a.gcd(b)
lcm_ab = a.lcm(b)
print(f"GCD({a.to_str()}, {b.to_str()}) = {gcd_ab.to_str()}")
print(f"LCM({a.to_str()}, {b.to_str()}) = {lcm_ab.to_str()}")

# Modular operations
modulus = BigInt(100)
mod_add_result = a.mod_add(b, modulus)
mod_sub_result = a.mod_sub(b, modulus)
mod_mul_result = a.mod_mul(b, modulus)
mod_square_result = a.mod_square(modulus)
mod_pow_result = a.mod_pow(3, modulus)

print(f"({a.to_str()} + {b.to_str()}) % 100 = {mod_add_result.to_str()}")
print(f"({a.to_str()} - {b.to_str()}) % 100 = {mod_sub_result.to_str()}")
print(f"({a.to_str()} * {b.to_str()}) % 100 = {mod_mul_result.to_str()}")
print(f"{a.to_str()}^2 % 100 = {mod_square_result.to_str()}")
print(f"{a.to_str()}^3 % 100 = {mod_pow_result.to_str()}")
