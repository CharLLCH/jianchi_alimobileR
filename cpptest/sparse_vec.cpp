/*****************************************
# File Name:sparse_vec.cpp
# Author:Charlley88
# Mail:charlley88@163.com
*****************************************/

#include "sparse_vec.h"

Sparse_Vector::Sparse_Vector(std::vector< std::pair<long,double> > &content):vc(),iter(vc.begin()){
    for (long i = 0; i < content.size(); i++){
        vc.insert(content[i]);
    }
}

void Sparse_Vector::print_value(){
    sp_const_iter it = vc.begin();
    std::cout<<"size "<<vc.size()<<std::endl;
    while(it != vc.end()){
        std::pair<long,double> kv = (*it);
        std::cout<<"index "<<kv.first<<"value "<<kv.second<<std::endl;
        it ++;
    }
    std::cout<<"----------------"<<std::endl;
}
