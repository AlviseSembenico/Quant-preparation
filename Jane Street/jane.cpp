#include <iostream>
#include <vector>
#include <array>
#include <functional>
#include <algorithm>
#include <thread>
#include <atomic>
#include <mutex>

using namespace std;

const int gridSize = 5;
const array<pair<int, int>, 8> moves = {{{2, 1}, {-2, 1}, {1, 2}, {-1, 2}, {2, -1}, {-2, -1}, {1, -2}, {-1, -2}}};
array<array<int, 6>, 6> inputArray = {{{0, 1, 1, 2, 2, 2},
                                       {0, 1, 1, 2, 2, 2},
                                       {0, 0, 1, 1, 2, 2},
                                       {0, 0, 1, 1, 2, 2},
                                       {0, 0, 0, 1, 1, 2},
                                       {0, 0, 0, 1, 1, 2}}};
array<array<int, 6>, 6> rotatedArray;
atomic<int> activeThreads{0};

void generatePaths(const vector<pair<int, int>> &path, function<void(const vector<pair<int, int>> &)> callback)
{
    auto pos = path.back();
    if (pos.first == gridSize && pos.second == gridSize)
    {
        activeThreads++;
        thread([callback, path]() { // Capture by value to avoid invalid reference issues
            callback(path);
            activeThreads--;
        })
            .detach();
        return;
    }

    for (auto &move : moves)
    {
        pair<int, int> new_pos = {pos.first + move.first, pos.second + move.second};
        if (new_pos.first > gridSize || new_pos.first < 0 || new_pos.second > gridSize || new_pos.second < 0)
        {
            continue;
        }

        if (find(path.begin(), path.end(), new_pos) == path.end())
        {
            vector<pair<int, int>> new_path = path;
            new_path.push_back(new_pos);
            generatePaths(new_path, callback);
        }
    }
}

vector<int> substitute(int a, int b, int c, const vector<pair<int, int>> &path, bool rotate)
{
    vector<int> res;
    auto &arr = rotate ? rotatedArray : inputArray;

    for (auto &[x, y] : path)
    {
        if (arr[x][y] == 0)
        {
            res.push_back(a);
        }
        else if (arr[x][y] == 1)
        {
            res.push_back(b);
        }
        else
        {
            res.push_back(c);
        }
    }

    return res;
}

int computeValue(const vector<int> &values)
{
    int result = values[0];
    for (size_t i = 1; i < values.size(); ++i)
    {
        if (values[i] == values[i - 1])
        {
            result += values[i];
        }
        else
        {
            result *= values[i];
        }
    }
    return result;
}

int min_value = 50;
bool isValid(int a, int b, int c, const vector<pair<int, int>> &path)
{
    if (a == b || a == c || b == c)
    {
        return false;
    }

    if (a + b + c > min_value)
    {
        return false;
    }

    for (bool rotate : {false, true})
    {
        auto substituted_values = substitute(a, b, c, path, rotate);
        if (computeValue(substituted_values) != 2024)
        {
            return false;
        }
    }

    return true;
}

void print2DArray(array<array<int, 6>, 6> arr, int rows, int cols)
{
    for (int i = 0; i < rows; ++i)
    {
        for (int j = 0; j < cols; ++j)
        {
            cout << arr[i][j] << " ";
        }
        cout << endl;
    }
}

int main()
{
    // Rotate the array by 90 degrees clockwise

    for (int i = 0; i < 6; ++i)
    {
        for (int j = 0; j < 6; ++j)
        {
            rotatedArray[j][5 - i] = inputArray[i][j];
        }
    }

    int ub = 50;
    vector<int> c_values = {11, 23, 2, 4, 8, 22, 44, 46};
    int counter = 0;
    mutex coutMutex;
    vector<pair<int, int>> start_path = {{0, 0}};
    generatePaths(start_path, [&](const vector<pair<int, int>> &path)
                  {
                      counter++;
                      if(counter <1120000)
                        return;
                      if ((counter + 1) % 1000 == 0)
                      {
                          cout << counter << endl;
                      }
                      for (int a = 1; a < ub; ++a)
                      {
                          for (int b = 1; b < ub; ++b)
                          {
                              for (int c : c_values)
                              {
                                  if (isValid(a, b, c, path))
                                  {
                                      min_value = a + b + c;
                                      lock_guard<mutex> guard(coutMutex);
                                      cout << a << " " << b << " " << c << " ";
                                      for (auto &[x, y] : path)
                                      {
                                          cout << "(" << x << "," << y << ") ";
                                      }
                                      cout << endl;
                                  }
                              }
                          }
                      } });

    // Wait until all threads are done
    while (activeThreads > 0)
    {
        this_thread::yield(); // Yield the main thread to allow other threads to finish
    }

    return 0;
}
