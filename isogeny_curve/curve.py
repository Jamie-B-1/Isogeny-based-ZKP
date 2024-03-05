# cypari is a Python wrapper for the PARI/GP library
# methods for elliptic curve isogenies are on page 97 of the docs
# cypari works on Windows and cypari2 works on linux
# https://cypari2.readthedocs.io/_/downloads/en/latest/pdf/

import cypari
# initialise pari variable
pari = cypari.pari


class CurveStruct:

    # initialise the curve structure
    def __init__(self, l_a, e_a, l_b, e_b, cofactor, p, gen_fp2, elli_curve, P_a, Q_a, P_b, Q_b):
        # l_a: small prime, e_a: exponent
        self.l_a, self.e_a = l_a, e_a
        # l_b: small prime, e_b: exponent
        self.l_b, self.e_b = l_b, e_b
        # cofactor ensures p is prime
        self.cofactor = cofactor
        # prime number of form: p = l_a^e_a * l_b^e_b * cofactor - 1
        self.p = p
        # generator of the field GF(p^2)
        self.gen_fp2 = gen_fp2
        # supersingular elliptic curve
        self.elli_curve = elli_curve
        # points to generate E[l_a^e_a]
        self.P_a = P_a
        self.Q_a = Q_a
        # points to generate E[l_b^e_b]
        self.P_b = P_b
        self.Q_b = Q_b

    # print the curve structure
    def __str__(self):
        return f"l_a: {self.l_a}, e_a: {self.e_a}\n" \
                f"l_b: {self.l_b}, e_b: {self.e_b}\n" \
                f"cofactor: {self.cofactor}\n" \
                f"p: {self.p}\n" \
                f"gen_fp2: {self.gen_fp2}\n" \
                f"elli_curve: {self.elli_curve}\n" \
                f"P_a: {self.P_a}\n" \
                f"Q_a: {self.Q_a}\n" \
                f"P_b: {self.P_b}\n" \
                f"Q_b: {self.Q_b}\n"


# generate random base points for a and b
def generate_base_points():
    return


# walk through the steps of the isogeny
def isogeny_walk():
    return


# create a supersingular elliptic curve
def create_curve(l_a, e_a, l_b, e_b, cofactor):
    # prime number of form: p = l_a^e_a * l_b^e_b * cofactor - 1
    p = pari(l_a ** e_a * l_b ** e_b * cofactor - 1)
    # generator of the field GF(p^2)
    gen_fp2 = pari(f"ffgen(ffinit({p}, 2), 'i)")
    x = gen_fp2
    # supersingular elliptic curve
    elli_curve = pari(f"ellinit([{x}, 0])")
    # initialise base points
    # P_a = pari(f"ellmul({l_a ** e_a}, elli_curve, {x})")
    # Q_a = pari(f"ellmul({l_a ** (e_a - 1)}, P_a, {x})")
    # P_b = pari(f"ellmul({l_b ** e_b}, elli_curve, {x})")
    # Q_b = pari(f"ellmul({l_b ** (e_b - 1)}, P_b), {x})")

    return CurveStruct(l_a, e_a, l_b, e_b, cofactor, p, gen_fp2, elli_curve, None, None, None, None)


# create a supersingular elliptic curve
curve = create_curve(2, 4, 3, 3, 1)
curve.__str__()
print(curve)
