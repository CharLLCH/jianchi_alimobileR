/*****************************************
# File Name:filecon.h
# Author:Charlley88
# Mail:charlley88@163.com
*****************************************/

#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <algorithm>

using namespace std;

//TODO string类型字符串的split函数
vector<string> split(const string &s,const string &delim, const bool keep_empty){
    vector<string> result;
    if (delim.empty()){
        result.push_back(s);
        return result;
    }
    string::const_iterator substart = s.begin(),subend;
    while(true){
        subend = search(substart,s.end(),delim.begin(),delim.end());
        string temp(substart,subend);
        if(keep_empty || !temp.empty()){
            result.push_back(temp);
        }
        if (subend == s.end()){
            break;
        }
        substart = subend + delim.size();
    }
    return result;
}

/*
 * string => char *
 * no.1 : data()
 *  string str = "abc";
 *  char *s = str.data();
 * no.2 : c_str()
 *  string str = "abc";
 *  char *s = str.c_str();
 */

//TODO BKDRhash func
unsigned int BKDRHash(const char *str){
    unsigned int seed = 131; // 31, 131, 1313, 13131 etc..
    unsigned int hash = 0;
    while(*str){
        hash = hash * seed + (*str++);
    }
    return (hash & 0x7FFFFF); //2^23 -1
}

//TODO main func to test the funcs
const char *filename = "w_te_rand.csv";
int main(){
    //ios:: in / out / app追加 /trunc如若存在先删除 / binary二进制
    fstream in(filename,ios::in);

    string delim = ",";
    char buffer[128];
    if(! in.is_open()){
        cout<<"Error opening."<<endl;
        return -1;
    }
    vector<string> tmp;
    while(!in.eof()){
        in.getline(buffer,128);
        string temp(buffer);
        //cout<<temp<<endl;
        tmp = split(temp,delim,true);
        for (vector<string>::iterator iter = tmp.begin();iter != tmp.end(); iter++){
            string st = *iter;
            cout<<"source str: "<<st<<" the hash: "<<BKDRHash(st.c_str())<<endl;
        }
    }
    return 0;
}

