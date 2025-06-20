from isogeny_curve import curve, sidh
from zk_protocol import utility
import random
import cypari
pari = cypari.pari
pari.allocatemem(1024 * 1024 * 1024)
c = curve.create_curve(2, 4, 3, 3, 1)
params = sidh.create_params(2, 4, 3, 3, c.P_a, c.Q_a, c.P_b, c.Q_b)
E = c.elli_curve

def sidh_ladder(h):
    E00 = c.elli_curve
    P_a = c.P_a
    Q_a = c.Q_a
    P_b = c.P_b
    Q_b = c.Q_b
    E_chain = [E00]  # bottom-left chain
    top_chain = []  # top-right chain
    P_a_chain = [P_a]
    Q_a_chain = [Q_a]
    P_b_chain = [P_b]
    Q_b_chain = [Q_b]
    alice_horizontal = []  # Alice's horizontal isogeny chain

    # Single secret kernel point for Alice
    sk_a = c.l_a * random.randint(0, c.l_a ** (c.e_a - 1) - 1)
    S_a = pari.elladd(E00, c.P_a, pari.ellmul(E00, c.Q_a, sk_a))
    G_i = S_a  # Alice's kernel at level 0
    #print("Initial kernel: ", G_i)
    G_i_chain = [G_i]  # Alice's kernel chain

    for i in range(h):
        #print(f"Step {i}: constructing square isogeny...")
        E_i0 = E_chain[-1]  # current lower-left curve
        P_a = P_a_chain[-1]
        Q_a = Q_a_chain[-1]
        P_b = P_b_chain[-1]  # current lower-left point
        Q_b = Q_b_chain[-1]

        # Bob’s vertical isogeny (E_i0 → E_{i+1,0})
        sk_b = c.l_b * random.randint(0, c.l_b ** (c.e_b - 1) - 1)
        S_b = pari.elladd(E_i0, P_b, pari.ellmul(E_i0, Q_b, sk_b))
        # replace heavy iso comp with isogeny_walk
        psi_i = pari.ellisogeny(E_i0, S_b)
        E_i1 = pari.ellinit(psi_i[0], c.gen_fp2)  # E_{i+1,0}
        E_chain.append(E_i1)

        # Push Alice's kernel G_i forward through ψ_i
        G_i_pushed = pari.ellisogenyapply(psi_i[1], G_i)
        # print("G_i_pushed: ", G_i_pushed)
        # Check if G_i_pushed is on E_{i+1,0}
        #print("Alice point: ", pari.ellisoncurve(E_i1, G_i_pushed))
        # Alice’s horizontal isogeny on E_{i+1,0} using pushed kernel
        phi_i = pari.ellisogeny(E_i1, G_i_pushed)
        E_i1_top = pari.ellinit(phi_i[0], c.gen_fp2)  # E'_{i+1,0}
        # print("Top curve: ", E_i1_top.j())
        top_chain.append(E_i1_top)

        P_b_new = pari.ellisogenyapply(psi_i[1], P_b)
        Q_b_new = pari.ellisogenyapply(psi_i[1], Q_b)
        P_b_chain.append(P_b_new)
        Q_b_chain.append(Q_b_new)

        # bob share
        P_b_top = pari.ellisogenyapply(phi_i[1], P_b_new)
        Q_b_top = pari.ellisogenyapply(phi_i[1], Q_b_new)
        S_b_top = pari.elladd(E_i1_top, P_b_top, pari.ellmul(E_i1_top, Q_b_top, sk_b))

        psi_i_prime = pari.ellisogeny(E_i1_top, S_b_top)
        E_i1_top_shared = pari.ellinit(psi_i_prime[0], c.gen_fp2)
        top_chain.append(E_i1_top_shared)

        # Alice share
        P_a_new = pari.ellisogenyapply(psi_i[1], P_a)
        Q_a_new = pari.ellisogenyapply(psi_i[1], Q_a)
        P_a_chain.append(P_a_new)
        Q_a_chain.append(Q_a_new)
        S_a_pushed = pari.elladd(E_i1, P_a_chain[-1], pari.ellmul(E_i1, Q_a_chain[-1], sk_a))
        # Check if S_a_pushed is on E_i1
        # print("Alice point: ", pari.ellisoncurve(E_i1, S_a_pushed))
        phi_i_prime = pari.ellisogeny(E_i1, S_a_pushed)
        E_i1_shared = pari.ellinit(phi_i_prime[0], c.gen_fp2)

        # check commutativity of SIDH square
        # print("E_i1: ", E_i1.j())
        # print("E_i1_top: ", E_i1_top.j())
        # print("E_i1_shared: ", E_i1_shared.j())
        # print("E_i1_top_shared: ", E_i1_top_shared.j())
        # print("shared curves?: ", E_i1_shared.j() == E_i1_top_shared.j())

        # Update Alice's kernel for next square
        G_i = G_i_pushed
        S_b = S_b_top

        #print(f"Step {i}: square isogeny constructed.")
    return E_chain[-1], psi_i, top_chain[-1], psi_i_prime, phi_i_prime
