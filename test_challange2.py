import math
from sympy import factorint
from sympy.ntheory.modular import crt

p = 500210000000000000000003801597
g = 282132810916179194351197318808
K_A = 488889094949725227665344694903
K_B = 128397645192957567210582962139


def bsgs(base, target, mod, order):
    """Baby-Step Giant-Step for subgroup of known prime order."""
    m = math.isqrt(order) + 1
    baby = {}
    cur = 1
    for j in range(m):
        baby[cur] = j
        cur = (cur * base) % mod
    factor = pow(base, -m, mod)
    gamma = target
    for i in range(m):
        if gamma in baby:
            return i * m + baby[gamma]
        gamma = (gamma * factor) % mod
    raise ValueError("DLP not found")


def solve_prime_power(g, h, p, q, e):
    """Solve g^x = h (mod p) in subgroup of order q^e."""
    x = 0
    g_base = pow(g, (p - 1) // q, p)
    for k in range(e):
        exp = (p - 1) // (q ** (k + 1))
        h_k = (pow(h, exp, p) * pow(g, -x * exp, p)) % p
        d_k = bsgs(g_base, h_k, p, q)
        x += d_k * (q ** k)
    return x


factors = factorint(p - 1)
print("Factors of p - 1:", factors)

moduli = []
remainders_a = []
remainders_b = []

for q, e in factors.items():
    pe = q ** e
    moduli.append(pe)
    remainders_a.append(solve_prime_power(g, K_A, p, q, e))
    remainders_b.append(solve_prime_power(g, K_B, p, q, e))

a, order = crt(moduli, remainders_a)
b, _ = crt(moduli, remainders_b)

assert pow(g, int(a), p) == K_A
assert pow(g, int(b), p) == K_B

S1 = pow(K_B, int(a), p)
S2 = pow(K_A, int(b), p)
assert S1 == S2
print("Shared Secret S:", S1)
