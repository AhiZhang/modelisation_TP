class Solution:
    def exercice_2(self, s: str) -> bool:
        return len(s) % 2 == 0
    
    def exercice_3(self, n: int) -> str:
        second_in_hour = 3600
        hour = n // second_in_hour
        minute = n % second_in_hour // 60
        second = n - hour * 3600 - minute * 60
        return "{} s correspondent a {} h {} mn {} s".format(n, hour, minute, second)
    
    def exercice_4(self, s: str) -> str:
        if len(s) >= 5:
            return s[-5:]
        else:
            return s
        
    def absolute(self, x: float) -> float:
        return x if x >= 0 else -x
    
    def e_6(self, n: int, p: float) -> float:
        return sum(i ** p for i in range(n + 1))
    
    def est_premier(self, n: int) -> bool:
        if n <= 1:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    def factorielle(self, n: int) -> int:
        res = 1
        for i in range(1, n + 1):
            res *= i
        return res
    
    def binom(self, n: int, p: int) -> int:
        return self.factorielle(n) // (self.factorielle(p) * self.factorielle(n - p))

    def fibo(self, n: int) -> int:
        if n <= 1:
            return 1
        prev_prev = 0
        cur = 0
        prev = 1
        for _ in range(2, n + 1):
            cur = prev_prev + prev
            prev_prev, prev = prev, cur
        return cur

    def est_somme_de_carres(self, n: int) -> bool:
        for i in range(int(n ** 0.5) + 1):
            b =  n - i ** 2
            if b == int(b ** 0.5) ** 2:
                return True
        return False

    def u(self, n: int) -> int:
        if n == 0:
            return 3
        u_i = 3
        for i in range(n):
            u_i = u_i ** 2 + 3 * u_i + i 
        return u_i

    def calcul(self, n: int) -> int:
        return sum(self.u(i) for i in range(n + 1))

    def distance(self, a: str, b: str) -> int:
        count = 0
        a, b = a.lower(), b.lower()
        for i, char in enumerate(a):
            if char != b[i]:
                count += 1
        return count

    def nb_voyelles(self, s: str) ->int:
        s = s.lower()
        count = 0
        for char in s:
            if char in ('a', 'e', 'i', 'o', 'u'):
                count += 1
        return count
    
    def dans_le_disque(self, a: int, b: int, r: int, x: int, y: int) -> bool:
        return (x - a) ** 2 + (y - b) ** 2 < r ** 2
    
    def premiers_entre_eux(self, n: int, m: int) -> bool:
        m, n = max(m, n), min(m, n)
        while n != 0:
            m, n = n, m % n
        return m == 1

    def lettres_consecutives_id(self, texte: str) -> bool:
        for i in range(len(texte) - 1):
            if texte[i] == texte[i + 1]:
                return True
        return False
    
    def pgcd(self, n: int, m: int) -> int:
        m, n = max(m, n), min(m, n)
        while n != 0:
            m, n = n, m % n
        return m
    
    def est_suffixe(self, s: str, m: str) -> bool:
        return m == s[-len(m):]

    def est_monotone(self, L: list[int]) -> bool:
        if len(L) <= 1:
            return True
        croissante = None
        for i in range(len(L) - 1):
            actuel = L[i]
            suivant = L[i + 1]
            if actuel == suivant:
                continue
            if croissante is None:
                croissante = actuel < suivant
            else:
                if croissante and actuel > suivant:
                    return False
                if not croissante and actuel < suivant:
                    return False
        return True

    def bezout(self, n: int, m: int) -> tuple[int, int]:
        if m == 0:
            return (1, 0)
        a1, b1 = self.bezout(m, n % m)
        a, b = b1, a1 - b1 * (n // m)
        return (a, b)