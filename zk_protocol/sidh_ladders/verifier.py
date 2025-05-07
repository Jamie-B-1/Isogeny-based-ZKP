import secrets

from zk_protocol import utility
from zk_protocol.sidh_ladders.prover import p1

def v(chall, resp):
    """
        Verifies the response from the prover based on the challenge value.
        @param chall: challenge value (-1, 0, 1)
        @param resp: response from prover containing values committed corresponding to each challenge
        @return: 1 if verification passes, 0 otherwise
    """
    if chall == -1:
        com2 = resp[0]
        # make response
        if utility.hash_commitment(resp[2], resp[3]) == com2:
            print("E2 j-invariant: ", resp[2].j())
            return 1
        # check psi is an l^n isogeny E0->E2
        return 0

    elif chall == 1:
        com3 = resp[0]
        # make response
        if utility.hash_commitment(resp[2], resp[3]) == com3:
            print("E3 j-invariant: ", resp[2].j())
            return 1
        # check psi_prime is an l^n isogeny E1->E3
        return 0

    elif chall == 0:
        com2 = resp[0]
        com3 = resp[1]
        # make response
        if utility.hash_commitment(resp[3], resp[4]) == com2 and \
                utility.hash_commitment(resp[5], resp[6]) == com3:
            print("E2 j-invariant: ", resp[3].j())
            print("E3 j-invariant: ", resp[5].j())
            return 1
        # check com2 == C(E2,r2)
        # check com3 == C(E3,r3)
        # check phi_prime is an l^n isogeny E2->E3
        return 0

    else:
        raise ValueError("Invalid challenge value")


if __name__ == "__main__":
    # Example usage
    # c = curve.create_curve(2, 18, 3, 13, 1)
    # params = sidh.create_params(2, 18, 3, 13, c.P_a, c.Q_a, c.P_b, c.Q_b)
    # E = c.elli_curve
    chall = secrets.choice([-1, 0, 1])
    print("Challenge: ", chall)
    p = p1(chall)
    print("Prover response: ", p)
    result = v(chall, p)
    print("Verification result: ", result)
