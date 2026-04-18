# TP5: Calculs avec les polynômes 计算多项式
> 不可变性是指数据一旦创建就不能被修改，任何更改都需要生成新的数据结构，从而提高代码的可预测性和安全性  

在这一章里，我们尽可能不去修改输入的列表，例如：
```Python
def reduire(L: list[int | float]) -> list[int | float]:
    res = L.copy()
    while len(res) > 0 and res[-1] == 0:
        res.pop()
    return res
```
而不是：
```Python
def reduire(L: list[int | float]) -> None:
    while len(L) > 0 and L[-1] == 0:
        L.pop()
    return
```

当然，第一段代码使用了`L.copy()`创建了一个新的列表对象，在`L`很大时会消耗更多性能，这时就需要进行取舍

### 多项式求值与霍纳法则

给定一个多项式 $P(X) = a_0 + a_1 X + a_2 X^2 + \dots + a_n X^n$ 和一个实数 $a$，我们需要计算 $P(a)$ 的值

#### 朴素实现与复杂度陷阱
最直接的想法是利用求和公式，通过循环计算每一项的值


朴素实现
```Python
def evaluation(P: list[int], a: float) -> float:
    #  la complexité: ?
    return sum(P[i] * (a ** i) for i in range(len(P)))
```

如果只看代码，很容易认为这段程序的时间复杂度是$O(n)$，因为程序只遍历了一次列表  
然而事情并没有那么简单，我们使用`**`运算符来实现幂运算，Python使用的是快速幂算法来计算`a ** i`，也就是说，计算$a^i$需要进行的乘法次数大约是$log_2(i)$次，这会导致总成本产生质变  
代码在循环中，从 $i=1$ 到 $n$，每次都重新计算 `a ** i`

- 当  $i=1$  时，成本约  $log(1)$ 
- 当  $i=2$  时，成本约  $log(2)$ 
- ...
- 当  $i=n$  时，成本约  $log(n)$ 

所以，总的操作次数是：

$$
\sum_{i=1}^{n} \log(i) = \log(1 \times 2 \times \dots \times n) = \log(n!)
$$

根据斯特林公式  
$$
n! \sim \sqrt{2\pi n} \left(\frac{n}{e}\right)^n
$$  
$log(n!)$的复杂度量级正是  $O(nlog n)$   

#### 两种优化方案
- 通过存储$a^i$的值来避免成本过高：
```Python
def evaluation(P: list[int], a: float) -> float:
    #  la complexité: O(n)
    a_i = 1
    res = 0
    for num in P:
        res += a_i * num
        a_i *= a
    return res
```
- 使用`Horner`算法  
```Python
def horner_digui(P: list[int | float], a: int | float) -> int | float:
    P_reduire = reduire(P)
    if not P_reduire:
        return 0
    
    return a * horner_digui(P_reduire[1:], a) + P_reduire[0]

def horner_diedai(P: list[int | float], a: int | float) -> int | float:
    P_reduire = reduire(P)
    if not P_reduire:
        return 0

    res = P_reduire[-1]
    n = len(P_reduire)
    for i in range(n - 2, -1, -1):
        res = res * a + P_reduire[i]
    
    return res
```
两种算法的时间复杂度均为$O(n)$

## 实现多项式余数除法
给定两个多项式 $f(x)$ 和 $g(x)$（其中 $g(x) \neq 0$），必然存在唯一的一对多项式 $Q(x)$ 和 $R(x)$，使得下式成立：

$$f(x) = g(x)Q(x) + R(x)$$

并且满足条件：
$$\deg(R(x)) < \deg(g(x))$$

其中：
*   $f(x)$ 被称为**被除式**。
*   $g(x)$ 被称为**除式**。
*   $Q(x)$ 被称为**商式**。
*   $R(x)$ 被称为**余式**。
*   $\deg(P(x))$ 表示多项式 $P(x)$ 的次数（即最高次项的幂次）。

简单来说，多项式除法就是将一个多项式 $f(x)$ 分解为除式 $g(x)$ 与商式 $Q(x)$ 的乘积，再加上一个次数低于除式的余式 $R(x)$ 的过程。当余式 $R(x) = 0$ 时，我们称 $f(x)$ 能被 $g(x)$ 整除。

