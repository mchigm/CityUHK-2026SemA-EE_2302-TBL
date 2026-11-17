import math

N1 = 40392231078347531512910276534143208818556780344331842048962992250205863463
N2 = 27443073907224807047208410121753755861810079669054509912076998855656890551

C1 = 15798163726688799865298793159527866026064727574458206448895609201487845728
C2 = 2932532981980128948769959383980604991085405839595353680899824460306979443

# 1. Check gcd(N1, N2)
assert math.gcd(N1, N2) == 1, "Moduli share a factor!"

# 2. Chinese Remainder Theorem for two moduli
inv_N1 = pow(N1, -1, N2)
X = (C1 + N1 * ((C2 - C1) * inv_N1 % N2)) % (N1 * N2)

# 3. Exact integer cube root via binary search


def integer_cube_root(n):
    low, high = 0, 1 << ((n.bit_length() + 2) // 3)
    while low < high:
        mid = (low + high + 1) // 2
        if mid ** 3 <= n:
            low = mid
        else:
            high = mid - 1
    return low


M = integer_cube_root(X)

# 4. Verify exact cube and 35-digit length
assert M ** 3 == X, "X is not a perfect cube!"
assert len(str(M)) == 35, f"Unexpected digit length: {len(str(M))}"

print("Recovered 35-digit Emergency Access Code M:", M)
