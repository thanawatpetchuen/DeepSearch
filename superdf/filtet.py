import json
with open('result/jt.json', 'r') as f:
    p = f.readline()
jsl = json.loads(p)
jtemp = {}
print()
for key in jsl['item_0']['count'].keys():
    # print(key)
    ktemp = []
    for item in jsl:
        try:
            gg = jsl[item]['count']
            print(gg[key])
            # print(jsl[item]['link'])
            ktemp.append({'link': jsl[item]['link'], 'count': jsl[item]['count'][key]})
        except:
            pass
        # if jsl[item]['count']['computer']:
        #
    jtemp[key] = ktemp
    # print(key)
    # print(ktemp)

print(jtemp['Computer'])
with open("result/tt.json", 'w', encoding='utf-8') as f:
    json.dump(jtemp, f)
# for i in jtemp:
    # print(jtemp[i])
g = [{'id': 1, 'count': {'a': 5, 'b': 6}}, {'id': 2, 'count': {'a': 7, 'b': 1}}, {'id': 3, 'count': {'a': None, 'b': 10}}]
print(g)
temp = {}
for item in g:
    if item['count']['a']:
        print(item['id'])
        temp['a'] = item['id']
