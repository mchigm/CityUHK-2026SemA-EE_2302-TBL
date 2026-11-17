ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz "
CHAR_TO_INT = {c: i for i, c in enumerate(ALPHABET)}
INT_TO_CHAR = {i: c for i, c in enumerate(ALPHABET)}
MOD = 53


def encode(s):
    return [CHAR_TO_INT[c] for c in s]


def decode(nums):
    return "".join(INT_TO_CHAR[x % MOD] for x in nums)


def rank_mod(cols, p=53):
    """Compute column rank over F_p."""
    if not cols:
        return 0
    M = [list(col) for col in zip(*cols)]
    rows, ncols = len(M), len(M[0])
    r = 0
    for c in range(ncols):
        pivot = next((i for i in range(r, rows) if M[i][c] % p != 0), None)
        if pivot is None:
            continue
        M[r], M[pivot] = M[pivot], M[r]
        inv_p = pow(M[r][c], -1, p)
        M[r] = [(x * inv_p) % p for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [(M[i][j] - f * M[r][j]) % p for j in range(ncols)]
        r += 1
        if r == rows:
            break
    return r


def mod_inv_matrix(M, p=53):
    n = len(M)
    A = [
        row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(M)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if A[r][col] % p != 0), None)
        if pivot is None:
            return None
        A[col], A[pivot] = A[pivot], A[col]
        inv_piv = pow(A[col][col], -1, p)
        A[col] = [(x * inv_piv) % p for x in A[col]]
        for r in range(n):
            if r != col and A[r][col] != 0:
                factor = A[r][col]
                A[r] = [(A[r][c] - factor * A[col][c]) %
                        p for c in range(2 * n)]
    return [row[n:] for row in A]


def mat_mul_mod(A, B, p=53):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) % p for j in range(len(B[0]))] for i in range(len(A))]


pairs = [
    ("May the Force be with you", "xwzJnuFtGzYQRbEmijuRq YKRKeYnw"),
    ("Stay hungry stay foolish", "ZEIqtabLYhkClfEmioDRmiojNNzdKJ"),
    ("The truth will set you free", "AsXLTcdLDnCRjWjwJrTisfFLsVYzWO"),
    ("Big Brother is watching you", "lyCYnaujrjpucseJsSHMUvzTcjMaQw"),
    ("Life is like a box of matches", "woQFSmWSan UtyBKMgbjrtvMqcDOiT"),
    ("I think therefore I am", "YlqHeVvsYJmwNERjMfYFMQWDyaMJAZ"),
    ("To be is to be perceived", "BiWjPlcOdkOggUqsYWzY PGAcfogga"),
    ("Girls are made of water", "mzuZlldSTpMiFfDU aRQRIrpGZUUQl"),
    ("God does not play dice", "sjcxplYeeHYjZzshSYbyvIioWskDuG"),
    ("I have loved none but you", "whPTJYlIKFYDbRUY EeMfxTQECrMVE"),
]

# Test all possible space placements at the PDF line break (28 non-space chars + 2 spaces = 30 chars)
part1 = "RpjANVjbOsEWH"
part2 = "FLoXgpEoFKxrBcD"
candidates = [
    part1 + (" " * mid_spaces) + part2 + (" " * (2 - mid_spaces))
    for mid_spaces in range(3)
]


def try_solve(n, affine=False):
    blocks = []
    for pt, ct in pairs:
        num_unpadded = len(pt) // n
        for b_idx in range(num_unpadded):
            p_vec = encode(pt[b_idx * n: (b_idx + 1) * n])
            if affine:
                p_vec = p_vec + [1]
            c_vec = encode(ct[b_idx * n: (b_idx + 1) * n])
            blocks.append((p_vec, c_vec))

    dim = n + 1 if affine else n
    sel_p, sel_c = [], []
    for p_vec, c_vec in blocks:
        if rank_mod(sel_p + [p_vec], MOD) > len(sel_p):
            sel_p.append(p_vec)
            sel_c.append(c_vec)
            if len(sel_p) == dim:
                break

    if len(sel_p) < dim:
        return None

    P = [list(col) for col in zip(*sel_p)]
    C = [list(col) for col in zip(*sel_c)]
    P_inv = mod_inv_matrix(P, MOD)
    if P_inv is None:
        return None

    K_aug = mat_mul_mod(C, P_inv, MOD)

    # Verify against all unpadded blocks
    for p_vec, c_vec in blocks:
        pred = [row[0]
                for row in mat_mul_mod(K_aug, [[x] for x in p_vec], MOD)]
        if pred != c_vec:
            return None

    return K_aug, len(blocks)


for n, affine in [(10, False), (10, True), (15, False), (15, True)]:
    res = try_solve(n, affine)
    if res is not None:
        K_aug, total_blocks = res
        K = [row[:n] for row in K_aug]
        b_vec = [row[n] for row in K_aug] if affine else [0] * n
        K_inv = mod_inv_matrix(K, MOD)

        print(f"SUCCESS! Block size n = {n}, Affine = {affine}")
        print(f"Verified consistently across all {
              total_blocks} unpadded blocks.\n")

        for mid_spaces, intercepted in enumerate(candidates):
            decrypted_chars = []
            for idx in range(0, len(intercepted), n):
                c_vec = encode(intercepted[idx: idx + n])
                c_shifted = [[(c_vec[i] - b_vec[i]) % MOD] for i in range(n)]
                p_vec = [row[0] for row in mat_mul_mod(K_inv, c_shifted, MOD)]
                decrypted_chars.append(decode(p_vec))

            full_decrypted = "".join(decrypted_chars)
            print(f"[Option {mid_spaces}: {mid_spaces} middle space(s), {
                  2 - mid_spaces} trailing space(s)]")
            print(f"  Raw Decrypted (30 chars): '{full_decrypted}'")
            print(f"  Stripped Plaintext:       '{full_decrypted.rstrip()}'\n")
        break
else:
    print("No consistent linear/affine solution found for n=10 or n=15; check n=30.")
