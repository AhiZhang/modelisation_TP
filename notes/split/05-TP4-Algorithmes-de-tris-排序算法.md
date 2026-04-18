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






