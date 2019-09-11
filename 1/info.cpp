#include <algorithm>
#include <cmath>
#include <regex>
#include "info.h"

using namespace std;

people_info::people_info()
{
}

people_info::~people_info()
{
}

string people_info::set_name(string ad)
{
    regex e("(.+)，(.*)");
    smatch result;
    bool found = regex_search(ad, result, e);
    if (found)
    {
        this->name = result.str(1);
        return result.str(2);
    }
    else
    {
        return ad;
    }
}

string people_info::set_tel(string ad)
{
    regex e("\\d{11}");
    smatch result;
    bool found = regex_search(ad, result, e);
    if (found)
    {
        this->tel = result.str(0);
        int pos = ad.find(this->tel);
        string nw_ad = ad.erase(pos, 11);
        return nw_ad;
    }
    else
    {
        return ad;
    }
}

string people_info::get_name()
{
    return this->name;
}

string people_info::get_tel()
{
    return this->tel;
}

string addr_info::cut_addr(string ad)
{
}