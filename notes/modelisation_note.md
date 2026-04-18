# 写在前面
这篇文档旨在从建模课的习题中提取出
1. 思维量较大
2. 解决方法独特
3. 笔者题解优于参考答案  

的题目,用于课后复盘,文档里的解答在思想,实现过程等方面与参考答案有时不完全一致,若有错漏,以参考答案为准  
若没有专门标注，本文档在讨论复杂度时一律都指**最差情况**下的时间/空间复杂度
本文档假设输入数据均符合规范




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


# TP2:
## 拉马努金公式
> $$
> \frac{1}{\pi} = \frac{2\sqrt{2}}{9801} \lim_{n \to +\infty} \sum_{k=0}^{n} \frac{(4k)! (1103 + 26390k)}{(k!)^4 396^{4k}}
> $$ 


本题难度不大,将它放上来的原因在于笔者在解题时直接调用了`math`库来计算 $k!$ 和 $4k!$ ,而参考答案则定义了一个函数以计算阶乘,计算每一项时都会重新计算阶乘,效率太低  

参考答案
```Python
def produit_cons(a,b) :
    p = a
    for i in range(a+1,b+1) :
        p = p*i
    return p
def ramanujan(n) :
    L = []
    un = (2**(1.5)/9801)*1103
    S = 0
    for i in range(0,n) :
        S = S + un
        L.append(S)
        un = produit_cons(4*i+1,4*i+4)*(1+26390/(1103+26390*i))*un/((i+1)**4*396**4)
    return S
```

优化后答案

```Python
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
```

### 连分数

任意正有理数 $\frac{p}{q} \in \mathbb{Q}^+$ 均可表示为**连分数**的形式。即存在非负整数序列 $a_0, \dots, a_k$ 使得：

$$
\frac{p}{q} = a_0 + \frac{1}{a_1 + \frac{1}{a_2 + \frac{1}{\ddots + \frac{1}{a_k}}}}
$$

该序列通常简记为 $[a_0; a_1, \dots, a_k]$。此概念亦可推广至无理数，通过无限序列 $a_0, a_1, \dots$ 表示实数，其前 $k$ 项构成的有理数称为**渐近分数**，常用于实数的有理逼近

---

#### 1. 有理数转连分数
利用**辗转相除法**，可以将分数 $\frac{p}{q}$ 分解为整数序列

```python
def decomposition(p: int, q: int) -> list[int]:
    result = []
    # 增加计数防止死循环（虽对于有理数必然终止）
    count = 0
    while q != 0 and count < 100:
        a = p // q          # 取整得到系数 a_i
        result.append(a)
        p, q = q, p % q     # 更新余数
        count += 1
    return result
```
#### 2. 连分数还原为分数

给定整数列表 $L$，将其逆向还原为分数形式 $\frac{p}{q}$
算法逻辑是从列表末尾向前迭代，维护分子`upper`和分母`down`
```python
def fraction(L: list[int]) -> list[int]:
    if not L:
        return [0, 1]
    
    # 从最后一项开始，初始为 a_k / 1
    upper, down = L[-1], 1
    
    # 逆向迭代
    for a in reversed(L[:-1]):
        # 新分子 = a * 旧分子 + 旧分母
        # 新分母 = 旧分子
        upper, down = a * upper + down, upper

    return [upper, down]
```

#### 3. 实数的连分数展开
对于实数 $x$，可以通过不断取整并取倒数的方式获取其连分数的前 $n$ 项系数
```python
def reduite(x: float, n: int) -> list[int]:
    L = []
    for _ in range(n + 1):
        a = int(x)          # 取整数部分
        L.append(a)
        x = x - a           # 取小数部分
        if x == 0:          # 若为整数则终止
            break
        x = 1 / x           # 取倒数

    return L
```
#### 4. 实数的有理逼近
利用连分数的性质，通过不断计算渐近分数来逼近实数 $x$，直到满足精度 $\varepsilon$
```python
def approx(x: float, eps: float) -> tuple[int, int]:
    L = []
    current_x = x
    
    while True:
        a = int(current_x)
        L.append(a)
        
        # 计算当前的渐近分数 p/q
        p, q = fraction(L)
        
        # 检查是否满足精度要求
        if abs(x - p / q) < eps:
            return (p, q)
            
        # 准备下一次迭代
        current_x -= a
        if current_x == 0:
            return (p, q)
            
        current_x = 1 / current_x
```

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


# TP4: Algorithmes de tris 排序算法
本次TP例题均为经典的排序算法，在此全部写上

