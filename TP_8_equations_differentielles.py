import numpy as np
import matplotlib.pyplot as plt
from typing import Callable

a = 3
b = 2
c = 2
d = 3
x_0 = 2 / 3
y_0 = 3 / 4

def FVL(X: np.ndarray) -> np.ndarray:
    x = X[0]
    y = X[1]

    part1 = a * x - b * x * y
    part2 = -c * y + d * x * y

    return np.array([part1, part2])

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


def H(x, y):
    global a, b, c, d
    return d * x - c * np.log(x) + b * y - a * np.log(y)


'''
X0 = np.array([x_0, y_0])
T = 3
N = 1000
solution = RK4(FVL, X0, T, N)

H_values = H(solution[0,:], solution[1, :])

plt.figure()
plt.plot(np.linspace(0, T, N+1), H_values, label="H(t)")
plt.xlabel('t')
plt.ylabel('H(x(t), y(t))')
plt.title('Conservation de l\'intégrale première')
plt.legend()
plt.show()



t = np.linspace(0, 3, 101)

plt.figure(figsize=(12,6))

s_e = Euler(FVL, np.array([x_0, y_0]), 3, 100)
plt.plot(t, s_e[0], 'b--', label="Euler x")
plt.plot(t, s_e[1], 'r--', label="Euler y")

s_R2 = RK2(FVL, np.array([x_0, y_0]), 3, 100)
plt.plot(t, s_R2[0], 'g-', label="RK2 x")
plt.plot(t, s_R2[1], 'm-', label="RK2 y")


s_R4 = RK4(FVL, np.array([x_0, y_0]), 3, 100)
plt.plot(t, s_R4[0], 'k-', label="RK4 x", linewidth=2)
plt.plot(t, s_R4[1], 'k-', label="RK4 y", linewidth=2)


plt.xlabel("temps")
plt.ylabel("population")
plt.show()

'''

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

dif = 1e-8
sigma += dif

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