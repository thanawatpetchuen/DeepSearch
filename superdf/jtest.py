import json

ll = [{'link1': {
                'related_link':
                    ['link1_1', 'link1_2'],
                'count': 50}}]
ll_j = json.dumps(ll)
ll_l = json.loads(ll_j)

# print(type(ll_l))
for item in ll_l:
    print(item['link1']['related_link'])