## Tris comptage 计数排序
通过计算列表所有元素出现的次数来排序,只适用于列表元素比较小的情况
| 时间复杂度 | 空间复杂度 |
|--------|---------|
| $O(n)$  | $O(n)$ |

```Python
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
```


## Tris par selection 选择排序
1. 把列表分成已排序和未排序两部分
2. 每一轮在未排序部分里找到最小值
3. 把这个值交换到未排序部分的开头
4. 重复直到整个列表有序

| 时间复杂度 | 空间复杂度 |
|--------|---------|
| $O(n^2)$  | $O(1)$ |

伪代码：

```pseudocode
tri_selection(L)
/* L est une liste d'éléments à trier                                 */
n = longueur de L
pour i allant de 0 à n-1 inclus faire
    indice = i
    pour j allant de i +1 à n-1 inclus faire
        si L[j] < L[indice] alors
            indice = j
        fin
    fin
    échanger L[i] et L[indice]
fin
```

Python实现：
```Python
def tri_selection(L: list[int]) -> list[int]:
    n = len(L)
    for i in range(n):
        indice = i
        for j in range(i + 1, n):
            if L[j] < L[indice]:
                indice = j
        L[i], L[indice] = L[indice], L[i]
    return L

```

## Tri insertion 插入排序
1. 记要排序的列表为`L`，初始化`i = 1`
2. 记`L[i]`为`valeur`
3. 向左比较，若`valeur`大于左边的数，则交换两个数的位置
4. 一直往左，直到`valeur`左边的数不大于`valeur`或者`valuer`走到最左边
5. `i += 1`，直到整个列表有序
   
| 时间复杂度 | 空间复杂度 |
|--------|---------|
| $O(n^2)$  | $O(1)$ |
Python实现：
```Python
def tri_insertion(L: list[int]) -> list[int]:
    n = len(L)
    for i in range(1, n):
        valeur = L[i]
        j = i
        while j > 0 and L[j-1] > valeur:
            L[j] = L[j-1]
            j -= 1
        L[j] = valeur
    return L
```

## Tri fusion 归并排序
归并排序是分治思想的典型体现
### 什么是分治思想?

分治法是一种算法设计思想，其核心在于将一个复杂的问题分解为若干个规模较小的子问题，递归地解决这些子问题，然后将子问题的解合并为原问题的解。分治法的步骤通常包括：
1. 分解:将问题分解为若干个规模较小、相互独立的子问题。
2. 解决:递归地求解每个子问题。
3. 合并:将各个子问题的解合并成原问题的解。

### 归并排序是怎么被想出来的?
我们借助分治思想来思考如何排序一个序列:
1. 分解:要想排序一整个列表L,我们不妨把L拆成两半,再将两个分开的列表分别排序,最后用某种方法将这两个列表合并成一个有序的
2. 解决:那么这两个独立的列表又应该怎么排序呢?我们不妨继续将列表拆开,直到列表里只有一个元素.只有一个元素的列表肯定是有序的
3. 合并:把两个有序列表合并成一个完整的有序列表
现在距离解决问题只差最后一步:如何把两个有序列表合成为一个有序列表?

### `fusion`归并函数
假设我们有`L`,`M`两个有序列表,编写一个函数fusion以合成`L`和`M`
```Python
def fusion(L: list[int], M: list[int]) -> list[int]:
    if not L or not M:
        return L + M

    if L[0] < M[0]:
        return [L[0]] + fusion(L[1:], M)

    return [M[0]] + fusion(L, M[1:])
```

### 归并排序
现在通过`fusion`函数,我们已经能够把两个有序列表合成为一个有序列表了
| 时间复杂度 | 空间复杂度 |
|--------|---------|
| $O(nlog(n))$  | $O(n)$ |
```Python
def tri_fusion(L:list[int]) -> list[int]:
    L_len = len(L)
    if L_len <= 1:
        return L

    n = L_len // 2

    L_left = L[:n]
    L_right = L[n:]

    L_left_sorted = tri_fusion(L_left)
    L_right_sorted = tri_fusion(L_right)

    return fusion(L_left_sorted, L_right_sorted)

```

