# Report

## Introduction

Let's start by defining the first solution to our problem.

```
def rand10():
    while (n:=(rand7()-1)*7+ rand7()-1) >= 40:
        ...
    return (n%10)+1
\end{lstlisting}
```

### Rand7 calls analysis

With `n=(rand7()-1)*7+ rand7()-1)` we generate uniformly random number between 0 and 48.
$n\sim U[0,48]$, thus the probability of $n\geq 40$ is $\frac{9}{49}$.

Thus, if we look at $I_n$ as the indicator function for $n <40$, we have that $I_n$ is a Bernoulli r.v. 

Being interest in the number of times we need to sample from $n$, we can see that it behaves like a Geometric Distribution $I \sim Geo(p)$ with $p=\frac{40}{49}$. Thus the expected value for a successful sample is $\mathbb{E} \left[ Geo(p) \right] = \frac{1}{p} = \frac{49}{40} \approx 1.225$.

Since we do 2 call to `rand7` per sample, on average we expect to do 2.45 calls to `rand7`.


## Alternative solution
The key idea is not to generate two values at the same time but first generate the first value, if it's 7 then discard it until we have a value $a<7$. Then the second value $b$ can be $\le 5$ since $(6-1)*7=35$. 
We now compute the expected value of calls to be 
$$\mathbb{E} \left[  \text{calls to rand7}\right] = 7/6+7/5*1/6+5/7\approx 2.114$$ 
which is a better bound.

## Further improvements
Note that when we generate two numbers we have a uniform distribution on $[1,49]$, in practice throwing away $39% numbers in order to just generate one from 1 to 10.

If we want to generate 2 numbers from 1 to 10, we need to generate 3 numbers from 1,7, giving a uniform in $[1,343]$, in this case throwing away $243$ values, which improves our usage of the information from $10/49$ to $100/343$. We can continue this reasoning until we reach a sample size of $n=19$, where the ratio approaches the theoretical limit of $\frac{\log_{2}10}{\log_2 7}\approx 1.1832.$

If we look at the problem with a change of basis, from a base of 10 to a base of 7, we can simply get a number by multiplying by increasing powers of 7. 

The code can be changed accordingly to (here we just produce new results instead of consuming the list in case is not empty).
Note that $7^19=11398895185373143$ and $\max\{i \in \mathbb{N}: 10^i < 7^19\} = 16$.
Therefore, we keep all the values that are smaller that $10^{16}$.

```
def rand10(self):
    while (s := sum([(rand7()-1)* (7**i) for i in range(19)])) > int(1e16):
        ...

    while True:
        self.cache.append(s % 10+1)
        if s < 9:
            break
        s = s // 10
    return self.result.pop()
```


So we can generalize it now to a class in the following way:
```
class Rand10:
    def __init__(self):
        self.cache = []
        self.compute_batch()
        
    def get(self):
        if not self.cache:
            self.compute_batch()
        return self.cache.pop()
        
    def compute_batch(self):
        while (s := sum([(rand7()-1)* (7**i) for i in range(19)])) > int(1e16):
            ...

        while True:
            self.cache.append(s % 10+1)
            if s < 9:
                break
            s = s // 10
```
This allow us to store the values we generate and the ammortized cost is then
$$1+ \frac{7^{19}- 10^{16}}{7^{19}} \approx 1.1227$$