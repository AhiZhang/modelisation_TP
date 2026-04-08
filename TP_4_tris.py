def recherche(T: list[int], x: int) -> int:
    left, right = 0, len(T) - 1
    while left <= right:
        middle = (left + right) // 2
        if T[middle] == x:
            return middle
        elif T[middle] > x:
            right = middle - 1
        else:
            left = middle + 1

    return -1


def tri_comptage(L: list[int]) -> list[int]:
    comptage_list = [0] * 51
    for value in L:
        comptage_list[value] += 1

    res = []
    for idx, count in enumerate(comptage_list):
        if count == 0:
            continue

        res.extend([idx] * count)

    return res

def tri_selection(L: list[int]) -> list[int]:
    n = len(L)
    for i in range(n):
        indice = i
        for j in range(i + 1, n):
            if L[j] < L[indice]:
                indice = j
        L[i], L[indice] = L[indice], L[i]

    return L

def tri_inserction(L: list[int]) -> list[int]:
    res = [L[0]]
    n = len(L)
    for i in range(1, n):
        cur_num = L[i]
        cur_res_len = len(res)
        idx = 0
        for j in range(cur_res_len - 1, -1, -1):
            if cur_num >= res[j]:
                idx = j
                break
        res.insert(idx, cur_num)

    return res

def fusion(L: list[int], M: list[int]) -> list[int]:
    if not L or not M:
        return L + M

    if L[0] < M[0]:
        return [L[0]] + fusion(L[1:], M)
    else:
        return [M[0]] + fusion(L, M[1:])
    
def tri_fusion(L: list[int]) -> list[int]:
    n = len(L)
    if n <= 1:
        return L
    
    left_L, right_L = L[:n // 2], L[n // 2:]
    
    left_sorted = tri_fusion(left_L)
    right_sorted = tri_fusion(right_L)

    return fusion(left_sorted, right_sorted)

def tri_rapide_aux(L: list[int]) -> list[int]:
    if len(L) <= 1:
        return L
    
    pivot = L[-1]
    left = [x for x in L[:-1] if x <= pivot]
    right = [x for x in L[:-1] if x > pivot]

    return tri_rapide_aux(left) + [pivot] + tri_rapide_aux(right)

def est_tas(L: list[int]) -> bool:
    return all(L[i] >= L[(i - 1) // 2] for i in range(1, len(L)))

def diminue(L: list[int], i: int, a: int) -> bool:
    if a > L[i]:
        return False
    
    L[i] = a




if __name__ == "__main__":
    list_to_sort = [1, 2, 5, 9, 6, 12, 3, 49, 6, 7, 12]
    L1 = [2, 3, 4, 2, 5, 6]
    L2 = [4, 1, 6, 5, 3]
    L3 = [1, 2, 2, 5, 6, 4, 3]
    L4 = [0, 0, 1, 1, 2, 4, 6]

    print(est_tas(L1))
    print(est_tas(L2))
    print(est_tas(L3))
    print(est_tas(L4))