/*****************************************
# File Name:sutil.h
# Author:Charlley88
# Mail:charlley88@163.com
*****************************************/
#ifndef SUTIL_H_
#define SUTIL_H_

#include <string>
#include <vector>
#include <algorithm>

#include "sparse_vec.h"

using std::cout;
using std::endl;

static std::vector<std::string> more_split(const std::string &s, const std::string &delim, const bool keep_empty){
    std::vector<string> result;
    if (delim.empty()){
        result.push_back(s);
        return result;
    }
    std::string::const_iterator substart = s.begin(), subend;
    while (true){
        subend = search(substart,s.end(),delim.begin(),delim.end());
        std::string temp(substart.subend);
        if (keep_empty || !temp.empty()){
            result.push_back(temp);
        }
        if (subend == s.end()){
            break;
        }
        substart = subend + delim.size();
    }
    return result;
}

static std::vector<std::string> split(const std::string &s,const char delim) {

  std::vector<std::string> result;

  const char* str = s.c_str();
  do{
    const char *begin = str;

    while(*str != delim && *str)
      str++;

    result.push_back(std::string(begin, str));
  } while (0 != *str++);

  return result;
}

static long stol(const std::string& s){
  return atol(s.c_str());
}

static double stod(const std::string& s){
  return atof(s.c_str());
}

static std::pair<int,Sparse_Vector> sparse_vector_form(const std::string& s){
  std::vector<std::string> sp = split(s,' ');

  int label = stol(sp[0]);

  Sparse_Vector sv;
  std::pair<int,Sparse_Vector> tp(label,sv);

  for(int i=1;i<sp.size();i++){
    std::vector<std::string> item = split(sp[i],':');
    long indx = stol(item[0].substr(1));
    double value = stod(item[1]);
    tp.second.set_value(indx,value);
  }
  return tp;
}


#endif
