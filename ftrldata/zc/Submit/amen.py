f = open('geo_sub.csv')
f.readline()
dic = {}

for line in f:
    dic[line] = True


f.close()
fw = open('combin.csv','w')
f = open('submit_0.75_with_rate.csv')
fw.write(f.readline())
cnt = 0
for line in f:
    if dic.has_key(line):
        cnt+=1
        fw.write(line)
fw.close()
f.close()
print cnt
