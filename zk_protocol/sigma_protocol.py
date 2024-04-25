from isogeny_curve import sidh
from isogeny_curve import curve
import utility
import secrets
import time
import cypari
pari = cypari.pari


# prover commitment
def prover(c, chal):
    # commitment ############################################################
    A = sidh.SIDH("A")
    B = sidh.SIDH("B")
    secretA = A.shared_secret(B)
    secretB = B.shared_secret(A)

    P_2, Q_2 = curve.random_bases(B.pub_key[0], c.l_b, c.e_b, c.P_b, c.Q_b)
    P_3, Q_3 = pari.ellisogenyapply(secretA[0][1], P_2), pari.ellisogenyapply(secretA[0][1], Q_2)
    mul = pari.ellmul(A.pub_key[0], A.pub_key[2], B.s_key)
    S = pari.elladd(A.pub_key[0], A.pub_key[1], mul)

    # E_3, K, P_3, Q_3 = sidh.isogeny_walk(secretB[0], B.pub_key[1], c.l_b, c.e_b, P_2, Q_2)
    # if E_3.j() == secretB[0].j():
    #     print("Curves are the same")

    kernel_point_E_2_E_0 = curve.get_random_point(A.pub_key[0], c.l_b, c.e_b, P_2, Q_2, rand_sample=True)
    d = kernel_point_E_2_E_0[1]
    kernel_point_E_3_E_1 = curve.get_random_point(secretB[0][0], c.l_b, c.e_b, P_3, Q_3, rand_sample=True)
    e = kernel_point_E_3_E_1[1]

    r_L = utility.generate_random_binary_string(256)
    r_R = utility.generate_random_binary_string(256)
    r = utility.generate_random_binary_string(256)

    com_2 = (B.pub_key[0], P_2, Q_2)
    com_3 = (secretB[0][0], P_3, Q_3)
    com_L = utility.hash_commitment(com_2, r_L)
    com_R = utility.hash_commitment(com_3, r_R)
    com_prime = utility.hash_commitment((d, e), r)
    com = (com_L, com_R, com_prime)

    # response ############################################################
    if chal == 1:
        z = secrets.randbelow(c.l_a ** c.e_a - 1)
        # print(secretB)

        k_phi_prime = secretA[1]
        # k_phi_prime = pari.ellmul(secretA[0][0], k_phi, z)
        # k_phi_prime = pari.ellisogenyapply(B.pub_key[3], A.pub_key[4])
        # print("K_phi_prime: ", k_phi_prime)
        #order = pari.ellorder(secretA[0][0], k_phi_prime)
        # print("Order of K_phi_prime: ", order)

        resp = (com_2, r_L, k_phi_prime, com_3, r_R)
        return com, resp
    else:
        if chal == 0:
            resp = (com_3, r_R, d, e, r)
            return com, resp
        else:
            resp = (com_2, r_L, d, e, r)
            return com, resp


def challenge():
    return secrets.choice([-1, 0, 1])


def verify(p, chal):
    com = p[0]
    print("Verifying based on challenge:", chal)

    if chal == 1:
        resp = p[1]
        com_2 = p[1][0]
        com_3 = p[1][3]
        if utility.hash_commitment(com_2, resp[1]) != (com[0]) or \
                utility.hash_commitment(com_3, resp[4]) != (com[1]):
            return False
        E_2_E_3 = sidh.isogeny_walk(com_2[0], resp[2], c.l_a, c.e_a)
        if E_2_E_3[0].j() == com_3[0].j():
            if com_3[1] == pari.ellisogenyapply(E_2_E_3[1], com_2[1]) and \
                    com_3[2] == pari.ellisogenyapply(E_2_E_3[1], com_2[2]):
                return True
            else:
                return False

    elif chal == 0:
        resp = p[1]
        com_3 = p[1][0]
        if utility.hash_commitment(com_3, resp[1]) != (com[1]) or \
                utility.hash_commitment((resp[2], resp[3]), resp[4]) != (com[2]):
            print("response rejected: ", com)
            return False
        # calculate dual kernel point
        # if statement to check if calculated secret curve is equal to the curve sent by the prover
        return False

    elif chal == -1:
        resp = p[1]
        com_2 = p[1][0]
        if utility.hash_commitment(com_2, resp[1]) != (com[0]) or \
                utility.hash_commitment((resp[2], resp[3]), resp[4]) != (com[2]):
            print("response rejected: ", com)
            return False
        # calculate dual kernel point
        # check if calculated secret curve is equal to the curve sent by the prover
        return False


def sigma_protocol():
    for i in range(10):
        chal = challenge()
        #chal = 1
        p = prover(c, chal)
        v = verify(p, chal)
        if not v:
            return "response rejected"
    return "response accepted"


t_0 = time.perf_counter()
c = sidh.c
params = sidh.params
print("-------------------")
print(sigma_protocol())
t_1 = time.perf_counter()
print("Time taken:", t_1 - t_0)
print("-------------------")
