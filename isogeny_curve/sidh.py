import random
import curve as c
import cypari
pari = cypari.pari


# create a dict to store base points and primes for A and B
def create_params(l_a, e_a, l_b, e_b, P_a, Q_a, P_b, Q_b):
    # P_a, Q_a, P_b, Q_b = generate_base_points(elli_curve)
    param_dict = {"A": [l_a, e_a, P_a, Q_a],
                  "B": [l_b, e_b, P_b, Q_b]}
    return param_dict


# compute an isogeny from base curve to E_prime (E -> E')
def isogeny_walk(E, P):
    return True


class SIDH:
    def __init__(self, agent):
        self.agent = agent
        self.l = params[agent][0]
        self.e = params[agent][1]
        self.P = params[agent][2]
        self.Q = params[agent][3]
        self.s_key = random.randint(0, self.l ** self.e)
        self.S = self.P + self.s_key * self.Q
        self.pub_key = self.public_key(self.get_other_agent(self.agent))

    def __str__(self):
        return f"l: {self.l}, e: {self.e}\n" \
                f"P: {self.P}\n" \
                f"Q: {self.Q}\n"

    def get_other_agent(self, agent):
        if self.agent == "A":
            return params["B"]
        else:
            return params["A"]

    def public_key(self, other_agent):
        return isogeny_walk(c.elli_curve, c.P_a)


c = c.create_curve(2, 4, 3, 3, 1)
print(c.__str__())
params = create_params(c.l_a, c.e_a, c.l_b, c.e_b, c.P_a, c.Q_a, c.P_b, c.Q_b)
sidh = SIDH("B")
print(sidh.__str__())


