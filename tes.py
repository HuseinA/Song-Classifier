import pickle, numpy
from statistics import mode
import operator

dur=[10,20,30]
offs=[30,60,90,120]
K=[5,10,15]

def cros_corr(train,test):
    return sum([a*b for a,b in zip(train,test)])

def xor(train,test):
    return len([True for a,b in zip(train,test) if a is b])

def distance(train,test):
    a=xor(train[0],test[0])
    b=[cros_corr(train[i+1],test[i+1]) for i in range(3)]
    return [a]+b

def minmax(mnmx):
    temp=numpy.transpose(mnmx)
    mn=[min(x) for x in temp]
    mx=[max(x) for x in temp]
    form=lambda a,i:(a-mn[i])/(mx[i]-mn[i])
    mnmx=[[form(b[a],a) for a in range(4)] for b in mnmx]
    return mnmx


def init(uji,data,K,kelas):
    a=[distance(x,uji) for x in data]
    a=minmax(a)
    a=[[4-sum(x),y[4]] for x,y in zip(a,data)]

    a=[a[i]+[kelas[x[1]]] for i,x in enumerate(a) if x[1] in kelas]
    a.sort(key=lambda x:x[0])
    res={'Hip Hop':[0,0],'Pop':[0,0],'Electronic':[0,0],'Rock':[0,0],'Jazz':[0,0],'Classic':[0,0]}
    for x in a[:K]:
        for y in x[2]:
            res[y][0]+=1
            res[y][1]+=x[0]

    test=[[v[0],k] for k,v in res.items()]
    test.sort(reverse=True)
    return [x[1] for x in test[:3]]

def Main(dur,offs,K):
    data=pickle.load(open('databin/latih'+str(offs)+str(dur)+'.p','rb'))
    tes=pickle.load(open('databin/uji'+str(offs)+str(dur)+'.p','rb'))
    kelas=pickle.load(open('databin/multilabelclasstes.p','rb'))
    z=[tes[i]+[kelas[x[4]]] for i,x in enumerate(tes) if x[4] in kelas]
    z=[(x[4:]+[init(x,data,K,kelas)]) for x in z]
    pickle.dump(z,open('databin/hasil'+str(offs)+str(dur)+str(K)+'.p','wb'))
    for x in z:
        print(x)
    for x in z:
        print(x[2])
    z=[x for x in z if any(y in x[2] for y in x[1])]
    print(len(z))
    print(z)

for x in dur:
    for y in offs:
        for z in K:
            print('duration:'+str(x)+'\toffset:'+str(y)+'\tK:'+str(z))
            Main(x,y,z)
            print('DONE')