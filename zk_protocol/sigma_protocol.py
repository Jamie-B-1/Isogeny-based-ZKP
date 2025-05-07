from isogeny_curve import sidh
from isogeny_curve import curve
from zk_protocol import utility
import secrets
import time
import cypari
pari = cypari.pari


# prover commitment
def prover(c, params, chal):
    # commitment ############################################################
    A = sidh.SIDH("A", c.elli_curve, params, c)
    B = sidh.SIDH("B", c.elli_curve, params, c)
    secretA = A.shared_secret(B, c)
    secretB = B.shared_secret(A, c)

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

    r_L = utility.generate_random_binary_string(2*256)
    r_R = utility.generate_random_binary_string(2*256)
    r = utility.generate_random_binary_string(2*256)

    com_2 = (B.pub_key, P_2, Q_2)
    com_3 = (secretB[0], P_3, Q_3)
    com_L = utility.hash_commitment(com_2, r_L)
    com_R = utility.hash_commitment(com_3, r_R)
    com_prime = utility.hash_commitment((d, e), r)
    com = (com_L, com_R, com_prime)

    # response ############################################################
    if chal == -1:
        resp = (com_2, r_L, d, e, r)
        return com, resp
    elif chal == 0:
        resp = (com_3, r_R, d, e, r)
        return com, resp
    else:
        z = secrets.randbelow(c.l_a ** c.e_a - 1)
        # print(secretB)

        k_phi_prime = secretA[1]
        # k_phi_prime = pari.ellmul(secretA[0][0], k_phi, z)
        # k_phi_prime = pari.ellisogenyapply(B.pub_key[3], A.pub_key[4])
        # print("K_phi_prime: ", k_phi_prime)
        # order = pari.ellorder(secretA[0][0], k_phi_prime)
        # print("Order of K_phi_prime: ", order)
        resp = (com_2, r_L, k_phi_prime, com_3, r_R)
        return com, resp


def challenge():
    return secrets.choice([-1, 0, 1])


def verify(c, p, chal):
    com = p[0]
    print("Verifying based on challenge:", chal)

    if chal == -1:
        resp = p[1]
        com_2 = p[1][0]
        if utility.hash_commitment(com_2, resp[1]) != (com[0]) or \
                utility.hash_commitment((resp[2], resp[3]), resp[4]) != (com[2]):
            print("response rejected: ", com)
            return 0
        return 1
        # calculate dual kernel point
        # calculate isogeny from E2 to E0
        ################################################
        # P_2 = resp[0][1]
        # Q_2 = resp[0][2]
        # d = resp[2]
        # a = d[0]
        # print(d)
        # e = resp[3]
        # b = e[0]
        # print(e)
        # psi_hat = pari.elladd(c.elli_curve, pari.ellmul(c.elli_curve, P_2, a), pari.ellmul(c.elli_curve, Q_2, b))
        # # psi_hat = pari.ellmul(c.elli_curve, P_2, d)
        # print(psi_hat)
        # [E_dual_prime, phi_dual] = pari.ellisogeny(c.elli_curve, psi_hat)
        # E_dual_prime = pari.ellinit(E_dual_prime, c.gen_fp2)
        #
        # #E_2_E_0 = sidh.isogeny_walk(com_2[0], psi_hat, c.l_a, c.e_a, c, P_2, Q_2)
        # # check if calculated secret curve is equal to the curve sent by the prover
        # if E_dual_prime == c.elli_curve:
        #     return True
        # else:
        #     return False

    elif chal == 0:
        resp = p[1]
        com_3 = p[1][0]
        if utility.hash_commitment(com_3, resp[1]) != (com[1]) or \
                utility.hash_commitment((resp[2], resp[3]), resp[4]) != (com[2]):
            print("response rejected: ", com)
            return 0
        # calculate dual kernel point

        # calculate isogeny from E3 to E1

        # phi_hat = pari.ellisogenyapply(com_3[0][1], resp[3])
        # # dual_E_3_E_1 = dual_isogeny(c, com_3)
        #
        #
        # E_3_E_1 = sidh.isogeny_walk(com_3[0][0], phi_hat, c.l_a, c.e_a, c)
        # print(E_3_E_1, E_3_E_1[0].j(), com_3[0][0].j())
        # dual = dual_isogeny(c, (com_3, resp[2], resp[3]))
        # if statement to check if calculated secret curve is equal to the curve sent by the prover
        # if E_3_E_1[0] == com_3[0][0]:
        #     return True
        # else:
        #     return False
        return 1

    elif chal == 1:
        resp = p[1]
        com_2 = p[1][0]
        com_3 = p[1][3]
        if utility.hash_commitment(com_2, resp[1]) != (com[0]) or \
                utility.hash_commitment(com_3, resp[4]) != (com[1]):
            return 0
        if pari.ellmul(com_2[0][0], resp[2], c.order) != 0:
            return 0
        E_2_E_3 = sidh.isogeny_walk(com_2[0][0], resp[2], c.l_a, c.e_a, c)
        if E_2_E_3[0].j() == com_3[0][0].j():
            print("j-invariant: ", E_2_E_3[0].j(), "j-invariant: ", com_3[0][0].j())
            if com_3[1] == pari.ellisogenyapply(E_2_E_3[1], com_2[1]) and \
                    com_3[2] == pari.ellisogenyapply(E_2_E_3[1], com_2[2]):
                return 1
            else:
                return 0
    else:
        # invalid challenge
        return 0


def sigma_protocol(c, params, k):
    for i in range(k):
        chal = challenge()
        #chal = 1
        p = prover(c, params, chal)
        v = verify(c, p, chal)
        if not v:
            return "response rejected"
    return "response accepted"


def main(k):
    # c = curve.create_curve(2, 4, 3, 3, 1)
    # c = curve.create_curve(2, 18, 3, 13, 1)
    c = curve.create_curve(2, 216, 3, 137, 1)
    params = sidh.create_params(c.l_a, c.e_a, c.l_b, c.e_b, c.P_a, c.Q_a, c.P_b, c.Q_b)
    print("-------------------")
    print(sigma_protocol(c, params, k))
    print("-------------------")


if __name__ == "__main__":
    # number of iterations
    iterations = int(input("Enter number of iterations: "))
    t_0 = time.perf_counter()
    main(iterations)
    t_1 = time.perf_counter()
    print("Time taken:", t_1 - t_0)
