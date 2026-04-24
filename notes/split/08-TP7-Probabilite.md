# TP7: Probabilite

所有题目都依赖`random`库,其中最常用的两个 API 是

- `random.random()` —— 返回 $[0, 1)$ 上的均匀分布随机数
- `random.randint(a, b)` —— 返回**闭区间** $[a, b]$ 上的均匀整数分布

## 抽球实验:有放回 vs 无放回

袋中有 $N_1$ 个红球, $N_2$ 个白球,进行 $n$ 次抽取,统计抽到红球的次数

### 有放回
每次抽取独立,单次抽到红球的概率恒为 $p = \frac{N_1}{N_1 + N_2}$,所以红球出现次数服从二项分布 $X \sim B(n, p)$

```Python
def experience1(N1: int, N2: int, n: int) -> int:
    res = 0
    for _ in range(n):
        one_try = random.randint(0, N1 + N2 - 1)
        if one_try < N1:
            res += 1

    return res
```

用`random.randint(0, N - 1) < N1`来模拟概率 $N_1 / N$ 的伯努利事件,比直接`random.random() < p`在数值上更干净——前者只涉及整数运算,完全没有浮点误差

### 无放回
题目约定抽到红球就从袋中拿走,白球放回,因此红球剩余数`red_rest`随实验递减,白球总数始终为 $N_2$

```Python
def experience2(N1: int, N2: int, n: int) -> int:
    res = 0
    red_rest = N1
    for _ in range(n):
        one_try = random.randint(0, red_rest + N2 - 1)
        if one_try < red_rest:
            res += 1
            red_rest -= 1

    return res
```

## 离散分布的期望与方差

输入统一为`L = [(a, P(X=a)), ...]`,即"取值—概率"对的列表

### 期望
直接按定义 $E[X] = \sum a \cdot P(X=a)$
```Python
def esperance(L):
    res = 0
    for a, Pa in L:
        res += a * Pa

    return res
```

### 方差
方差的原始定义 $\mathrm{Var}(X) = E[(X - E[X])^2]$ 需要先求出 $E[X]$ 再遍历一次求平方差,共两轮遍历,我们可以用下面这个恒等式把计算结构简化:

$$
\mathrm{Var}(X) = E[X^2] - (E[X])^2
$$

只需把取值平方后复用`esperance`即可
```Python
def variance(L):
    L_carre = [[L[i][0] ** 2, L[i][1]] for i in range(len(L))]
    e_l = esperance(L)
    e_l_carre = esperance(L_carre)

    return e_l_carre - e_l ** 2
```

> 注意:$E[X^2] - (E[X])^2$ 在数学上等价于原始定义,但在**浮点数**实现中,当 $E[X^2]$ 和 $(E[X])^2$ 都很大且十分接近时会发生**灾难性抵消 (catastrophic cancellation)**,结果可能出现负数或严重失真. 对本题这种以概率列表输入的场景问题不大,但在做真实数据统计时,经典的 Welford 在线算法更稳定

## 几何分布:首次成功出现的位置

重复独立的伯努利试验,单次成功概率为 $p$,返回形如`[0, 0, ..., 0, 1]`的序列,其长度 $T$ 服从几何分布:

$$
P(T = k) = (1 - p)^{k-1} \cdot p, \quad k \geq 1
$$

```Python
def premier_rang(p):
    res = []
    while True:
        if random.random() > p:
            res.append(0)
        else:
            res.append(1)
            return res
```

## 泊松分布的抽样

泊松分布参数 $\lambda > 0$, 概率质量函数为

$$
P(X = k) = e^{-\lambda}\cdot\frac{\lambda^k}{k!}
$$

我们希望通过**逆变换采样**来生成: 抽 $U \sim \mathcal{U}[0, 1)$, 找到最小的 $k$ 使得累积分布 $F(k) = \sum_{i=0}^{k} P(X=i) \geq U$, 返回该 $k$

直接按定义计算 $P(X=k)$ 要算 $\lambda^k$ 和 $k!$, 开销很大, 不过相邻两项之间有一个非常优雅的递推:

$$
P(X = k+1) = P(X = k) \cdot \frac{\lambda}{k + 1}
$$

