# TP6: Integration numeriquue
`import math as np`
> ~~开幕雷击~~老师这么写一定有他的道理,但我们还是写`import math`
## 几种基础的积分方法
我们以$f(x)=cos(x)$和$g(x)=\sqrt{x}$为例,展示各个积分方法
```Python
import math
def f(x: int | float) -> float:
    return math.cos(x)

def g(x: int | float) -> float:
    return math.sqrt(x)
```
### 左\右矩形法
```Python
def integraleG(f,a,b,N) :
    h=(b-a)/N
    t=[a+i*h for i in range(N)]
    IN=0.
    for i in range(N) :
        IN+=h*f(t[i])
    return IN

def integraleD(f,a,b,N) :
    h=(b-a)/N
    t=[a+i*h for i in range(N + 1)]
    IN=0.
    for i in range(1, N) :
        IN+=h*f(t[i])
    return IN
```

### 梯形法
```Python
def integraleT(f,a,b,N):
    h = (b - a) / N
    res = 0
    for i in range(N):
        left = a + i * h
        right = a + (i + 1) * h
        area = (f(left) + f(right)) * h / 2
        res += area

    return res
```

假设我们将区间分为 $N$ 份,其中第 $i$ 个子区间 $[x_i, x_{i+1}]$ 的梯形面积计算公式为:

$$
A_i = \frac{h}{2} \left[ f(x_i) + f(x_{i+1}) \right]
$$


观察总积分公式 $S = \sum_{i=0}^{N-1} A_i$,我们可以发现除了首项 $f(x_0)$ 和末项 $f(x_N)$ 外,中间的所有节点 $f(x_i)$ 都是相邻两个梯形的公共边,被重复计算了两次

我们可以这么写:

$$
\begin{aligned}
S &\approx \frac{h}{2} f(x_0) + \left( \frac{h}{2}f(x_1) + \frac{h}{2}f(x_1) \right) + \dots + \left( \frac{h}{2}f(x_{N-1}) + \frac{h}{2}f(x_{N-1}) \right) + \frac{h}{2} f(x_N) \\
&= h \left[ \frac{1}{2}f(x_0) + \sum_{i=1}^{N-1} f(x_i) + \frac{1}{2}f(x_N) \right]
\end{aligned}
$$

通过这种变换,我们只需要遍历一次内部节点,每个函数值仅计算一次

```python
def integraleT_optimized(f, a, b, N):
    h = (b - a) / N
    res = 0.5 * (f(a) + f(b))
    
    for i in range(1, N):
        res += f(a + i * h)
        
    return res * h
```



### 中点法
```pYTHON
def integraleM(f,a,b,N):
    h = (b - a) / N
    res = 0
    for i in range(N):
        middle = a + (i + 0.5) * h
        area = f(middle) * h
        res += area

    return res
```
### Simpson法
```Python
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
```
### 如何判断误差阶数
误差项 $E(h)$ 与步长 $h$ 的几次方成正比,这个积分方法的误差阶数就是几,在实际计算中,我们能直接把步长变为原来的两倍,再判断改变后的误差是改变前的多少倍
以下是一段简单的判断误差阶数的代码
```Python
if __name__ == "__main__":
    a = float(input("Enter the value of a:"))
    b = float(input("Enter the value of b:"))
    N = int(input("Enter the value of N:"))

    exact_val = math.sin(b) - math.sin(a)
    val_G_N = integraleG(f, a, b, N)
    val_G_2N = integraleG(f, a, b, 2 * N)
    err_G_N = abs(val_G_N - exact_val)
    err_G_2N = abs(val_G_2N - exact_val)
    # 防止除零错误
    if err_G_2N > 1e-15:
        p_G = math.log2(err_G_N / err_G_2N)
    else:
        p_G = 0
    print(f"{'integraleG':<15} | {err_G_N:<15.4e} | {err_G_2N:<15.4e} | {p_G:.2f}")

    # --- 3. 右矩形法 ---
    val_D_N = integraleD(f, a, b, N)
    val_D_2N = integraleD(f, a, b, 2 * N)
    err_D_N = abs(val_D_N - exact_val)
    err_D_2N = abs(val_D_2N - exact_val)
    if err_D_2N > 1e-15:
        p_D = math.log2(err_D_N / err_D_2N)
    else:
        p_D = 0
    print(f"{'integraleD':<15} | {err_D_N:<15.4e} | {err_D_2N:<15.4e} | {p_D:.2f}")

    # --- 4. 梯形法 ---
    val_T_N = integraleT(f, a, b, N)
    val_T_2N = integraleT(f, a, b, 2 * N)
    err_T_N = abs(val_T_N - exact_val)
    err_T_2N = abs(val_T_2N - exact_val)
    if err_T_2N > 1e-15:
        p_T = math.log2(err_T_N / err_T_2N)
    else:
        p_T = 0
    print(f"{'integraleGT':<15} | {err_T_N:<15.4e} | {err_T_2N:<15.4e} | {p_T:.2f}")

    # --- 5. Simpson法 ---
    val_S_N = integraleS(f, a, b, N)
    val_S_2N = integraleS(f, a, b, 2 * N)
    err_S_N = abs(val_S_N - exact_val)
    err_S_2N = abs(val_S_2N - exact_val)
    if err_S_2N > 1e-15:
        p_S = math.log2(err_S_N / err_S_2N)
    else:
        p_S = 0
    print(f"{'Simpson':<15} | {err_S_N:<15.4e} | {err_S_2N:<15.4e} | {p_S:.2f}")
```
## Legendre多项式
Legendre多项式定义:
$
(n+1)P_{n+1} = (2n+1)XP_n - nP_{n-1},  P_0 = 1 , P_1 = X
$
我去,这个递推式居然包含三项,递归实现的代码很容易想到,这里提供递推思路,虽然数组名是`dp`,但并没有使用动态规划  