## Tri rapide 快速排序
### 思考
在使用归并排序时,我们先把数组切成了两半,再分别对这两个数组进行排序.有时这种切分方式显得过于粗暴,导致我们在合并数组时仍然需要一一比对.能否构思出一种切法,使得在合并时不用比对,直接接上去就行了?
当然可以,只需要找到一个标准值`index`,把小于`index`的数放在左边分为一组,大于`index`的数放在右边分为一组,在分别排序后,就能直接对接两个数组得到一个有序数组了
### 快速排序
| 时间复杂度 | 空间复杂度 |
|--------|---------|
| 平均$O(nlog(n))$,最差$O(n^2)$  | 平均$O(log(n))$,最差$O(n)$   |
```Python
def tri_rapide(L: list[int], left: int, right: int) -> None:
    if left >= right:
        return

    pivot = L[left]
    smaller_pointer = left + 1
    bigger_pointer = right

    while smaller_pointer <= bigger_pointer:
        while smaller_pointer <= bigger_pointer and L[smaller_pointer] <= pivot:
            smaller_pointer += 1

        while smaller_pointer <= bigger_pointer and L[bigger_pointer] >= pivot:
            bigger_pointer -= 1
        
        if smaller_pointer < bigger_pointer:
            L[smaller_pointer], L[bigger_pointer] = L[bigger_pointer], L[smaller_pointer]

    L[left], L[bigger_pointer] = L[bigger_pointer], L[left]
    pivot_index = bigger_pointer

    tri_rapide(L, left, pivot_index - 1)
    tri_rapide(L, pivot_index + 1, right)
```

## Tri par tas 堆排序
这种算法还是挺难的,TP用了十一题才弄明白,我在此尽量写清楚

### 什么是堆?
堆是一种非线性结构，可以把堆看作一棵二叉树，也可以看作一个数组，即：堆就是利用完全二叉树的结构来维护的一维数组
堆可以分为大顶堆和小顶堆
- 大顶堆：每个结点的值都大于或等于其左右孩子结点的值  
- 小顶堆：每个结点的值都小于或等于其左右孩子结点的值  
> 给定一个长度为 $n$ 的实数列表 $L$，称 $L$ 是一个**最大堆**，当且仅当满足如下性质：
>
> $$
> \forall i \in \{1, 2, \dots, n-1\},\quad L[i] \ge L\left\lfloor \frac{i-1}{2} \right\rfloor
> $$
TP上的定义有点让人困惑，这分明是最大堆的定义，但剩下的题目几乎均处理最小堆，我们在此给出最小堆的定义
> 给定一个长度为 $n$ 的实数列表 $L$，称 $L$ 是一个**最小堆**，当且仅当满足如下性质：
>
> $$
> \forall i \in \{1, 2, \dots, n-1\},\quad L[i] \le L\left\lfloor \frac{i-1}{2} \right\rfloor
> $$
我们可以实现如下判断一个列表是不是最大堆\最小堆的函数
```Python
def est_tas_max(L: list[int]) -> bool:
    return all(L[i] >= L[(i - 1) // 2] for i in range(1, len(L)))

def est_tas_min(L: list[int]) -> bool:
    return all(L[i] <= L[(i - 1) // 2] for i in range(1, len(L)))
```

### 堆的操作
下面,我们要在保持堆的性质时操作堆中元素
#### `diminue()`减小某元素
我们把堆`L`的索引`i`处的元素替换为`a`,且`a < L[i]`,并返回操作是否成功

```Python
def diminue(L: list[int], i: int, a: int) -> bool:
    n = len(L)
    if i >= n or a > L[i]:
        return False

    L[i] = a
    parent = (i - 1) // 2
    while i > 0 and L[parent] > L[i]:
        L[i], L[parent] = L[parent], L[i]
        i = parent
        parent = (i - 1) // 2

    return True

```

#### `augument()`增大某元素
我们把堆`L`的索引`i`处的元素替换为`a`,且`a > L[i]`,并返回操作是否成功  
**注意：在编写时(2026/4/3)笔者注意到参考答案存在问题**  
参考答案：
```Python
def augmente(L,i,a) :
    n = len(L)
    if i >=n or L[i] > a :
        return False
    else :
        L[i] = a
        g, d = 2*i+1, 2*i+2
        if g >= n :
            return True
        if d >= n :
            if L[g] < L[i] :
                L[g],L[i] = L[i],L[g]
            return True
            # 在交换之后的子树可能仍然不满足堆的定义，需要进一步检查，而这里直接返回True
        if L[g] >= a and L[d] >= a :
            return True
        if L[g] >= L[d] :
            indice = d
        else :
            indice = g
        L[i] = L[indice]            # 原来应该交换i和indice的值，这里只有赋值而没有交换
        # 前面均有返回bool值，而这里却没有返回值
```

笔者答案：

