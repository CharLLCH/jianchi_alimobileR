class User_csv_Reader:
    def __init__(self, path):
        self.path = path
    
    def get_dic(self, key = [], value = []):
        if len(key) == 0:
            return {}
        dic = {}
        f = open(self.path)
        title = f.readline()[0:-1].split(',')
        attribute = {}
        for i in range(len(title)):
            attribute[title[i]] = i
        for line in f:
            line = line[:-1].split(',')
            ky = ''
            vl = ''
            for k in key:
                ky = ky + line[attribute[k]] + ','
            ky = ky[:-1]
            for v in value:
                vl = vl + line[attribute[v]] + ','
            vl = vl[:-1]
            dic[ky] = vl
        f.close()
        return dic
