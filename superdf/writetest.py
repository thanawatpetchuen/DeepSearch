import json
import pyrebase
import sys

config = {
    'apiKey': "AIzaSyARHCftDkC0xBgcvvflEnaBP24yQ99GKug",
    'authDomain': "smartvision-sv.firebaseapp.com",
    'databaseURL': "https://smartvision-sv.firebaseio.com",
    'projectId': "smartvision-sv",
    'storageBucket': "smartvision-sv.appspot.com",
    'messagingSenderId': "913555155579"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

user = auth.sign_in_with_email_and_password("paladinnot@gmail.com", "123456789")
db = firebase.database()
f = open('result/jt.json', 'r', encoding="utf-8")
ll = f.readline()
f.close()

jl = json.loads(ll)
print(jl['item_0'])
for item in jl:
    print(item)
    db.child('record').push(jl[item], user['idToken'])
# for item in jl:
#     try:
#         # for items in jl[item]['count']:
#         #     if(('.' in items) or ('/' in items) or ('$' in items) or ('#' in items) or ('[' in items) or (']' in items)):
#         #         print("Yes")
#         db.child('record').push({'link': jl[item]['link'], 'count': jl[item]['count']}, user['idToken'])
#         print(item, jl[item]['count'])
#     except:
#         print(sys.exc_info())
#
# print(type(eval(ll)))

# jsd = json.dumps(ll)
# print(type(jsd))
# print(json.loads(jsd))



# data = eval(ll)
# PrecedingText = "item"
# ListOfDictAsDict = {}
# for i in range(len(data)):
#     # db.child('record').push(data[i], user['idToken'])
#     ListOfDictAsDict[(PrecedingText + str(i)).replace('.', '').replace('/', '')] = data[i]
#
# with open('result/jt2.json', 'w', encoding="utf-8") as f:
#     jd = json.dump(ListOfDictAsDict, f)
#
# # results = db.child('record').set(json.dumps(ListOfDictAsDict), user['idToken'])
# print(ListOfDictAsDict)
