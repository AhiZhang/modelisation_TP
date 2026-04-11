import math as np

def cos(x) :
    return np.cos(x)

def racine_de(x):
    return np.sqrt(x)

def integraleG(f,a,b,N) :
    h=(b-a)/N
    t=[a+i*h for i in range(N)]
    IN=0.
    for i in range(N) :
        IN+=h*f(t[i])
    return IN

def integraleT(f,a,b,N):
    h = (b - a) / N
    res = 0
    for i in range(N):
        left = a + i * h
        right = a + (i + 1) * h
        area = (f(left) + f(right)) * h / 2
        res += area

    return res

def integraleM(f,a,b,N):
    h = (b - a) / N
    res = 0
    for i in range(N):
        middle = a + (i + 0.5) * h
        area = f(middle) * h
        res += area

    return res

def integraleS(f,a,b,N):
    h = (b - a) / N
    res = 0
    for i in range(N):
        left = a + i * h
        right = a + (i + 1) * h
        middle = (left + right) / 2
        intergrale = (right - left) * (f(left) + 4 * f(middle) + f(right)) / 6
        res += intergrale

    return res

def primitivePoly(P):
    res = ['C']
    for idx, k in enumerate(P):
        res.append(k / (idx + 1))

    return res

def integrerPoly(P,a,b):
    primitive_of_P = primitivePoly(P)
    '''
    return sum((b ** i) * primitive_of_P[i] for i in range(len(primitive_of_P)) ) - sum((a ** i) * primitive_of_P[i] for i in range(len(primitive_of_P)) )
    很明显还有优化空间
    '''
    res = 0
    a_power_k = b_power_k = 1
    for k in primitive_of_P:
        res += k * (b_power_k - a_power_k)
        a_power_k *= a
        b_power_k *= b

    return res

def reduire(L: list[int | float]) -> list[int | float]:
    res = L.copy()
    while len(res) > 0 and res[-1] == 0:
        res.pop()
    return res

def somme(P: list[int | float], Q: list[int | float]) -> list[int | float]:
    max_len = max(len(P), len(Q))
    res = []
    for i in range(max_len):
        a = P[i] if i < len(P) else 0
        b = Q[i] if i < len(Q) else 0
        res.append(a + b)
    return reduire(res)

def diff(P: list[int | float], Q: list[int | float]) -> list[int | float]:
    max_len = max(len(P), len(Q))
    res = []
    for i in range(max_len):
        a = P[i] if i < len(P) else 0
        b = Q[i] if i < len(Q) else 0
        res.append(a - b)
    return reduire(res)

def produit(P: list[int], Q: list[int]) -> list[int]:
    #  la complexité: O(len(P) * len(Q))
    len_P, len_Q = len(P), len(Q)
    res = [0 for _ in range(len_P + len_Q)]
    for idx_P, num_P in enumerate(P):
        for idx_Q, num_Q in enumerate(Q):
            res[idx_P + idx_Q] += num_P * num_Q

    return reduire(res)

def polyLegendre(n):
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]
    dp = [[] for _ in range(n + 1)]
    dp[0] = [1]
    dp[1] = [0, 1]
    for i in range(2, n + 1):
        frist = produit(dp[i - 1], [0, 1])
        for idx, k in enumerate(frist):
            frist[idx] = k * (2 * i - 1)

        second = dp[i - 2]
        for idx, k in enumerate(second):
            second[idx] *= (i - 1)

        res = diff(frist, second)
        for k in res:
            dp[i].append(k / (i + 1))

    return dp[n]
    
def integrepoly(P):
    res = 0
    n_fact = 1
    for idx, k in enumerate(P):
        if idx == 0:
            res += n_fact * k
            continue

        n_fact *= idx
        res += n_fact * k

    return res

def produitscalaire(P,Q):
    P_Q_produit = produit(P, Q)
    return integrepoly(P_Q_produit)


def devP(xi):
    if not xi:
        return [1]
    
    terms = [[-i, 1] for i in xi]
    res = [1]
    for i in range(len(terms)):
        res = produit(res, terms[i])

    return res

def poids(xi):
    n = len(xi)
    if n == 0:
        return []
    
    res = []
    
    for i in range(n):
        other_roots = [xi[j] for j in range(n) if j != i]
        numerator_poly = devP(other_roots)
        
        denominator = 1
        for j in range(n):
            if i != j:
                denominator *= (xi[i] - xi[j])
        
        Li_poly = [coeff / denominator for coeff in numerator_poly]
        
        Ai = integrerPoly(Li_poly, -1, 1)
        res.append(Ai)
        
    return res

def value_of_polynome(P, a):
    res = 0
    a_power_k = 1

    for k in P:
        res += k * a_power_k
        a_power_k *= a

    return res

def derive(P: list[int]) -> list[int]:
    return [P[i] * i for i in range(1, len(P))]

def racine(P, a, b):
    a_value = value_of_polynome(P, a)
    b_value = value_of_polynome(P, b)
    if a_value * b_value > 0:
        return a - 1
    
    x_curr = (a + b) / 2
    P_i = max(P)
    tolerance = P_i * 1e-15
    max_iter = 100
    for _ in range(max_iter):
        f_val = value_of_polynome(P, x_curr)
        
        if abs(f_val) < tolerance:
            return x_curr
            
        deriv_val = value_of_polynome(derive(P), x_curr)
        
        if deriv_val == 0:
            break
            
        x_next = x_curr - f_val / deriv_val
        
        if not (a <= x_next <= b):
            break 
            
        x_curr = x_next

        




if __name__ == "__main__":
    '''
    a = float(input("Enter the value of a:"))
    b = float(input("Enter the value of b:"))
    N = int(input("Enter the value of N:"))
    excat_val = np.sin(b) - np.sin(a)
    N_val = integraleG(f, a, b, N)
    two_N_val = integraleG(f, a, b, 2 * N)
    print(f"Error of N: {excat_val - N_val}")
    print(f"Error of 2N: {excat_val - two_N_val}")
    print(f"Ordre of the methode {np.log2((excat_val - N_val) / (excat_val - two_N_val))}")
    '''
