
import json
from treelib import Node, Tree
import numpy as np
tree = Tree()
tree.create_node("Root", "root")  # root node
tree.create_node("Link1", "link1", parent="root", data={'related_link': ["sublink1_1", 'sublink1_2'],
                                                        'count': 50})
tree.create_node("Link2", "link2", parent="root", data={'related_link': ["sublink2_1", 'sublink2_2'],
                                                        'count': 60})
tree.create_node("Link3", "link3", parent="root", data={'related_link': ["sublink3_1", 'sublink3_2'],
                                                        'count': 70})
tree.create_node("Link4", "link4", parent="root", data={'related_link': ["sublink4_1", 'sublink4_2'],
                                                        'count': 80})
tree.create_node("Link5", "link5", parent="root", data={'related_link': ["sublink5_1", 'sublink5_2'],
                                                        'count': 40})

tree.show()
t2j = tree.to_json(with_data=True)
t2j_load = json.loads(t2j)

# print(t2j_load['Root']['children'])
try:
    print([tree[node].data for node in \
            tree.expand_tree(mode=Tree.DEPTH, filter=np.sum)])
except TypeError:
    pass


# print(tree.get_node('link5').data)
for nodes in tree.all_nodes_itr():
    dat = nodes.data
    try:
        print(dat['related_link'], dat['count'])
    except TypeError:
        print("This is ROOT!")