因此我们只需维护两个变量: **当前 pmf `pk`** 和 **累积 cdf `cdf`**, 每轮迭代都是 $O(1)$

```Python
import math

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
```

笔者最初的写法是把当前 pmf 和 cdf 合并成同一个变量`probability`,递推写作`probability += probability * l / res`. 这样做会把**已经累加在里面的 CDF 部分**也一起乘上 $\lambda / k$,分布严重偏差  
**pmf (概率质量) 和 cdf (累积分布) 是两个不同的量, 在递推中必须分开维护**

另外,直接用`math.exp(-l)`比自己手写常量`e`再做`e ** (-l)`更精确也更快,后者在 $\lambda$ 较大时会有明显误差

## 按给定离散分布采样任意整数

输入`L = [p0, p1, ..., p_{k-1}]`,保证 $\sum p_i = 1$,希望返回下标 $i$,使得 $P(\text{返回 } i) = p_i$

用**累积分布函数 + 均匀随机数**的思想:
1. 抽 $U \sim \mathcal{U}[0, 1)$
2. 从左到右扫描,维护前缀和 $S_i = p_0 + \ldots + p_i$,第一个满足 $S_i \geq U$ 的下标就是答案

```Python
def entier_aleatoire(L):
    try_res = random.random()
    cur_p_sum = 0
    for idx, p in enumerate(L):
        cur_p_sum += p
        if cur_p_sum >= try_res:
            return idx
```

单次调用的时间复杂度为 $O(k)$. 如果需要**频繁采样**且 $k$ 较大,可以预先计算 CDF 数组然后用二分查找降到 $O(\log k)$;若 $k$ 固定且有大量采样需求,**别名方法 (Alias Method)** 能做到 $O(1)$ 采样,预处理开销 $O(k)$

## 用蒙特卡洛方法估计 π

在单位正方形 $[0, 1] \times [0, 1]$ 内均匀撒点,落在单位圆内 ($x^2 + y^2 \leq 1$) 的概率正好是四分之一圆的面积除以正方形面积:

$$
P(\text{落入圆内}) = \frac{\pi / 4}{1} = \frac{\pi}{4}
$$

所以用落入圆内的经验频率来逼近 $\pi / 4$,再乘以 $4$ 就是 $\pi$ 的估计

```Python
def approx(n):
    inside_time = 0
    for _ in range(n):
        x_i, y_i = random.random(), random.random()
        is_inside = (x_i ** 2 + y_i ** 2 <= 1)
        if is_inside: inside_time += 1

    return inside_time / n
```


## 随机置换与不动点

### 生成随机置换
#### `random`库生成随机置换
Python内置的 `random` 库直接提供了现成函数
```python
def permutation_aleatoire_random(n):

    return random.sample(range(n), n)

def permutation_aleatoire_shuffle(n):
    arr = list(range(n))
    random.shuffle(arr)
    return arr
```

#### 回溯生成随机置换
通过回溯枚举 $\{0, 1, \ldots, n-1\}$ 的所有 $n!$ 个排列, 再均匀随机挑一个返回
```Python
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
```
使用了回溯算法的方法法效率非常低: 时间与空间复杂度均为 $O(n \cdot n!)$, 实际上 $n \geq 10$ 就已经几乎跑不动了  


### 不动点个数
不动点 = 满足 $\sigma(i) = i$ 的下标 $i$, 直接遍历计数即可
```Python
def nb_points_fixes(L):
    res = 0
    for idx, value in enumerate(L):
        if idx == value:
            res += 1

    return res
```

### 经验均值
重复 $m$ 次 "生成随机置换 $\to$ 数不动点",取平均
```Python
def moyenne_empirique(n, m):
    res = 0
    for _ in range(m):
        permutation = permutation_aleatoire(n)
        res += nb_points_fixes(permutation)

    return res / m
```

对大小为 $n$ 的均匀随机置换, 不动点个数 $X_n$ 的期望为

$$
E[X_n] = E\left[\sum_{i=0}^{n-1} \mathbf{1}_{\sigma(i)=i}\right] = \sum_{i=0}^{n-1} P(\sigma(i) = i) = \sum_{i=0}^{n-1} \frac{1}{n} = 1
$$

