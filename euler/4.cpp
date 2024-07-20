#include <iostream>
#include <cmath>
#include <string>
#include <algorithm>
#include <vector>
using namespace std;

int main()
{
    int m = 0;
    for (int i = 999; i > 99; i--)
        for (int j = 999; j > 99; j--)
        {
            string s = to_string(i * j);
            string r = s;
            reverse(r.begin(), r.end());
            if (s == r && i * j > m)
                m = i * j;
        }
    cout << m;
}