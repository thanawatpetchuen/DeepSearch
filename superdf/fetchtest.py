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

# Push  #########################
# data = [{'link': "wwww.google.com", "count": 5}, {'link': "wwww.facebook.com", "count": 2}, {'link': "wwww.instagram.com", "count": 10}]
#
# for item in data:
#     record = db.child('record/computer').push(item, user['idToken'])
#################################


record = db.child('record').order_by_child('count/computer').get()
print(record.val())
# sr = {}
# reval = record.val()
# for item in reval:
#     try:
#
#         print(reval[item]['count']['computer'])
#         sr[reval[item]['count']['computer']] = []
#         # sr[reval[item]['count']['computer']].append(reval[item]['link'])
#     except:
#         pass
#
# for item in reval:
#     try:
#
#         # print(reval[item]['count']['computer'])
#         # sr[reval[item]['count']['computer']] = []
#         sr[reval[item]['count']['computer']].append(reval[item]['link'])
#     except:
#         pass
# print(sr)
