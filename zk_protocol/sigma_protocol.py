from isogeny_curve import sidh
from isogeny_curve import curve
import cypari
pari = cypari.pari


# prover commitment
def commitment():
    R_1 = curve.get_random_point(c.elli_curve, c.l_a, c.e_a, c.P_a, c.Q_a)
    E_2, K = sidh.isogeny_walk(c.elli_curve, R_1, c.l_a, c.e_a)
    P_2, Q_2 = curve.random_bases(E_2, c.l_a, c.e_a, c.P_a, c.Q_a)
    E_3, K_2, P_3, Q_3 = sidh.isogeny_walk(E_2, K, c.l_a, c.e_a, P_2, Q_2)
    return E_2, P_2, Q_2, E_3, P_3, Q_3


c = sidh.c
print("curve E0: ", c.__str__(), "\n-------------------")
params = sidh.params
# A = sidh.SIDH("A")
# B = sidh.SIDH("B")
# secretA = A.shared_secret(B)
# secretB = B.shared_secret(A)
# if secretA == secretB:
#     print("Shared secret is the same")
print(commitment())
print("-------------------")
