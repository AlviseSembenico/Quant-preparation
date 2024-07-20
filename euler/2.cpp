#include <iostream>

using namespace std;
int main()
{
    int l1 = 0, l2 = 1;

    int res = 0;

    while (l1 <= 4e6)
    {
        int tmp = l1 + l2;
        l1 = l2;
        l2 = tmp;
        if (tmp % 2 == 0)
            res += tmp;
    }
    cout << res;

    return 0;
}