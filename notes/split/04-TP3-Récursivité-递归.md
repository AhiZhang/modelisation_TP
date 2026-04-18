# TP3: Récursivité 递归
递归是一种算法思想，指函数直接或间接调用自身，将复杂问题分解为规模更小的子问题。递归的核心在于通过重复的自我调用解决问题，直到满足终止条件
在解决这类问题时,一般要考虑以下要素:
1. 明确函数功能
2. 递归终止条件
3. 等价关系式

例如,我们希望实现一个打印0~n个横杠-的函数`print_dash(n)`:
1. 明确函数功能:我们希望这个函数能够自动打印n,n-1,...1个横杠
2. 递归终止条件:`n == 0`
3. 等价关系式:`print_dash(n) = print("-" * n) + print_dash(n - 1)`
则实现如下:
```Python
def print_dash(n: int) -> None:
    if n == 0:
        return
    print("-" * n)
    print_dash(n - 1)
```
在实现过程中,我们大可假设这个函数能够实现目标功能,在内部大胆调用(即使还没写完)  

递归往往不是最有效的解法,例如*Exo1: Étude de la programmation de la suite de Fibonacci*,参考答案使用的就是递归:
```Python
def fibo_rec(n) :
    if n == 0 or n == 1 :
        return 1
    return fibo_rec(n-1) + fibo_rec(n-2)
```
时间复杂度为o(2^n),当输入的n很大时,递归会让计算的复杂度指数爆炸

值得一提的是,Python的递归深度是1000层,读者可以运行以下代码:
```Python
def f(n):
    print(f"This is recursive call {n}")
    f(n + 1)

f(1)
```
在输出`This is recursive call 997`后,程序就崩溃了

### 递归数列 
设实数$a, b, c$，我们研究数列$(u_n)_{n\in\mathbb{N}}$
$$
u_0 = a,\quad u_1 = b,\quad u_2 = c,\quad \forall n \in \mathbb{N},\ u_{n+3} = 2u_{n+2} - u_{n+1} + 4u_n.
$$

参考答案:
```Python
def u(a,b,c,n):
    dico = {0:a,1:b,2:c}
        def u_aux(n) :
            if n in dico :
                return dico[n]
            nouveau_u = 2*u_aux(n-1) -u_aux(n-2)+4*u_aux(n-3)
            dico[n] = nouveau_u
            return dico[n]
        return u_aux(n)
```




笔者解法:
```Python
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
```

---


### 卡特兰数

卡特兰数（Catalan Number）是组合数学中一个常见的数列，记为 $(c_n)_{n\in\mathbb{N}}$。其定义如下：

$$
c_0 = 1, \quad \forall n \in \mathbb{N}, \ c_{n+1} = \sum_{k=0}^n c_k c_{n-k}
$$

该数列的前几项为：1, 1, 2, 5, 14, 42, 132...

---

#### 1. 朴素递归实现
直接根据数学定义编写递归函数。这种方法代码简洁，但存在严重的效率问题

```python
def cat(n: int) -> int:
    if n == 0:
        return 1
    
    summary = 0
    # 对应公式中的求和项
    for i in range(n):
        summary += cat(i) * cat(n - i - 1)

    return summary
```
#### 2. 记忆化与动态规划优化
为了解决重复计算的问题，我们可以通过存储已经计算过的 $c_k$ 值，将时间复杂度降低到 $O(n^2)$
```python
def cat_eff(n: int) -> int:
    if n == 0:
        return 1
    
    # 使用字典存储已计算的结果，避免重复计算
    dic = {0: 1}
    
    # 自底向上计算，从 c_1 算到 c_n
    for i in range(1, n + 1):
        dic[i] = 0
        for j in range(i):
            # 利用之前存储的结果直接计算
            dic[i] += dic[j] * dic[i - j - 1]

    return dic[n]
```



### 帕斯卡三角形
帕斯卡三角形（又称杨辉三角）是二项式系数在三角形中的一种几何排列，第 $n$ 行对应于二项式展开 $(x + y)^n$ 
的系数。
其核心递推关系为：每个数等于它上方两数之和
$$
\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}
$$

参考答案(递归):
```Python
def triangle(n) :
    if n == 0 :
        return [1]
    T = triangle(n-1)
    L = [1]+[0]*(n-1)+[1]
    for i in range(1,n) :
        L[i] = T[i-1]+T[i]
    return L
```

笔者答案(迭代):
```Python
def ligne_pascal(n: int) -> list[int]:
    res = [1]
    for _ in range(n):
        res = [1] + [res[i] + res[i+1] for i in range(len(res) - 1)] + [1]
    return res
```

两种算法的时间复杂度均为 $O(n^2)$ ,但递归算法的空间复杂度为 $O(n^2)$ ,迭代算法只有 $O(n)$


### 递归生成全排列

全排列是指将集合 $\{0, 1, \dots, n-1\}$ 中的所有元素按照一定顺序排列。我们可以利用**递归**的思想，通过“插入法”来构建所有可能的排列。

#### 构造规则
- 基础情况：大小为 1 的集合只有一种排列：$(0,)$。
- 递归步骤：假设已知大小为 $n-1$ 的所有排列，要生成大小为 $n$ 的排列，只需将新元素 $n-1$ 插入到每一个旧排列的 $n$ 个可能位置（从开头到结尾）中。

例如，从 $(1, 0)$ 生成大小为 3 的排列：
- 在位置 0 插入 2：$(2, 1, 0)$
- 在位置 1 插入 2：$(1, 2, 0)$
- 在位置 2 插入 2：$(1, 0, 2)$

#### 1. 辅助函数：在元组中插入元素
首先实现一个函数，用于将特定值插入到元组的所有可能位置，并返回生成的新元组列表。

```python
def liste_nouveaux(t: tuple[int], a: int) -> list[tuple[int]]:
    n = len(t)
    res = []
    # 遍历所有可能的插入位置 (0 到 n)
    for i in range(n + 1):
        # 利用切片分割元组
        cur_left, cur_right = t[:i], t[i:]
        # 拼接新元组：左部分 + (新元素,) + 右部分
        res.append(cur_left + (a,) + cur_right)

    return res
```
#### 2. 主函数：生成全排列
利用上述辅助函数，递归地生成 ${0,1,…,n−1}$ 的全排列
```python
def generer_permut(n: int):
    # 基础情况：n=0 或 n=1 时，返回包含唯一排列的列表
    if n == 0:
        return [(0,)]
    
    res = []
    # 1. 递归获取 n-1 的所有排列
    permuts_prev = generer_permut(n - 1)
    
    # 2. 对每个旧排列，插入新元素 n-1
    for permut in permuts_prev:
        new_permut = liste_nouveaux(permut, n - 1)
        # 将生成的新排列加入结果列表
        res.extend(new_permut)

    return res
```
#### 回溯法生成全排列
```Python
l = ['P', 'Y', 'T', 'H', 'O', 'N']
def permut(l: list[str]) -> list[str]:
    n = len(l)
    used = [False] * n
    res = []

    def dfs(cur):
        if cur:
            res.append(cur)
        
        for idx, char in enumerate(l):
            if not used[idx]:
                used[idx] = True
                dfs(cur + char)
                used[idx] = False

    dfs('')
    return res
```


