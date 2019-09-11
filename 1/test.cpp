#include <algorithm>
#include <cmath>
#include <regex>
#include <iostream>
using namespace std;

int main()
{
    string str;
    cin >> str;
    regex e("$,");
    smatch m;
    bool found = regex_search(str, m, e);
    cout << m[0] << endl;
    cout << m[1] << endl;
    system("pause");
    return 0;
}