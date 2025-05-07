from zk_protocol import utility
from zk_protocol.sidh_ladders import ladder


# import cypari
# pari = cypari.pari
# c = curve.create_curve(2, 18, 3, 13, 1)
# params = sidh.create_params(2, 18, 3, 13, c.P_a, c.Q_a, c.P_b, c.Q_b)
# E = c.elli_curve

def p1(chall):  # E0, E1, phi, n, c, params
    h = 10
    sidh_ladder = ladder.sidh_ladder(h)
    # print("ladder: ", sidh_ladder)
    r2 = utility.generate_random_binary_string(2 * 256)
    r3 = utility.generate_random_binary_string(2 * 256)
    com2 = utility.hash_commitment(sidh_ladder[0], r2)
    com3 = utility.hash_commitment(sidh_ladder[2], r3)
    print("com2: ", com2, "\ncom3: ", com3)
    # return com2, com3

# def p2(chall):
    if chall == -1:
        resp = (com2, sidh_ladder[1], sidh_ladder[0], r2)
        return resp
    elif chall == 1:
        resp = (com3, sidh_ladder[3], sidh_ladder[2], r3)
        return resp
    elif chall == 0:
        resp = (com2, com3, sidh_ladder[4], sidh_ladder[0], r2, sidh_ladder[2], r3)
        return resp
    else:
        raise ValueError("Invalid challenge value")

# print(p1(-1))
