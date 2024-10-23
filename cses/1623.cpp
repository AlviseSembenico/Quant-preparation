#include <cmath>
#include <iostream>
#include <vector>
#include <istream>
#include <iterator>
#include <sstream>
#include <string>
#include <set>
#include <algorithm>

using namespace std;
typedef long long int lint;

lint apple_division(lint n, vector<int> numbers)
{
    sort(numbers.begin(), numbers.end());
    reverse(numbers.begin(), numbers.end());

    lint total = 0;
    for (int i : numbers)
        total += i;
    lint d = total / 2;
    for (int i : numbers)
        if (i <= d)
            d -= i;

    return total % 2 + d;
}

int main()
{
    vector<int> numbers;
    string line;
    lint n;
    getline(cin, line);
    n = stoi(line);
    getline(cin, line);

    lint num;

    istringstream parser(line);

    numbers.insert(numbers.begin(),
                   istream_iterator<int>(parser), istream_iterator<int>());
    cout << apple_division(n, numbers);
}