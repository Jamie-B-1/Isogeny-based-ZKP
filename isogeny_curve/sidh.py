import random
from isogeny_curve import curve
import cypari
pari = cypari.pari


# create a dict to store base points and primes for A and B
def create_params(l_a, e_a, l_b, e_b, P_a, Q_a, P_b, Q_b):
    param_dict = {"A": [l_a, e_a, P_a, Q_a],
                  "B": [l_b, e_b, P_b, Q_b]}
    return param_dict


# compute an isogeny from base curve to E_prime (E -> E')
def isogeny_walk(E, S, l, e, P_prime=None, Q_prime=None):
    # finite field from base curve
    ff = c.gen_fp2
    for i in range(e):
        scalar = l ** (e - i - 1)
        # compute the kernel of the isogeny
        R = pari.ellmul(E, S, scalar)
        # new curve E' and isogeny from E to E'
        [E_prime, ff_prime] = pari.ellisogeny(E, R)
        # apply the isogeny from E to E'
        E = pari.ellinit(E_prime, ff)
        S = pari.ellisogenyapply(ff_prime, S)
        if P_prime is not None and Q_prime is not None:
            P_prime = pari.ellisogenyapply(ff_prime, P_prime)
            Q_prime = pari.ellisogenyapply(ff_prime, Q_prime)
    if P_prime is not None and Q_prime is not None:
        return E, P_prime, Q_prime, ff_prime, R
    return E, ff_prime, R



class SIDH:
    def __init__(self, agent):
        self.agent = agent
        self.l = params[agent][0]
        self.e = params[agent][1]
        self.P = params[agent][2]
        self.Q = params[agent][3]
        # sample a random l-torsion point multiplied by l: [2m']
        self.s_key = self.l * random.randint(0, self.l ** (self.e-1)-1)
        # Generator for a secret S : self.S = self.P + self.s_key * self.Q
        # point addition and multiplication to generate S above
        s_mul = pari.ellmul(c.elli_curve, self.Q, self.s_key)
        # S = P + [2m']Q
        self.S = pari.elladd(c.elli_curve, self.P, s_mul)
        # public key computed in isogeny walk from E to E'
        self.pub_key = self.public_key(self.get_other_agent())

    def __str__(self):
        return f"l: {self.l}, e: {self.e}\n" \
                f"P: {self.P}\n" \
                f"Q: {self.Q}\n" \
                f"s_key: {self.s_key}\n" \
                f"S: {self.S}\n" \
                f"pub_key: {self.pub_key}\n"

    def get_other_agent(self):
        if self.agent == "A":
            return params["B"]
        elif self.agent == "B":
            return params["A"]
        else:
            raise ValueError("Invalid agent")

    def public_key(self, other_agent):
        return isogeny_walk(c.elli_curve, self.S, self.l, self.e, other_agent[2], other_agent[3])

    def shared_secret(self, other):
        # S = other_agent.pub_key[1] + self.s_key * other_agent.pub_key[2]
        mul = pari.ellmul(other.pub_key[0], other.pub_key[2], self.s_key)
        S = pari.elladd(other.pub_key[0], other.pub_key[1], mul)
        # compute the isogeny walk E_a -> E_ab, E_b -> E_ba
        shared_curve = isogeny_walk(other.pub_key[0], S, self.l, self.e)
        # print(shared_curve.j())
        # return the j-invariant of the shared curve: shared secret
        return shared_curve, S


c = curve.create_curve(2, 216, 3, 137, 1)
# print(c.__str__())
params = create_params(c.l_a, c.e_a, c.l_b, c.e_b, c.P_a, c.Q_a, c.P_b, c.Q_b)
# print(sidh.__str__())