```Python
def augment(L: list[int], i: int, a: int) -> bool:
    n = len(L)
    if i >= n or a < L[i]:
        return False

    L[i] = a

    while True:
        left = 2 * i + 1
        right = 2 * i + 2
        smallest = i

        if left < n and L[left] < L[smallest]:
            smallest = left
        if right < n and L[right] < L[smallest]:
            smallest = right

        if smallest == i:
            break

        L[i], L[smallest] = L[smallest], L[i]
        i = smallest

    return True
```
#### `ajout()`增加一个元素
我们接收一个数`a`,并将其加入`L`中
```Python
def ajout(L: list[int], a: int):
    L.append(a)
    diminue(L,len(L)-1,a)
    return
```
#### `extraire_min()`提取最小值
我们接收一个`L`（表示一个堆）作为参数，并返回`L`中的最小值

该函数同时会对 L 执行以下修改：
1. 用 L 的最后一个元素替换最小值
2. 删除 L 的最后一个元素
3. 执行一系列交换操作，以维持堆的结构不变

```Python
def extraire_min(L: list[int]) -> int:
    heap_top = L[0]
    last_elem = L.pop()
    augument(L, 0, last_elem)
    return heap_top
```

#### `construction_tas()`把列表变为堆
我们接收一个列表`L`作为参数，并返回构建完成的堆。
构建方式为：初始化一个空列表 T，依次将 L 中的每个元素添加到 T 中，且每次添加后都保持 T 为堆结构
```Python
def construction(L: list[int]) -> list[int]:
    res = []
    for elem in L:
        ajout(res, elem)

    return res
```

### 实现堆排序
在初步了解过堆以及有了以上对堆的操作后，我们就能写出堆排序了
由本题得出的堆排序：
| 时间复杂度 | 空间复杂度 |
|--------|---------|
| $O(nlog(n))$  | $O(n)$ |
```Python
def tri_par_tas(L: list[int]) -> list[int]:
    L_heap = construction(L)
    res = []
    for i in range(len(L)):
        res.append(extraire_min(L_heap))

    return res
```
---

不占用额外空间的堆排序：
| 时间复杂度 | 空间复杂度 |
|--------|---------|
| $O(nlog(n))$  | $O(1)$ |

```Python
def sift_down(arr: list[int], n: int, i: int) -> None:
    # 下沉调整（大顶堆）
    while True:
        largest = i       # 父节点
        left = 2 * i + 1  # 左孩子
        right = 2 * i + 2 # 右孩子

        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right

        if largest == i:
            break  # 已经满足堆性质

        arr[i], arr[largest] = arr[largest], arr[i]
        i = largest


def heap_sort(arr: list[int]) -> None:
    n = len(arr)

    # 1. 自底向上建堆 O(n)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(arr, n, i)

    # 2. 逐个提取堆顶 O(n log n)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # 堆顶放到末尾
        sift_down(arr, i, 0)             # 重新调整堆
```

Python也有自带的堆模块`heap`,封装了对堆的操作,要指出的是,这个库只支持最小堆,当需要建最大堆时,不妨存入原数的负值,取出时再取一次负:
|函数  |  功能  |  	Python heapq 函数
|--------|---------|---------|
|diminue / augment  |  调整  |  内部自动实现
|ajout(L, a)  |  添加元素  |  heapq.heappush(L, a)
|extraire_min(L)  |  取出最小值  |  heapq.heappop(L)
|construction(L)  |  建堆  |  heapq.heapify(L)

| 时间复杂度 | 空间复杂度 |
|--------|---------|
| $O(nlog(n))$  | $O(1)$ |

```Python
import heapq

def heap_sort(arr: list[int]) -> list[int]:
    heapq.heapify(arr)
    return [heapq.heappop(arr) for _ in range(len(arr))]
```






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





