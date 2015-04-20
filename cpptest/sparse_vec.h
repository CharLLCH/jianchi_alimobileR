#ifndef SPARSE_VEC_H_
#define SPARSE_VEC_H_

#include <iostream>
#include <map>
#include <vector>
#include <tr1/unordered_map>
#include <tr1/unordered_set>

const double SMALL = 1e-3;
const double BIG = 1e-3;

//类似hash_map，支持key类型
typedef std::tr1::unordered_map<long,double> sp_type;
typedef std::tr1::unordered_map<long,double>::iterator sp_iter;
typedef std::tr1::unordered_map<long,double>::const_iterator sp_const_iter;


//类
class Sparse_Vector{
    private:
        //unordered_map 和 iterator
        sp_type vc;
        sp_iter iter;

    public:
        Sparse_Vector(std::vector< std::pair<long,double> > &content);
        //创建一个空的map，迭代器取开始
        Sparse_Vector(void):vc(),iter(vc.begin()){}
        Sparse_Vector(const Sparse_Vector &sp):vc(sp.vc),iter(vc.begin()){}

        void print_value();
        
        inline void set_value(long index, double value){
            vc[index] = value;
        }
};

#endif
