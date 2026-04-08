import time


def fibo_rec(n: int) -> int:
    if n == 0 or n == 1:
        return 1
    return fibo_rec(n - 1) + fibo_rec(n - 2)

def list_mots_binaires(n: int) -> list[str]:
    if n == 0:
        return
    
    if n == 1:
        return ['0', '1']
    
    return ['0' + j for j in list_mots_binaires(n - 1)] + ['1' + i for i in list_mots_binaires(n - 1)]
    
def exponentiation_rapide(x: float, n: int) -> float:
    # 时间复杂度:o(log(n))
    if n == 0:
        return 1
    
    if n == 1:
        return x
    
    n_is_pair = (n % 2 == 0)
    if n_is_pair:
        return exponentiation_rapide(x * x, n // 2)
    else:
        return x * exponentiation_rapide(x * x, (n - 1) // 2)
    
def exponetiation(x: float, n: int) -> float:
    res = 1
    for _ in range(n):
        res *= x

    return res

def u(a: float, b: float, c: float, n: int) -> float:
    if n == 0:
        return a
    elif n == 1:
        return b
    elif n == 2:
        return c
    
    # return 2 * u(a, b, c, n - 1) - u(a, b, c, n - 2) + 4 * u(a, b, c, n - 3)
    u0, u1, u2 = a, b, c 
    for _ in range(3, n + 1):

        un = 2 * u2 - u1 + 4 * u0

        u0 = u1
        u1 = u2
        u2 = un
    
    return u2

def cat(n: int) -> int:
    if n == 0:
        return 1
    
    summary = 0
    for i in range(n):
        summary += cat(i) * cat(n - i - 1)

    return summary

def cat_eff(n: int) -> int:
    if n == 0:
        return 1
    
    dic = {0: 1}
    for i in range(1, n + 1):
        dic[i] = 0
        for j in range(i):
            dic[i] += dic[j] * dic[i - j - 1]

    return dic[n]

def ligne_pascal(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [1]
    
    res = [1]
    for _ in range(1, n):
        res = [1] + [res[i] + res[i + 1] for i in range(len(res) - 1)] + [1]

    return res

def liste_nouveaux(t: tuple[int], a: int) -> list[tuple[int]]:
    n = len(t)
    res = []
    for i in range(n + 1):
        cur_left, cur_right = t[:i], t[i:]
        res.append(cur_left + (a,) + cur_right)

    return res

def generer_permut(n: int):
    if n == 0:
        return [(0,)]
    
    res = []
    permuts_prev = generer_permut(n - 1)
    for permut in permuts_prev:
        new_permut = liste_nouveaux(permut, n - 1)
        res.extend(new_permut)

    return res
    
def generer_part(n) :
    dico = {1:[(1,)], 2 : [(1,1),(2,)]}
    def generer_aux(n) :
        if n in dico :
            return dico[n]
        dico[n] = []
        res = []
        for i in range(1, n // 2 + 1):
            i_part = generer_aux(i)
            n_i_part = generer_aux(n  - i)
            for one_partition_i in i_part:
                for one_partition_n_i in n_i_part:
                    if one_partition_i[-1] <= one_partition_n_i[0]:
                        res.append(one_partition_i + one_partition_n_i)

        res.sort()
        dico[n] = list(set(res))
        return dico[n]
    
    generer_aux(n)
    return dico[n]

def is_closed(s: str) -> bool:
    matched = {'(': ')', '[': ']', '{': '}'}
    stack = []
    for bracket in s:
        if bracket in ('[', '{', '('):
            stack.append(bracket)
        else:
            if not stack:
                return False
            if bracket == matched[stack[-1]]:
                stack.pop()
            else:
                return False
    return stack == []



if __name__ == "__main__":


    '''
    calcul_times = 100000
    x, n = 1.141592653589793, 2500
    st_time = time.time()
    for _ in range(calcul_times):
        x_n_power = exponetiation(x, n)
    ed_time = time.time()
    print(f"res={x_n_power}, time used:{ed_time - st_time:.10f}s")
    st_time = time.time()
    for _ in range(calcul_times):
        x_n_power = exponentiation_rapide(x, n)
    ed_time = time.time()
    print(f"res={x_n_power}(rapide), time used:{ed_time - st_time:.10f}s")
    
    print(ligne_pascal(10))
    
    print(liste_nouveaux((1,0,2),3))
    
    print(generer_part(5))
    '''
    while True:
        s = input()
        print(is_closed(s))