### 长除法实现
```Python
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
```
时间复杂度为$O(len(P)*len(Q))$

### 另一种方法-多项式求逆
#### 多项式求逆

在模 $x^n$ 的意义下，给定一个多项式 $A(x)$，如果存在一个多项式 $B(x)$ 满足：

$$A(x)B(x) \equiv 1 \pmod{x^n}$$

则称 $B(x)$ 为 $A(x)$ 的**逆元**，记作 $A^{-1}(x)$

~~死去的数论开始攻击我~~

#### 牛顿迭代法求多项式的逆
由
$$A(x)B(x) = 1 \pmod{x^n}$$
构造函数
$$G(B) = \frac{1}{B} - A$$
将$A$视为常数,对$G(B)$求导:
$$G'(B) = -B^{-2} = -\frac{1}{B^2}$$

牛顿迭代法的通用公式为：
$$B_{new} = B_{old} - \frac{G(B_{old})}{G'(B_{old})}$$

为了书写方便，设 $B_k$ 为当前已知的模 $x^n$ 下的逆，我们要推导 $B_{2n}$（即精度翻倍后的逆）。将步骤 1 中的 $G(B)$ 和 $G'(B)$ 代入公式：

$$B_{2n} \equiv B_n - \frac{\frac{1}{B_n} - A}{-\frac{1}{B_n^2}} \pmod{x^{2n}}$$

处理分式部分：
$$B_{2n} \equiv B_n - \left( \left( \frac{1}{B_n} - A \right) \cdot (-B_n^2) \right) \pmod{x^{2n}}$$

展开括号内的项：
$$B_{2n} \equiv B_n - \left( -B_n + A \cdot B_n^2 \right) \pmod{x^{2n}}$$

去括号并合并同类项：
$$B_{2n} \equiv B_n + B_n - A \cdot B_n^2 \pmod{x^{2n}}$$
$$B_{2n} \equiv 2B_n - A \cdot B_n^2 \pmod{x^{2n}}$$

提取公因式 $B_n$，得到最终公式：
$$B_{2n} \equiv B_n (2 - A B_n) \pmod{x^{2n}}$$

通过构造函数 $G(B) = \frac{1}{B} - A$，我们成功推导出了多项式求逆的倍增公式：
$$B_{2n} = B_n(2 - AB_n) \pmod{x^{2n}}$$

代码实现，**AI写的**
```Python
def poly_mul(a, b, mod):
    """
    计算两个多项式的乘积 (朴素卷积 O(n^2))
    返回结果列表，结果长度会自动调整
    """
    if not a or not b:
        return []
    
    # 结果多项式的长度最多为 len(a) + len(b) - 1
    res =  * (len(a) + len(b) - 1)
    
    for i in range(len(a)):
        for j in range(len(b)):
            res[i + j] = (res[i + j] + a[i] * b[j]) % mod
            
    return res

def poly_inverse(p, mod, n):
    """
    使用牛顿迭代法求多项式 P 的逆 Q
    满足 P(x) * Q(x) ≡ 1 (mod x^n)
    
    参数:
    p: 输入多项式系数列表，p[i] 是 x^i 的系数
    mod: 模数 (通常为大质数，如 998244353)
    n: 需要求逆的精度 (模 x^n)
    
    返回:
    q: 逆多项式系数列表
    """
    
    # 1. 检查常数项是否可逆
    # 如果 p 为 0，则逆不存在
    if p == 0:
        raise ValueError("常数项为0，逆不存在")

    # 2. 初始化 B_1 (模 x^1 的逆)
    # B_1 = p^(-1)
    # 使用费马小定理求逆元: a^(p-1) ≡ 1 (mod p) => a^(-1) ≡ a^(p-2) (mod p)
    def pow_mod(base, exp, m):
        result = 1
        base = base % m
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % m
            exp = exp >> 1
            base = (base * base) % m
        return result

    b = [pow_mod(p, mod - 2, mod)]  # 当前逆多项式，初始长度为 1

    # 3. 牛顿迭代倍增
    # 每次循环将精度翻倍: 1 -> 2 -> 4 -> ... -> n
    current_len = 1
    while current_len < n:
        next_len = min(current_len * 2, n)
        
        # 核心公式: B_new = B_old * (2 - P * B_old)
        # 注意：我们需要在模 x^next_len 下计算
        
        # 步骤 3.1: 计算 P * B_old
        # 我们只需要 P 的前 next_len 项，因为结果只要模 x^next_len
        p_trunc = p[:next_len]
        pb = poly_mul(p_trunc, b, mod)
        
        # 截断到 next_len
        pb = pb[:next_len]
        
        # 步骤 3.2: 计算 (2 - P * B_old)
        # 2 对应的是常数项系数
        two_minus_pb =  * next_len
        two_minus_pb = 2  # 常数项设为 2
        
        for i in range(len(pb)):
            two_minus_pb[i] = (two_minus_pb[i] - pb[i]) % mod
            
        # 步骤 3.3: 计算 B_old * (2 - P * B_old)
        b = poly_mul(b, two_minus_pb, mod)
        
        # 截断结果到 next_len
        b = b[:next_len]
        
        current_len = next_len

    return b

# --- 测试代码 ---
if __name__ == "__main__":
    MOD = 998244353
    
    # 例子: P(x) = 1 - x  (即列表 [1, MOD-1])
    # 理论上 1/(1-x) = 1 + x + x^2 + x^3 + ...
    # 所以结果应该是 [1, 1, 1, 1, ...]
    P = [1, MOD - 1] 
    N = 8 # 求前 8 项
    
    try:
        Q = poly_inverse(P, MOD, N)
        print(f"输入 P: {P}")
        print(f"逆 Q:   {Q}")
        
        # 验证 P * Q 是否等于 1 (模 x^N)
        check = poly_mul(P, Q, MOD)
        check = check[:N] # 截断
        # 构造目标 [1, 0, 0, ...]
        target =  +  * (N - 1)
        print(f"P * Q:  {check}")
        print(f"验证通过: {check == target}")
        
    except ValueError as e:
        print(e)
```






#### 多项式求逆在求解多项式除法里的应用
观察多项式除法的定义：
$$f(x) = g(x)Q(x) + R(x)$$
我们发现，只要没有$R(x)$，就能够直接使用多项式求逆来解决除法  
为了简化这个问题，我们需要思考，该如何消除余项  
我们需要构造一个模数$x^k$，使得在这个模数下，$R(x)$变为0，而$Q(x)$依然存在  
但$R(x)$的次数显然小于$Q(x)$，在这种情况下，不可能存在这样的模数  
因此我们需要一个变换，在不改变多项式大部分性质和等式的情况下反转多项式  
考虑构造变换
$$f^R(x) = x^{\deg(f)} \cdot f\left(\frac{1}{x}\right)$$
这个变换能够在次数为$n$的多项式里反转系数，如果一个多项式系数是$[a_0,a_1,...,a_n]$，那么其在变换之后的系数就为$[a_n,a_n-1,...,a_0]$
将这个变换应用到等式两端，我们惊喜地发现，原式变为：
$$f^R(x) = g^R(x)Q^R(x) + x^{n-m+1}\cdot R^R(x)$$
余项现在自己就含有因子$x^{n-m+1}$,现在我们直接取模：
$$f^R(x) = g^R(x)Q^R(x) \pmod{x^{n-m+1}}$$
我们可以直接使用这个式子把$Q^R(x)$解出来，移项：
$$Q^R(x) = f^R(x)(g^R(x))^{-1} \pmod{x^{n-m+1}}$$
已知$f^R(x)$，只需要求$(g^R(x))^{-1}$就能解出$Q^R(x)$，进一步解出$Q(x)$，最后通过
$$f(x) = g(x)Q(x) + R(x)$$
移项得：
$$R(x) = f(x) - g(x)Q(x)$$
解出$R(x)$

上述数学推导还不十分严密，因为没有证明：
- 等式在变换后还能成立
- 变换是否符合分配律
- 除了余数项以外的其他项会不会由于取模受到影响
- 逆元$(g^R(x))^{-1}$的存在性
- 反转定义里次数$x^{\deg(f)}$的对齐问题  
等问题，但我现在实在是太忙了，等考完试尽量补上

#### 代码实现


