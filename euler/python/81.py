from imco import *

M = np.loadtxt("./files/81.txt", dtype=int, delimiter=",")
print(M.shape)
m, n = M.shape


@cache
def f(x, y):
    if x == m - 1:
        if y == n - 1:
            return M[x, y]
        return M[x, y] + f(x, y + 1)
    if y == n - 1:
        return M[x, y] + f(x + 1, y)
    return M[x, y] + min(f(x + 1, y), f(x, y + 1))


print(f(0, 0))
