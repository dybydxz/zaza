import pyrebase

configs = {
    "apiKey": "AIzaSyBjQ_v_RSOvWS2lBTyiKboGRpHbFgfyg68",
    "authDomain": "detect-a62d5.firebaseapp.com",
    "projectId": "detect-a62d5",
    "storageBucket": "detect-a62d5.appspot.com",
    "messagingSenderId": "770984764564",
    "appId": "1:770984764564:web:b8649a12d0e6a31b4f0081",
    "measurementId": "G-MG24NFN2H1"
}

firebase = pyrebase.initialize_app(configs)
storage = firebase.storage()

path_on_cloud = "imaage/foo.jpg"
path_local = "3.jpg"
storage.child(path_on_cloud).put(path_local)