# 一些细节
本文内容大部分来自Python官方技术文档[Python标准库]((https://docs.python.org/zh-cn/3/library/index.html))  
如果有时间，**强烈建议直接阅读文档**

## Python运算的底层实现


## 误差问题
在
[TP1](#tp1-revision-复习我们之前学过吗), Exo10
我们给出了这种解法:
```Python
def est_somme_de_carres(n: int) -> bool:
    for i in range(int(n ** 0.5) + 1):
        b =  n - i ** 2
        if b == int(b ** 0.5) ** 2:
            return True
    return False
```
但由于浮点数误差，使用`** 0.5`存在精度风险，对于一个很大的完全平方数：

```Python
n = 1000000000000000000000000000000000000     # 1e36
n_sqare = n * n
print(n == int(n_sqare ** 0.5))               # 输出: False
```
浮点数开方的精度问题会导致算法出错，因此在面对特别巨大的输入时，建议使用`math.isqrt()`避免这类错误




## 如何选择合适的算法？
**这两张表只作参考之用，以实际为准**  
Python每秒大约能运算$10^6$~$10^7$次

| 算法 / 写法 | 时间复杂度 | 空间复杂度 |
| :--- | :--- | :--- |
| 递归（无记忆化） |  $O(2^n)$  |  $O(n)$  |
| 递归 + 记忆化 |  $O(n)$  |  $O(n)$  |
| 动态规划（迭代） |  $O(n)$  |  $O(1)$  /  $O(n)$  |
| 暴力枚举排列 |  $O(n!)$  |  $O(n)$  |
| 二分查找 |  $O(\log n)$  |  $O(1)$  |
| 排序（内置） |  $O(n \log n)$  |  $O(n)$  |

为了避免超时，建议把输入数据`n`带入到对应算法的时间复杂度里，若结果大于$10^6$，则算法几乎必然超时  
或者根据输入的数据规模反向考虑使用的算法
| 输入数据  $n$  的范围 | 推荐的时间复杂度 | 可选的算法举例 |
| :--- | :--- | :--- |
|  $n \le 10$  |  $O(n!)$  | 暴力全排列、深度搜索 |
|  $n \le 20$  |  $O(2^n)$  | 递归、位运算暴力搜索 |
|  $n \le 100$  |  $O(n^3)$  | 简单的三维动态规划、Floyd算法 |
|  $n \le 2000$  |  $O(n^2)$  | 简单的二维动态规划、冒泡排序 |
|  $n \le 10^5$  |  $O(n \log n)$  | 归并排序、快速排序、二分查找 |
|  $n \le 10^6$  |  $O(n)$  | 线性扫描、哈希表统计 |
|  $n > 10^9$  |  $O(\log n)$  /  $O(1)$  | 数学公式推导、二分答案 |


## 异常和异常处理
### 异常
在Python中，所有的异常均是对象，以下是一些常见的异常类型：

|    异常名称  |  异常描述  |
|-----------|-----------|
| ZeroDivisionError  | 除(或取模)零 |
| IndexErrorr  | 序列中没有此索引 |
| SyntaxError  | 语法错误 |
| TypeError  | 类型无效 |





### 自定义异常c
```Python
class ExempleError():
    pass
```
### 捕获异常
```Python
try:
    pass

except XXXError:
    pass
```

`else`和`finally`：
1. `else`
   只有`try`里面的代码完全正常执行之后才能执行

2. `finally`
    100%会执行

```Python
try:
    # 可能出错的代码
    
except 异常类型1:
    # 捕获到异常类型1时执行

except 异常类型2:
    # 捕获到异常类型2时执行

else:
    # 没有发生任何异常时执行

finally:
    # 无论是否出错、是否捕获，一定会执行
```
# 一些Python语法糖
> 什么叫我的代码还不够Pythonic?



# 一些有用的库

## `time`库：计算程序的运行时间
### 精度要求不高\程序时间较长
一般使用`time`库以计算程序运行时间
```Python
import time
def main():
    pass

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"It takes {end_time - start_time:.6f}s to run the program")
```
### 精度要求较高\程序时间较短
1. 多跑几次
```Python
import time

def main():
    return

if __name__ == "__main__":
    start_time = time.time()
    for _ in range(10000)
        main()
    end_time = time.time()
    print(f"It takes {end_time - start_time:.6f}s to run the program 100000 times")
```
2. 使用`time.perf_counter()`
```Python
import time

def main():
    for i in range(1000000):
        pass

if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f"It takes {end_time - start_time:.6f}s to run the program")
```

## `math`库：获得常量的值，计算初等函数
### 获取常量
```Python
import math

print(math.pi)
print(math.e)
print(math.inf)
```
### 计算初等函数
```Python
import math

x, y = 5, 3
print(math.pow(x, y))
print(math.exp(x))
```

## `random`库：生成伪随机数
### 在某个区间生成伪随机数
```Python
import random

x = random.randrange(50)       # 生成50(不含)以下的伪随机整数
print(x)
y = random.randrange(0, 100)   # 生成0(含)以上,100(不含)以下的伪随机整数
print(y)
```
### 打乱列表
```Python
import random

l1 = [0, 1, 2, 3, 4, 5]
random.shuffle(l1)             # 打乱列表(原地修改，无返回值)
print(l1)
```