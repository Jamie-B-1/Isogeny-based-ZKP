# cypari is a Python wrapper for the PARI/GP library
# methods for elliptic curve isogenies are on page 97 of the docs
# cypari works on Windows and cypari2 works on linux
# https://cypari2.readthedocs.io/_/downloads/en/latest/pdf/
import secrets
import cypari
# initialise pari variable
pari = cypari.pari


def get_random_point(elli_curve, l, e, P, Q, rand_sample=False):
    # while True:
    # sample a random l-torsion point multiplied by l: [2m']
    m = l * secrets.randbelow(l ** (e - 1))
    # point addition and multiplication to generate R
    s_mul = pari.ellmul(elli_curve, Q, m)
    # R = P + [2m']Q
    R = pari.elladd(elli_curve, P, s_mul)
    if rand_sample:
        return R, m
    return R

def random_bases(elli_curve, l, e, P, Q):
    while True:
        P = get_random_point(elli_curve, l, e, P, Q)
        Q = get_random_point(elli_curve, l, e, P, Q)
        order_P = pari.ellorder(elli_curve, P)
        order_Q = pari.ellorder(elli_curve, Q)
        if order_P % l**e == 0 and order_Q % l**e == 0:
            return P, Q


def generate_base_points(gen_fp2, elli_curve, l_a, e_a, l_b, e_b):
    t = gen_fp2

    P_a = [111 + 311 * t, 247 + 162 * t]  # SIDH parameters for l=2,3 e=4,3
    print("order of P_a for E0: ", pari.ellorder(elli_curve, P_a))
    Q_a = [290 + 176 * t, 29 + 421 * t]
    P_b = [360 + 112 * t, 287 + 146 * t]
    Q_b = [347 + 404 * t, 68 + 176 * t]

    # SIKEp434 parameters
    # P_a = [
    #     15937686683633039019196728742331738441209610167832388917703407269928835422226362845467776102646239486823941673658245515771001898283 +
    #     2003351496878340769927496857888485805825600511617562327658105361759369326590776207465430298367135830995863247764468049749472449827 * t,
    #     17108323619081055472406376613720773413736121124406182472541249873821398922393300545360934897611851130699945176056842470104358654884 +
    #     8337004641788845819131721857290673922295053839933467431582336072726065745705096801632409264717689480409378684646781531582640287399 * t]
    # Q_a = [
    #     15088817061064820268855215031798808081934414602474420517091065419503164076185078899700761543847379884983212295919804932006246031947 +
    #     7804220673805821185818875507282627517813183801913071739476129171353898518782055651068417838573748671068461643818212154265625205666 * t,
    #     3248126327355632307449398910863440627630497001071650448251192432379165836841686224302872841534443206199579057873167957417639551029 +
    #     19507679526450799728438014183641858310821309240412911974764102921372927929916615211429302545241275283904311830918752312996285161807 * t]
    # P_b = [
    #     556274038285849315241897557477215211505102505036877971385691866860361859320408873381354575789101651011570316507766991773952557997 +
    #     16306656024954733221075162754955969260730457357369697629788710022165816786748701612472655217816963254297818152946097129242450733644 * t,
    #     14837889202738555922760869822639160650458519841159771977016139817337716263517812064882918694469258377690642456437323127075249813131 +
    #     3614789590927682028814871604873208458500877330458658745597461397001311907390924812620749562716470922547140320752451448882603082824 * t]
    # Q_b = [
    #     3847144497801108225028716818622358634049600547745572272841246235914612333824083439220341539519730256837264684681979401578390546981 +
    #     8224904841129032115973432646497290185163264395865958574314664346285559445962868006749870180240521074454182724558887407546736075058 * t,
    #     5070201965208378562575304366332945278081481321657317607555997081531054662815938554843891620583341723452310835208486872845165579560 +
    #     5917717394456628336842002186881500641795694051979049336189885252227184440851721545191446902294118704165036223586306979148424339996 * t]

    return P_a, Q_a, P_b, Q_b


# create a supersingular elliptic starting curve
def create_curve(l_a, e_a, l_b, e_b, cofactor):
    # prime number of form: p = l_a^e_a * l_b^e_b * cofactor - 1
    p = pari(l_a ** e_a * l_b ** e_b * cofactor - 1)

    # polynomial x^2 + 1, for the field GF(p^2)
    fp = pari(f"Mod(1, {p})*x^2 + Mod(1, {p})")
    # generator of the field GF(p^2)
    gen_fp2 = pari(f"ffgen({fp}, 'i)")

    # supersingular elliptic curve initialisation
    elli_curve = pari.ellinit([1, 0], gen_fp2)
    # check if elli_curve is a supersingular elliptic curve at p
    if pari.ellissupersingular(elli_curve, p) == 0:
        raise ValueError("Curve is not supersingular")

    P_a, Q_a, P_b, Q_b = generate_base_points(gen_fp2, elli_curve, l_a, e_a, l_b, e_b)

    return CurveStruct(l_a, e_a, l_b, e_b, cofactor, p, gen_fp2, elli_curve, P_a, Q_a, P_b, Q_b)


class CurveStruct:

    # initialise the curve structure
    def __init__(self, l_a, e_a, l_b, e_b, cofactor, p, gen_fp2, elli_curve, P_a, Q_a, P_b, Q_b):
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
        self.P_a = P_a
        self.Q_a = Q_a
        # points to generate E[l_b^e_b]
        self.P_b = P_b
        self.Q_b = Q_b

    # print the curve structure
    def __str__(self):
        return f"l_a: {self.l_a}, e_a: {self.e_a}\n" \
                f"l_b: {self.l_b}, e_b: {self.e_b}\n" \
                f"cofactor: {self.cofactor}\n" \
                f"p: {self.p}\n" \
                f"gen_fp2: {self.gen_fp2}\n" \
                f"elli_curve: {self.elli_curve}\n" \
                f"P_a: {self.P_a}\n" \
                f"Q_a: {self.Q_a}\n" \
                f"P_b: {self.P_b}\n" \
                f"Q_b: {self.Q_b}\n"


# create a supersingular elliptic curve
# curve = create_curve(2, 4, 3, 3, 1)
# curve.__str__()
# print(curve)