```Python
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
```                                                                                           
## Gauss积分法
本次TP的大头
### 
### 基础方法
在开始解决这些问题前,我们还需要一些工具来帮我们处理多项式的计算,当然,这些工具我们在本次TP或者TP5里面就已经写好了,现在只需要调用\直接复制过来就可以
```Python
def reduire(L: list[int | float]) -> list[int | float]:
    res = L.copy()
    while len(res) > 0 and res[-1] == 0:
        res.pop()
    return res

def produit(P: list[int], Q: list[int]) -> list[int]:
    #  la complexité: O(len(P) * len(Q))
    len_P, len_Q = len(P), len(Q)
    res = [0 for _ in range(len_P + len_Q)]
    for idx_P, num_P in enumerate(P):
        for idx_Q, num_Q in enumerate(Q):
            res[idx_P + idx_Q] += num_P * num_Q

    return reduire(res)

def integrerPoly(poly, a, b):
    integral = 0.0
    for k in range(len(poly)):
        coeff = poly[k]
        deg = k
        integral += coeff * (b**(deg+1) - a**(deg+1)) / (deg+1)
    return integral

def derive(P: list[int]) -> list[int]:
    return [P[i] * i for i in range(1, len(P))]

def evaluation(P: list[int | float], a: int | float) -> int | float:
    # 本来是TP5的horner_diedai(P, a)函数,在此我们将其命名为evaluation方便理解,同时跑得比朴素实现的evaluation快很多
    P_reduire = reduire(P)
    if not P_reduire:
        return 0

    res = P_reduire[-1]
    n = len(P_reduire)
    for i in range(n - 2, -1, -1):
        res = res * a + P_reduire[i]
    
    return res
```
### 生成多项式
编写一个函数 `devP(xi)`,输入多项式 $P$ 的所有单根,输出是该多项式按系数降序排列的列表,如果输入为空列表,则返回 $P=1$
```Python
def devP(xi):
    if not xi:
        return [1]
    
    terms = [[-i, 1] for i in xi]
    res = [1]
    for i in range(len(terms)):
        res = produit(res, terms[i])

    return res
```

### 计算权重
给定区间 $[−1,1]$ 上的节点列表 $(x_i​)$ ,编写函数 `poids(xi)` 计算对应的权重 $(A_i)$ 要求该积分公式对所有次数不超过 $n$ 的多项式精确成立
```Python
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
```

### 求根
编写函数 `racine(P,a,b)`,如果满足 $P(a)P(b)<0$ ,则在区间 $[a,b]$ 内返回 $P$ 的一个根,精度要求为 $10^{15}$ 
使用牛顿迭代法,若失败,则使用二分法
```Python
def racine(P, a, b):
    if evaluation(P, a) * evaluation(P, b) >= 0:
        return None  

    dP = derive(P)
    r = (a + b) / 2
    M = max(abs(p) for p in P)

    # 牛顿法迭代六次
    for _ in range(6):
        r = r - evaluation(P, r) / evaluation(dP, r)

    if a < r < b and abs(evaluation(P, r)) < 1e-15 * M:
        return r

    # 如果牛顿法迭代之后还是没有成功,则先用二分法缩小根的范围,然后递归
    c = (a + b) / 2
    val_c = evaluation(P, c)

    if val_c == 0:
        return c
    elif evaluation(P, a) * val_c < 0:
        return racine(P, a, c)
    else:
        return racine(P, c, b)
```

### 枚举所有根
设定步长 $h = \frac{1}{n^2}$ ,采样点$a_k = -1+kh$ ,编写函数 `toutesracines(P)`,遍历所有小区间 $[a_k, a_{k+1}]$,检查两个端点的函数值是否异号,若是,则调用[求根](#求根)函数`racine`算出具体根,返回多项式 $P$ 的所有根的列表
```Python
def toutesracines(P):
    xi = []
    N = len(P) - 1
    h = 1/ (N * N)
    ak = [-1 + k * h for k in range(2 * N * N + 1)]
    for k in range(2 * N * N):
        if evaluation(P, ak[k]) == 0:
            xi.append(ak[k])
        if evaluation(P, ak[k]) * evaluation(P, ak[k+1]) < 0:
            xi.append(racine(P, ak[k], ak[k+1]))
    return xi
```

### 输出高斯点&高斯权重
```Python
def Gauss(N):
    P = polyLegendre(N)
    xi=toutesracines(P)
    Ai=poids(xi)

    return xi,Ai
```
### 实现复合高斯积分法
使用六个点的高斯公式,即 $N=5$ 将区间 $[a,b]$ 切成 $N$ 个子区间
```Python
x6,A6 = Gauss(6)
def integraleGauss(f,a,b,N):
    h=(b-a)/N
    t=[a+i*h for i in range(N)]
    IN=0.
    for i in range(N) :
        for k in range(6):
            IN+=h*A6[k]/2*f(t[i]+h*(x6[k]+1)/2)
    return IN
```

