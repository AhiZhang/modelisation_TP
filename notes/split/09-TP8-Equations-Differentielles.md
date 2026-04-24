# TP8: Equations Differentielles
在这次TP,我们研究比较复杂的微分方程的数值解,以方程
$$
\left\{
\begin{aligned}
x'(t) &= a x(t) - b x(t) y(t) \\
y'(t) &= -c y(t) + d x(t) y(t)
\end{aligned}
\right.
$$
为例,其中
$$
(x(0),y(0)) = (x_0,y_0)
$$
且设
$$
a = 3, b = 2, c = 2, d = 3, x_0 = \frac{2}{3}, y_0 = \frac{3}{4}
$$

## 计算导数值
输入$X$`=np.array([x, y])`,以`np.array`格式输出$(x', y')$
```Python
def FVL(X: np.ndarray) -> np.ndarray:
    x = X[0]
    y = X[1]

    part1 = a * x - b * x * y
    part2 = -c * y + d * x * y

    return np.array([part1, part2])
```
在了解了[numpy](#numpy)库后,我们就能够判断出这个函数的输入输出类型均为`ndarray`,而不是`list`或者别的什么东西


## 求微分方程的数值解
我们希望求从$t = 0$到$t = T$所有时刻的$x(t)$和$y(t)$的解,显然,不管是我们还是计算机,都不大可能求出无限细分的时间区间上每个
$x(t)$和$y(t)$的数值,于是我们退而求其次,将区间分为$N$个部分,步长$h= \frac{T}{N}$,则离散时间点
$$
t_0 = 0, t_1 = h, ..., t_N = T
$$
利用递推公式,从当前时刻的值推算下一时刻的值
最终得到一组离散的近似解
显然,步长$h$越小,我们求得的数值越精准
### 一阶显式Euler法
最简单的方法,当前点的导数作为斜率,将两点之间的函数近似为直线,推到下一个时间点的函数值:
$$
X_{n+1} = X_n + hF(X_n)
$$
```Python
def Euler(F: Callable[[np.ndarray], np.ndarray], 
          X0: np.ndarray, 
          T: float, 
          N: int) -> np.ndarray:
    h = T / N
    n = np.size(X0)
    S = np.zeros((n, N + 1))
    S[:, 0] = X0
    Xn = X0
    for i in range(N):
        Xn += h * F(Xn)
        S[:, i + 1] = Xn
    return S
```
数值分析课上并没有介绍解微分方程数值解的具体方式,不过我们能够从给出的例子里面管窥其思想  
在初见这个函数时,不知所云很正常,
首先,我们要要了解`ndarray`的切片规则

返回的矩阵`S`表示微分方程数值解的轨迹  
- 每一列表示某一时刻的状态向量
- 每一行表示某个变量随时间的变化  
对于状态向量$X = (x,y)$：
$$
S = 
\begin{bmatrix}
x_0 & x_1 & x_2 & \dots & x_N \\
y_0 & y_1 & y_2 & \dots & y_N
\end{bmatrix}
$$

其中：
- 每一行代表一个状态变量（$x,\ y$）  
- 每一列对应一个时刻：  
  第 0 列 $\leftrightarrow t=0$  
  第 1 列 $\leftrightarrow t=h$  
  第 2 列 $\leftrightarrow t=2h$  
  $\dots$  
  第 $N$ 列 $\leftrightarrow t=T$  

此外,在标注`F`的类型时,我们使用了`Callable`,这表示`F`是一个函数

### 二阶Runge-Kutta法
我们回顾[TP6_中点法](#中点法),为了减小积分的误差,我们没有使用区间端点的函数值,而选择了区间中点的函数值  
同理,在这里,我们也可以选择区间中点来计算下一个点的数值:  
$$
\begin{aligned}
k_1 &= F(X_n) \\
k_2 &= F\left(X_n + \frac{h}{2}k_1\right) \\
X_{n+1} &= X_n + h\,k_2
\end{aligned}
$$


```Python
def RK2(F: Callable[[np.ndarray], np.ndarray], 
        X0: np.ndarray, 
        T: float, 
        N: int) -> np.ndarray:
    h = T / N
    n = np.size(X0)
    S = np.zeros((n, N + 1))
    S[:, 0] = X0
    Xn = X0
    
    for i in range(N):
        k1 = F(Xn)
        k2 = F(Xn + h/2 * k1)
        Xn = Xn + h * k2
        S[:, i+1] = Xn
        
    return S
```

在中点法求积分的部分,我们直接使用了
$$
area = f(middle) * h
$$
来计算中点的函数值,但为什么这里却需要先通过计算端点的斜率来得到中点的斜率,而不直接计算中点的斜率?

### 四阶Runge-Kutta法
用四个点上的斜率加权平均得到斜率 $k$ ,再更新 $X_{n + 1}$ 
$$
\left\{
\begin{aligned}
k_0 &= F(X_n), \\
k_1 &= F\left(X_n + \frac{h}{2}k_0\right), \\
k_2 &= F\left(X_n + \frac{h}{2}k_1\right), \\
k_3 &= F\left(X_n + h k_2\right), \\
k &= \frac{k_0}{6} + \frac{k_1}{3} + \frac{k_2}{3} + \frac{k_3}{6}, \quad X_{n+1} = X_n + h k
\end{aligned}
\right.
$$

```Python
def RK4(F: Callable[[np.ndarray], np.ndarray], 
        X0: np.ndarray, 
        T: float, 
        N: int) -> np.ndarray:
    h = T / N
    n = np.size(X0)
    S = np.zeros((n, N + 1))
    S[:, 0] = X0
    Xn = X0
    for i in range(N):
        k0 = F(Xn)
        k1 = F(Xn + h * k0 / 2)
        k2 = F(Xn + h * k1 / 2)
        k3 = F(Xn + h * k2)
        k = k0 / 6 + k1 / 3 + k2 / 3 + k3 / 6
        Xn = Xn + h * k
        S[:, i + 1] = Xn
        
    return S
```


### 二阶Adams-Bashforth法
 $n$ 阶Adams-Bashforth法的本质是通过对前 $n$ 个点的斜率加权计算下一个点的斜率,各个点的斜率如何推出并不是本文重点,对于二阶AB法,我们有:
$$
X_{n+1} = X_n + \frac{h}{2}(3F(X_n) - F(X_{n - 1}))
$$
在实际应用时,我们先用别的方法(如二阶RK法)算出这个方法无法算出的 $F_1$ ,再进行递推
 
```Python
def AB2(F: Callable[[np.ndarray], np.ndarray], 
        X0: np.ndarray, 
        T: float, 
        N: int) -> np.ndarray:
    h = T / N
    n = np.size(X0)
    S = np.zeros((n, N+1))
    S[:, 0] = X0

    X1 = RK2(F, X0, h, 1)[:, -1]
    S[:, 1] = X1

    for i in range(1, N):
        S[:, i+1] = S[:, i] + (h/2) * (3*F(S[:, i]) - F(S[:, i-1]))
    return S
```
对应地,如果要使用 $p$ 阶AB法,就要先用别的方法算出 $F_1~F{p-1}$ 一共 $p-1$ 个初始解才能启动  
~~我说精确度卡我启动了~~

### 隐式Euler法

什么是隐式?  
在计算 $X_n$ 时,公式里同时出现 $X_n$ 和未知的 $X_{n+1}$ 的方法就是隐式法  
根据隐式Euler法,我们有:  
$$
X_{n+1} = X_n + hF(X_{n+1})
$$
显然,我们无法直接计算 $X_{n+1}$ ,需要借助牛顿迭代法  
定义函数 
$$
G(X) = X - X_n -  hF(X)
$$
求解
$$
G(X_{n+1}) = 0
$$
对向量方程 $G(X)=0$,设第 $k$ 次迭代近似解为 $X^{(k)}$
迭代:
$$
X^{(k+1)} = X^{(k)} - [J_G(X^{(k)})]^{-1}G(X^{(k)})
$$
其中 $J_G$ 是 $G$ 的Jacobian矩阵  
求 $G$ 的Jacobian矩阵
$$
G(X) = X - X_n - hF(X)
$$
求导:
$$
J_G(X) = I - h \cdot J_F(X)
$$
其中:
- $I$ :单位矩阵
- $J_F(X) = DF(X)$ 为函数 $F$ 的Jacobian矩阵

我们初始猜测 $X^{(0)} = X_n$ ,每次迭代:
$$
\begin{cases}
G_k = X^{(k)} - X_n - hF(X^{(k)}) \\
J_k = I - hDF(X^{(k)}) \\
\text{解线性方程组：}J_k \delta = -G_k \\
X^{(k+1)} = X^{(k)} + \delta
\end{cases}
$$

若干次迭代之后,有:
$$
 X^{(fin)} = X_{n+1}
$$

代码实现:
```Python
def IEuler(F: Callable[[np.ndarray], np.ndarray], 
           DF: Callable[[np.ndarray], np.ndarray], 
           X0: np.ndarray, 
           T: float, 
           N: int) -> np.ndarray:
    h = T / N
    n = np.size(X0)
    S = np.zeros((n, N + 1))
    S[:, 0] = X0
    for i in range(N):
        Xn = S[:, i]
        X_next = Xn.copy()
        for _ in range(10):
            G = X_next - Xn - h * F(X_next)
            DG = np.eye(n) - h * DF(X_next)
            delta = np.linalg.solve(DG, -G)
            X_next = X_next + delta
        S[:, i+1] = X_next
    return S
```

### Crank-Nicholson法
我们有:
$$
X_{n+1} = X_n + \frac{h}{2}(F(X_n) + F(X_{n+1}))
$$

类似地,定义:
$$
G(X) = X - X_n - \frac{h}{2}(F(X_n) + F(X))
$$
求解：
$$
G(X_{n+1}) = 0
$$
迭代:
$$
X^{(k+1)} = X^{(k)} - [J_G(X^{(k)})]^{-1} G(X^{(k)})
$$

求 $G$ 的Jacobian矩阵
$$
J_G(X) = I - \frac{h}{2}\cdot J_F(X)
$$
其中:
- $I$ 为单位矩阵
- $J_F(X)=DF(X)$ 为函数 $F$ 的Jacobian矩阵
我们初始猜测 $X^{(0)} = X_n$ ,每次迭代:

$$
\begin{cases}
G_k = X^{(k)} - X_n - \dfrac{h}{2}(F(X_n)+F(X^{(k)}))\\[4pt]
J_k = I - \dfrac{h}{2}\,DF(X^{(k)})\\[4pt]
\text{求解线性方程组：} \ J_k \delta = -G_k\\[4pt]
X^{(k+1)} = X^{(k)} + \delta
\end{cases}
$$

若干次迭代之后,有:
$$
 X^{(fin)} = X_{n+1}
$$
代码实现:
```Python
def CN(F: Callable[[np.ndarray], np.ndarray], 
       DF: Callable[[np.ndarray], np.ndarray], 
       X0: np.ndarray, 
       T: float, 
       N: int) -> np.ndarray:
    h = T / N
    n = np.size(X0)
    S = np.zeros((n, N + 1))
    S[:, 0] = X0
    for i in range(N):
        Xn = S[:, i]
        X_next = Xn.copy()
        for _ in range(10):
            G = X_next - Xn - (h / 2) * (F(Xn) + F(X_next))
            DG = np.eye(n) - (h / 2) * DF(X_next)
            delta = np.linalg.solve(DG, -G)
            X_next = X_next + delta
        S[:, i+1] = X_next
    return S
```

## 测试
### 首次积分
使用以上求解方法绘制首次积分:
$$
H(x,y) = dx -c \space ln(x) + by -a \space ln(y)
$$
以四阶RK方法为例:
```Python
def H(x, y):
    global a, b, c, d
    return d * x - c * np.log(x) + b * y - a * np.log(y)

X0 = np.array([x_0, y_0])
T = 3
N = 10000
solution = RK4(FVL, X0, T, N)

H_values = H(solution[0,:], solution[1, :])

plt.figure()
plt.plot(np.linspace(0, T, N+1), H_values, label="H(t)")
plt.xlabel('t')
plt.ylabel('H(x(t), y(t))')
plt.title('Conservation de l\'intégrale première')
plt.legend()
plt.show()
```
需要注意的是,`N`的取值不应该太小,否则最后得到的图像可能不理想
![n=10000](split\images\Figure_1.png "n=10000时得到的图像")
![n=1000](split\images\Figure_2.png "n=1000时得到的图像")

### Lorenz混沌系统
$$
\left\{
\begin{aligned}
y_1'(t) &= \sigma \left( y_2(t) - y_1(t) \right) \\
y_2'(t) &= r y_1(t) - y_2(t) - y_1(t) y_3(t) \\
y_3'(t) &= y_1(t) y_2(t) - b y_3(t)
\end{aligned}
\right. ,
$$

其中
$$
\sigma = 10, r = 28, b = \frac{8}{3}
$$
#### 绘制3D图和投影图
```Python
sigma = 10
b = 8 / 3
r = 28
def Lorenz(Y):
    y_1 = Y[0]
    y_2 = Y[1]
    y_3 = Y[2]
    global sigma, b, r

    composante1 = sigma * (y_2 - y_1)
    composante2 = r * y_1 - y_2 - y_1 * y_3 
    composante3 = y_1 * y_2 - b * y_3
    return np.array([composante1, composante2, composante3])

Y0 = np.array([1, 0, 0])
T = 100
N = 10000
Lrz_solution = RK4(Lorenz, Y0, T, N)

fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(111, projection='3d')
ax.plot(Lrz_solution[0,:], Lrz_solution[1,:], Lrz_solution[2,:], linewidth=0.6)
ax.set_xlabel('y1')
ax.set_ylabel('y2')
ax.set_zlabel('y3')
plt.title('Attracteur de Lorenz 3D (RK4)')
plt.show()

plt.figure()
plt.plot(Lrz_solution[0,:], Lrz_solution[2,:])
plt.xlabel('y1')
plt.ylabel('y3')
plt.title('Attracteur de Lorenz (RK4)')
plt.show()
```

#### 模拟微小扰动
我们对
- 初始位置
- $\sigma$
- 时间步长 $h$  
作微小扰动(10^{-8}),对比结果差异



