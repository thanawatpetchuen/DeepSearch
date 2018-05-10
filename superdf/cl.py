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

db.child('record').set({'sad': 'asd'}, token=user['idToken'])
