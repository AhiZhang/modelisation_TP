# TP1: revision 复习(~~我们之前学过吗~~)
## 检查一个整数是否是多个整数的平方的和

参考答案：
```Python
def est_somme_de_carre(n) :
    for a in range(n) :
        for b in range(n) :
            if (a*a + b*b)==n :
                return True
    return False
# Il est possible de améliorer les bornes...
```
优化后答案：
```Python
def est_somme_de_carres(n: int) -> bool:
    for i in range(int(n ** 0.5) + 1):
        b =  n - i ** 2
        if b == int(b ** 0.5) ** 2:
            return True
    return False
```
参考答案的时间复杂度为 $O(n^2)$ ,优化后答案则为 $O(√n)$

## 判断互质

我们需要判断两个数是否互质,一个容易想到的方法是取min(m,n),遍历(0, min(m, n) + 1)这个区间,若有某个数能整除二者,则返回False,若没有,则返回True
```Python
def premiers_entre_eux(n: int,m: int) -> bool:
    m, n = min(m, n), max(m, n)
    for i in range(2, m + 1):
        if m % i == 0 and n % i == 0:
        return False

    return True
```
这种算法的时间复杂度为 $O(min(m, n))$ ,当两个数过大时效率很低.不妨考虑使用更有效的辗转相除法  
  互质的定义:对于两个数m,n,若pgcd(m, n) = 1,则称m,n*互质*
```Python
def premiers_entre_eux(n: int,m: int) -> bool:
    x, y = m ,n
    while y != 0:
        x, y = y, x % y

    return x == 1
```
或者直接调用`math`库：
```Python
import math

def premiers_entre_eux(n: int, m: int) -> bool:
    return math.gcd(n, m) == 1
```

以上两种算法的时间复杂度均为 $O(log(min(n, m)))$  

## 贝祖定理

我们需要找到一个数组(u, v),使得(u, v)对(m, n)满足u · n + m · v = PGCD(n,m)(贝祖定理)  
对于任意的(m, n),存在不止一组(u, v)满足贝祖定理,我们只需要找到其中一组即可  

通过递归解决:
```Python
def bezout(n: int, m: int) -> tuple[int, int]:
    if m == 0:
        return (1, 0)
    a1, b1 = bezout(m, n % m)
    a, b = b1, a1 - b1 * (n // m)   # 为什么用整除？因为使用普通除法会返回浮点数而非整数
    return (a, b)
```

同时,理论上,所有递归算法均能使用迭代解决:
```Python
def bezout(n: int, m: int) -> tuple[int, int]:
    old_r, r = n, m
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t


    return old_s, old_t
```


