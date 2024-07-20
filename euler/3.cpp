#include <iostream>
#include <cmath>

using namespace std;

bool isPrime(int n)
{
    for (int i = 2; i < sqrt(n); i += 2)
        if (i % n == 0)
            return false;
    return true;
}

int largestPrimeNumber(long long int n)
{
    if (n == 1)
        return 1;
    if (n % 2 == 0)
        return largestPrimeNumber(n / 2);
    for (int i = 3; i < sqrt(n); i += 2)
    {
        if (!isPrime(i))
            continue;
        if (n % i == 0)
            return max(i, largestPrimeNumber(n / i));
    }
    return n;
}

int main()
{
    cout << largestPrimeNumber(600851475143);
}