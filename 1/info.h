#ifndef __INFO_H__
#define __INFO_H__

#include <cstring>
#include <string>

using namespace std;

class people_info
{
private:
    string name;
    string tel;
    addr_info addr;
public:
    people_info();
    ~people_info();
    string set_name(string ad);
    string set_tel(string ad);
    string set_addr(string ad);
    string get_name();
    string get_tel();
    string get_addr();
    void cre_json();
};

class addr_info
{
public:
    string province;
    string city;
    string county;
    string town;
    string other;
    addr_info();
    ~addr_info();
    string cut_addr(string ad);
};
#endif