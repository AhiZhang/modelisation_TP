def polEgaux(L: list[int], M: list[int]) -> bool:
    L_len, M_len = len(L), len(M)

    if L_len >= M_len:
        for i in range(M_len):
            if L[i] != M[i]:
                return False
            
        for j in range(M_len, L_len):
            if L[j] != 0:
                return False
            
        return True
    
    else:
        for i in range(L_len):
            if L[i] != M[i]:
                return False
            
        for j in range(L_len, M_len):
            if M[j] != 0:
                return False
            
        return True
    
def reduire(L: list[int | float]) -> list[int | float]:
    res = L.copy()
    while len(res) > 0 and res[-1] == 0:
        res.pop()
    return res
        
def degre(P: list[int]) -> int:
    for i in range(len(P) - 1, -1, -1):
        if P[i] != 0:
            return i
        
    return -1

def derive(P: list[int]) -> list[int]:
    return [P[i] * i for i in range(1, len(P))]

def somme(P: list[int | float], Q: list[int | float]) -> list[int | float]:
    max_len = max(len(P), len(Q))
    res = []
    for i in range(max_len):
        a = P[i] if i < len(P) else 0
        b = Q[i] if i < len(Q) else 0
        res.append(a + b)
    return reduire(res)

def evaluation(P: list[int], a: float) -> float:
    #  la complexité: O(nlogn)
    return sum(P[i] * (a ** i) for i in range(len(P)))

def Horner(P: list[int], a: float) -> float:
    if not P:
        return 0
    
    return a * Horner(P[1:], a) + P[0]

def produit(P: list[int], Q: list[int]) -> list[int]:
    #  la complexité: O(len(P) * len(Q))
    len_P, len_Q = len(P), len(Q)
    res = [0 for _ in range(len_P + len_Q)]
    for idx_P, num_P in enumerate(P):
        for idx_Q, num_Q in enumerate(Q):
            res[idx_P + idx_Q] += num_P * num_Q

    return reduire(res)

def division(P: list[int], Q: list[int]) -> list[int | float]:
    P, Q = reduire(P), reduire(Q)
    len_P, len_Q = len(P), len(Q)
    if len_Q > len_P:
        return P
    
    quotient_degree = len_P - len_Q
    quotients = [0.0] * (quotient_degree + 1)


    for i in range(quotient_degree, -1, -1):
        coeff = P[-1] / Q[-1]
        quotients[i] = coeff
        
        term = [0.0] * i + [coeff]
        produit_term_Q = produit(term, Q)
        
        P = somme(P, [-x for x in produit_term_Q])
        P = reduire(P)
    
    return P
        
def produit_rapide(P: list[int], Q: list[int]) -> list[int]:

    if len(P) <= 32 or len(Q) <= 32:
        return produit(P, Q)

    n = len(P) // 2

    P0, P1 = P[:n], P[n:]
    Q0, Q1 = Q[:n], Q[n:]

    A = produit_rapide(P0, Q0)
    B = produit_rapide(P1, Q1)
    C = produit_rapide(somme(P0, P1), somme(Q0, Q1))

    D = somme(somme(C, [-x for x in A]), [-x for x in B])

    D_shifted = [0] * n + D
    B_shifted = [0] * (2 * n) + B

    return reduire(somme(somme(A, D_shifted), B_shifted))

def quotient_reste(P: list[int], Q: list[int]) -> tuple[list[float], list[float]]:
    P, Q = reduire(P), reduire(Q)
    len_P, len_Q = len(P), len(Q)
    if len_Q > len_P:
        return [], P
    
    quotient_degree = len_P - len_Q
    quotients = [0.0] * (quotient_degree + 1)


    for i in range(quotient_degree, -1, -1):
        coeff = P[-1] / Q[-1]
        quotients[i] = coeff
        term = [0.0] * i + [coeff]
        produit_term_Q = produit(term, Q)
        
        P = somme(P, [-x for x in produit_term_Q])
        P = reduire(P)
    
    return quotients, P



n = 1e36  # 这是一个浮点数
n_square = n * n
calculated_root = n_square ** 0.5
truncated_root = int(calculated_root)

n = 1e36
n_square = n * n
calculated_root = n_square ** 0.5

# 真正的 10 的 36 次方（整数）
real_target = 10**36 

print(f"计算结果: {calculated_root:.0f}")
print(f"真实目标: {real_target}")
print("-" * 20)
# 这里才是真正的判断：它到底是不是 10^36？
print(f"它等于 10^36 吗？: {calculated_root == real_target}") 