'''
class Rule: generate transform rules
class Encoder: transform file
'''

import csv

def split_time(idir, odir):
    print 'split time:'
    fi = open(idir)
    fo = open(odir, 'w')

    reader = csv.reader(fi)
    writer = csv.writer(fo)

    title = reader.next()
    title.append('hour')
    writer.writerow(title)

    cnt = 0
    for line in reader:
        cnt += 1
        if cnt % 1000000 == 0:
            print ' complete', cnt, 'lines'
        time, hour = line[-1].split(' ')
        line[-1] = time
        line.append(hour)
        writer.writerow(line)
    
    fi.close()
    fo.close()
    print 'split time succeed!\n'

class Maker:
    def __init_dic__(self, attribute):
        self.dic = {}
        for att in attribute:
            self.dic[att] = {}
    def __make_rule__(self, idir, attribute):
        print ' make rules:'
        f = open(idir)
        reader = csv.reader(f)
        
        title = reader.next()
        att = {}
        for i in range(len(title)):
            att[title[i]] = i
            
        cnt = 0
        for line in reader:
            cnt += 1
            if cnt % 1000000 == 0:
                print '  complete', cnt, 'lines'
            for a in attribute:
                self.dic[a][line[att[a]]] = True

        print '  complete', cnt, 'lines'
        print ' make rules succeed!\n'
        self.__write_size__()
        f.close()
        
    def make_transform_rules(self, idir, odir, attribute):
        print 'make_transform rules:',idir
        self.__init_dic__(attribute)
        self.__make_rule__(idir, attribute)
        for att in attribute:
            self.__write_rule__(odir, att)
        print 'make transform rules succeed!\n'

    def __write_rule__(self, odir, att):
        print ' write rule', att
        fo = open(odir+att, 'w')
        writer = csv.writer(fo)
        writer.writerow([att])
        att_keys = self.dic[att].keys()
        att_keys.sort()
        for key in att_keys:
            writer.writerow([key])
        fo.close()
        print ' write rule succeed!\n'
    def __write_size__(self):
        f = open('./mylibs/size.py','w')
        for key in self.dic:
            f.write(key+' = '+str(len(self.dic[key]))+'\n')

class Decoder:
    def __init_dic__(self, attribute):
        self.dic = {}
        for att in attribute:
            self.dic[att] = []
    def __load_rule__(self, idir, att):
        print '  load rule', att
        fi = open(idir + att)
        reader = csv.reader(fi)
        
        if reader.next()[0] == att:
            for [value] in reader:
                self.dic[att].append(value)
        fi.close()
        print '  load rule succeed!\n'
    def __init__(self, idir, attribute):
        print ' init Decoder:'
        self.__init_dic__(attribute)
        for att in attribute:
            self.__load_rule__(idir, att)
        print ' init Decoder succeed!\n'
    
    def decode(self, att, n):
        if self.dic.has_key(att):
            return self.dic[att][int(n)]
        else:
            return n

    def decode_file(self, idir, odir):
        print 'decode file:',idir
        fi = open(idir)
        fo = open(odir,'w')

        reader = csv.reader(fi)
        writer = csv.writer(fo)
        
        title = reader.next()
        writer.writerow(title)
        
        cnt = 0
        for line in reader:
            cnt += 1
            if cnt % 1000000 == 0:
                print ' complete',cnt,'lines'
            for i in range(len(line)):
                line[i] = self.decode(title[i], line[i])
            writer.writerow(line)

        print ' complete',cnt,'lines'
        fi.close()
        fo.close()
        print 'decode file succeed!\n'

#Encoder : use for encode and decode
class Encoder:
    def __init_dic__(self, attribute):
        self.dic = {}
        for att in attribute:
            self.dic[att] = {}
    def __load_rule__(self, idir, att):
        print '  load rule', att
        fi = open(idir + att)
        reader = csv.reader(fi)
        
        i = 0
        if reader.next()[0] == att:
            for [value] in reader:
                self.dic[att][value] = i
                i += 1
        fi.close()
        print '  load rule succeed!\n'
    def __init__(self, idir, attribute):
        print ' init Encoder:'
        self.__init_dic__(attribute)
        for att in attribute:
            self.__load_rule__(idir, att)
        print ' init Encoder succeed!\n'
    
    def encode(self, att, key):
        if self.dic.has_key(att):
            return str(self.dic[att][key])
        else:
            return key

    def encode_file(self, idir, odir):
        print 'encode file:',idir
        fi = open(idir)
        fo = open(odir, 'w')

        reader = csv.reader(fi)
        writer = csv.writer(fo)
        
        title = reader.next()
        writer.writerow(title)
        
        cnt = 0
        for line in reader:
            cnt += 1
            if cnt % 1000000 == 0:
                print ' complete',cnt,'lines'
            for i in range(len(line)):
                line[i] = self.encode(title[i], line[i])
            writer.writerow(line)

        print ' complete',cnt,'lines'
        fi.close()
        fo.close()
        print 'encode file succeed!\n'
