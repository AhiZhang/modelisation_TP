import math
import random

def experience1(N1: int, N2: int, n: int) -> int:
    res = 0
    for _ in range(n):
        one_try = random.randint(0, N1 + N2 - 1)
        if one_try < N1:
            res += 1

    return res

def experience2(N1: int, N2: int, n: int) -> int:
    res = 0
    red_rest = N1
    for _ in range(n):
        one_try = random.randint(0, red_rest + N2 - 1)
        if one_try < red_rest:
            res += 1
            red_rest -= 1

    return res

def esperance(L):
    res = 0
    for a, Pa in L:
        res += a * Pa

    return res

def variance(L):
    L_carre = [[L[i][0] ** 2, L[i][1]] for i in range(len(L))]
    e_l = esperance(L)
    e_l_carre = esperance(L_carre)

    return e_l_carre - e_l ** 2

def premier_rang(p):
    res = []
    while True:
        if random.random() > p:
            res.append(0)
        else:
            res.append(1)
            return res
        
def poisson(l: int | float) -> int:
    u = random.random()
    pk = math.exp(-l)
    cdf = pk
    k = 0
    while cdf < u:
        k += 1
        pk *= l / k
        cdf += pk

    return k

def entier_aleatoire(L):
    try_res = random.random()
    cur_p_sum = 0
    for idx, p in enumerate(L):
        cur_p_sum += p
        if cur_p_sum >= try_res:
            return idx
        
def approx(n):
    inside_time = 0
    for _ in range(n):
        x_i, y_i = random.random(), random.random()
        is_inside = (x_i ** 2 + y_i ** 2 <= 1)
        if is_inside: inside_time += 1

    return inside_time / n

def permutation_aleatoire(n):
    all_permutation = []
    all_num = [i for i in range(n)]
    num_used = [False for _ in range(n)]

    def backtrak(path):
        if len(path) == n:
            all_permutation.append(path[:])
            return

        for i in range(n):
            if not num_used[i]:
                path.append(all_num[i])
                num_used[i] = True
                backtrak(path)
                path.pop()
                num_used[i] = False

    backtrak([])

    res_idx = random.randint(0, len(all_permutation) - 1)
    return all_permutation[res_idx]

def nb_points_fixes(L):
    res = 0
    for idx, value in enumerate(L):
        if idx == value:
            res += 1

    return res

def moyenne_empirique(n, m):
    res = 0
    for _ in range(m):
        permutation = permutation_aleatoire(n)
        res += nb_points_fixes(permutation)

    return res / m
 