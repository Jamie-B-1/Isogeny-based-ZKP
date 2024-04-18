from isogeny_curve import sidh
from isogeny_curve import curve
import utility
import secrets
import cypari
pari = cypari.pari


# prover commitment
def prover(c, chal):
    # commitment ############################################################
    # A = sidh.SIDH("A")
    # B = sidh.SIDH("B")
    # secretA = A.shared_secret(B)
    # secretB = B.shared_secret(A)

    P_2, Q_2 = curve.random_bases(B.pub_key[0], c.l_b, c.e_b, c.P_b, c.Q_b)
    mul = pari.ellmul(A.pub_key[0], A.pub_key[2], B.s_key)
    S = pari.elladd(A.pub_key[0], A.pub_key[1], mul)

    E_3, K, P_3, Q_3 = sidh.isogeny_walk(secretB[0], B.pub_key[1], c.l_b, c.e_b, P_2, Q_2)
    if E_3.j() == secretB[0].j():
        print("Curves are the same")

    kernel_point_E_2_E_0 = curve.get_random_point(A.pub_key[0], c.l_b, c.e_b, P_2, Q_2, rand_sample=True)
    d = kernel_point_E_2_E_0[1]
    kernel_point_E_3_E_1 = curve.get_random_point(E_3, c.l_b, c.e_b, P_3, Q_3, rand_sample=True)
    e = kernel_point_E_3_E_1[1]

    r_L = utility.generate_random_binary_string(256)
    r_R = utility.generate_random_binary_string(256)
    r = utility.generate_random_binary_string(256)

    com_2 = (B.pub_key[0], P_2, Q_2)
    com_3 = (E_3, P_3, Q_3)
    com_L = utility.hash_commitment(com_2, r_L)
    com_R = utility.hash_commitment(com_3, r_R)
    com_prime = utility.hash_commitment((d, e), r)
    com = (com_L, com_R, com_prime)

    # response ############################################################
    if chal == 1:
        z = random.randint(0, c.l_a**(c.e_a-1))
        print(secretB)
        k_phi_prime = pari.ellmul(secretB[0], secretB[1], z)
        resp = (com_L, r_L, k_phi_prime, com_R, r_R)
        return com, resp
    else:
        if chal == 0:
            resp = (com_R, r_R, d, e, r)
            return resp
        else:
            resp = (com_L, r_L, d, e, r)
            return resp


def challenge():
    return secrets.choice([-1, 0, 1])


def verify(p, chal):
    com = p
    if chal == 1:
        print("commitment and response: ", com)
    else:
        return



def sigma_protocol():
    chal = challenge()
    p = prover(c, chal)
    verify(p, chal)
    return p

c = sidh.c
print("curve E0: ", c.__str__(), "\n-------------------")
params = sidh.params
A = sidh.SIDH("A")
B = sidh.SIDH("B")
secretA = A.shared_secret(B)
secretB = B.shared_secret(A)
if secretA == secretB:
    print("Shared secret is the same")
# print(commitment(c))
print(sigma_protocol())
print("-------------------")
