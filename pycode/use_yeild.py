#coding=utf-8

from test_yeild import get_raw_data

def print_raw_data():
    row_data = get_raw_data()
    for x in row_data:
        print x

if __name__ == "__main__":
    print_raw_data()
