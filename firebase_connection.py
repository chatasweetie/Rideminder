"""Connects to my firebase jazz"""

from firebase import firebase

firebase = firebase.FirebaseApplication("https://popping-torch-2216.firebaseio.com/", None)

result = firebase.get("/", None)

