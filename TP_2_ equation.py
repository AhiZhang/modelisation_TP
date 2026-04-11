import math
import time

def approx(eps: float) -> float:
    u_0 = 1
    u_1 = 1 + 1 / u_0
    while abs(u_0 - u_1) > eps:
        u_0 = 1 + 1 / u_1
        u_1 = 1 + 1 / u_0
    return (u_0 + u_1) / 2

def dich_fixe(eps: float) -> float:
    left = 1
    right = 1 + 1 / left
    while abs(right - left) > eps:
        middle = (right + left) / 2
        dif = 1 + 1 / middle - middle
        if dif > 0:
            left = middle
        elif dif < 0:
            right = middle
    return middle

def newton(n: int) -> float:
    u = 1
    for _ in range(n):
        u = u - (u ** 2 - u - 1) / (u ** 2 + 1)
    return u

def dicho(a: float, b: float, A: float, n: int) -> float:
    left, right = min(a, b), max(a, b)
    intervalle_len = (b - a) * (0.5 ** n)
    while right - left > intervalle_len:
        middle = (right + left) / 2
        dif = middle ** 2 - A
        if dif > 0:
            right = middle
        elif dif < 0:
            left = middle
        else:
            break
    return middle

def racine_carre_newton(A: float, n: int) -> float:
    u = 1
    for i in range(n):
        u = 0.5 * (u + A / u)
    return u

def formule_de_ramanujan(n:int) -> float:
    coefficient = 2 ** 1.5 / 9801
    summary = 1103
    fact_4k = fact_k = 1
    for k in range(1, n + 1):
        # summary += math.factorial(4 * k) * (1103 + 26390 * k) / (math.factorial(k) * (396 ** (4 * k)))
        fact_4k *= (4*(k-1)+1) * (4*(k-1)+2) * (4*(k-1)+3) * (4*(k-1)+4)
        fact_k *= k
        summary += fact_4k * (1103 + 26390 * k) / (fact_k ** 4 * (396 ** (4 * k)))
    # summary = sum(math.factorial(4 * k) * (1103 + 26390 * k) / (math.factorial(k) * (396 ** (4 * k))) for k in range(n + 1))

    return coefficient * summary

def dicho_general(f: callable, a: float, b: float, e: float) ->float:
    f_a, f_b = f(a), f(b)
    if f_a * f_b > 0:
        return None
    left, right = min(a, b), max(a, b)
    while right - left > e:
        f_left, f_right = f(left), f(right)
        middle = (right + left) / 2
        f_middle = f(middle)
        if f_middle == 0:
            return middle
        if f_middle * f_left > 0:
            left = middle
        elif f_middle * right > 0:
            right = middle
    return middle

def newton_general(f: callable, df: callable, x0: float, n: int) -> float:
    u = x0
    for _ in range(n):
        u = u - f(u) / df(u)
    return u

def decomposition(p: float, q: float) -> list[float]:
    result = []
    count = 0
    while q != 0 and count < 100:
        a = p // q
        result.append(a)
        p, q = q, p % q
        count += 1
    return result

def fraction(L: list[float]) -> list[int]:
    if not L:
        return [0, 1]
    upper, down = L[-1], 1
    for a in reversed(L[:-1]):
        upper, down = a * upper + down, upper
    return [upper, down]

# def reduit(x: float, n: int) -> list[float]:



if __name__ == "__main__":
    """
    valeur = (1 + 5 ** 0.5) / 2
    eps = float(input("Enter the value of epsilon:"))
    n = int(input("Enter the value of n:"))

    start_time = time.time()
    valeur_approchee = approx(eps)
    end_time = time.time()
    time_used_1 = end_time - start_time

    start_time = time.time()   
    valeur_dich = dich_fixe(eps)
    end_time = time.time()
    time_used_2 = end_time - start_time

    start_time = time.time()
    valeur_newton = newton(n)
    end_time = time.time()
    time_used_3 = end_time - start_time

    print(f"valeur approchee: {valeur_approchee}, dif={valeur - valeur_approchee}, time used:{time_used_1:.10f}")
    print(f"valeur dichotomie: {valeur_dich}, dif={valeur - valeur_dich},  time used:{time_used_2:.10f}")
    print(f"valeur dichotomie: {valeur_newton}, dif={valeur - valeur_newton},  time used:{time_used_3:.10f}")

    print(fraction([3, 7]))
    """
    PI_inverse = 1 / 3.141592653589793
    PI_approched = formule_de_ramanujan(1)
    print(f"{PI_approched}, dif={PI_inverse - PI_approched:.20f}")