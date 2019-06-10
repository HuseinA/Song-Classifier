import pickle, numpy
from statistics import mode
import operator

dur=20
offs=60
K=10
data=pickle.load(open('databin/normlatih'+str(offs)+str(dur)+'.p','rb'))
tes=pickle.load(open('databin/normuji'+str(offs)+str(dur)+'.p','rb'))
kelas=pickle.load(open('databin/multilabelclass0.p','rb'))

def cros_corr(train,test):
    return sum([a*b for a,b in zip(train,test)])/numpy.sqrt(sum([a**2 for a in train]) * sum([a**2 for a in test]))

def xor(train,test):
    return len([True for a,b in zip(train,test) if a is b])

def distance(train,test,mn,mx):
    a=xor(train[0],test[0])
    b=[cros_corr(train[i+1],test[i+1]) for i in range(3)]
    #print(train[4],sum([(a-mn)/(mx-mn)]),b)
    return [sum([(a-mn)/(mx-mn)]+b),train[4]]

def sync(z,n):
    for i,x in enumerate(z):
        if x[n] in kelas:
            z[i]+=[kelas[x[n]]]

def init(uji):
    temp = [xor(x[0], uji[0]) for x in data]
    mn, mx = min(temp), max(temp)
    a=[distance(x,uji,mn,mx) for x in data]

    a=[a[i]+[kelas[x[1]]] for i,x in enumerate(a) if x[1] in kelas]
    a.sort(key=lambda x:x[0])

    res={'Hip Hop':[0,0],'Pop':[0,0],'Electronic':[0,0],'Rock':[0,0],'Jazz':[0,0],'Classic':[0,0]}
    for x in a[:K]:
        if x[2] in res:
            res[x[2]][0]+=1
            res[x[2]][1]+=x[0]
        else:
            for y in x[2]:
                res[y][0]+=1
                res[y][1]+=x[0]

    test=[[v[0],k] for k,v in res.items()]
    test.sort(reverse=True)

    print([x[:2] for x in a[:K]])
    print(uji[4:],[x[1] for x in test[:3]])

    try:
        return [x[1] for x in test[:3]]#mode([x[2] for x in a[:K]])
    except:
        return min([v[1],k] for k,v in res.items() if v[0]==max(v[0] for v in res.values()))[1]

def Main():
    sync(tes,4)
    z=[(x[4:]+(init(x))) for x in tes]
    z=[x for x in z if any(y in x[2] for y in x[1])]
    print(len(z))
    print(z)

Main()
