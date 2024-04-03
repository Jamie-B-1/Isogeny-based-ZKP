# cypari is a Python wrapper for the PARI/GP library
# methods for elliptic curve isogenies are on page 97 of the docs
# cypari works on Windows and cypari2 works on linux
# https://cypari2.readthedocs.io/_/downloads/en/latest/pdf/

import cypari
# initialise pari variable
pari = cypari.pari


class CurveStruct:

    # initialise the curve structure
    def __init__(self, l_a, e_a, l_b, e_b, cofactor, p, gen_fp2, elli_curve, P_1, Q_1, P_2, Q_2):
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
        self.P_1 = P_1
        self.Q_1 = Q_1
        # points to generate E[l_b^e_b]
        self.P_2 = P_2
        self.Q_2 = Q_2

    # print the curve structure
    def __str__(self):
        return f"l_a: {self.l_a}, e_a: {self.e_a}\n" \
                f"l_b: {self.l_b}, e_b: {self.e_b}\n" \
                f"cofactor: {self.cofactor}\n" \
                f"p: {self.p}\n" \
                f"gen_fp2: {self.gen_fp2}\n" \
                f"elli_curve: {self.elli_curve}\n" \
                f"P_a: {self.P_1}\n" \
                f"Q_a: {self.Q_1}\n" \
                f"P_b: {self.P_2}\n" \
                f"Q_b: {self.Q_2}\n"


def generate_base_points(elli_curve):
    P, Q = pari.ellgenerators(elli_curve)
    return P, Q


# walk through the steps of the isogeny
def isogeny_walk():
    return


# create a supersingular elliptic starting curve
def create_curve(l_a, e_a, l_b, e_b, cofactor):
    # prime number of form: p = l_a^e_a * l_b^e_b * cofactor - 1
    p = pari(l_a ** e_a * l_b ** e_b * cofactor - 1)

    # polynomial x^2 + 1, for the field GF(p^2)
    fp = pari(f"ffinit({p}, 2)")
    # generator of the field GF(p^2)
    gen_fp2 = pari(f"ffgen({fp}, 't)")

    # supersingular elliptic curve initialisation
    elli_curve = pari.ellinit([1, 0], gen_fp2)
    # check if elli_curve is a supersingular elliptic curve at p
    if pari.ellissupersingular(elli_curve, p) == 0:
        print("Curve is not supersingular")
        return
    print(f"j-invariant: {str(elli_curve.j())}")
    bases = generate_base_points(elli_curve)
    P_1 = bases[0][0]
    Q_1 = bases[0][1]
    P_2 = bases[1][0]
    Q_2 = bases[1][1]
    return CurveStruct(l_a, e_a, l_b, e_b, cofactor, p, gen_fp2, elli_curve, P_1, Q_1, P_2, Q_2)


# create a supersingular elliptic curve
curve = create_curve(2, 4, 3, 3, 1)
curve.__str__()
print(curve)
