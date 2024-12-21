from imco import *

with open("./files/99.txt", "r") as file:
    ns = []
    for line in file:
        # Split the line into two parts and convert to integers
        parts = line.strip().split(",")
        num1, num2 = map(int, parts)
        ns.append((num1, num2))


res = 0
for i in range(1, len(ns)):
    a, b = ns[i]
    c, d = ns[res]
    if b > d * log(c, a):
        res = i

print(res + 1)
