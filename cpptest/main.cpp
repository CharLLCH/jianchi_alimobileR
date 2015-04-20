/*****************************************
# File Name:main.cpp
# Author:Charlley88
# Mail:charlley88@163.com
*****************************************/

#include <vector>
#include <set>
#include "sparse_vec.h"

int main(){
    std::vector< std::pair<long,double> > tmp;
    for(long i = 0; i < 10; i++){
        double x = i*2;
        tmp.push_back(std::pair<long,double>(i,x));
    }
    for (std::vector< std::pair<long,double> >::iterator iter = tmp.begin(); iter != tmp.end(); iter++){
        std::cout<<(*iter).first<<std::endl;
    }
    Sparse_Vector vc(tmp);
    vc.print_value();
    return 1;
}
