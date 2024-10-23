#include <cmath>
#include <iostream>
#include <vector>
#include <istream>
#include <iterator>
#include <sstream>
#include <string>
#include <set>

using namespace std;

long long int increasing(long long int n, vector<long long int> numbers)
{
    long long int prev = numbers[0];
    long long int res = 0;
    for (long long int i = 1; i < n; i++)
    {
        long long int v = numbers[i];
        // cout << prev << " " << v << " " << abs(v - prev) << endl;
        if (v < prev)
            res += abs(v - prev);
        prev = max(prev, v);
    }

    return res;
}

int main()
{
    vector<long long int> numbers;
    string line;
    long long int n;
    getline(cin, line);
    n = stoi(line);
    getline(cin, line);

    long long int num;

    istringstream parser(line);

    numbers.insert(numbers.begin(),
                   istream_iterator<long long int>(parser), istream_iterator<long long int>());
    cout << increasing(n, numbers);
}