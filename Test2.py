

TestDic1 = {'This': 'is', 'That':'was'}
#print(TestDic1)
delete_list = []

print(TestDic1)

for dic in TestDic1:
    if dic == 'This':
        delete_list.append(dic)

for dic in TestDic1:
    print(dic)

for deletes in delete_list:
    print(deletes)
    del TestDic1[deletes]

print(delete_list)
print(TestDic1)