"""Transit Alert"""
# from jinja2 import StrictUndefined

# from flask import Flask, render_template, request, flash, redirect, session
# from flask_debugtoolbar import DebugToolbarExtension

from firebase import firebase

# import request

# app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
# app.secret_key = "123"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
# app.jinja_env.undefined = StrictUndefined

# Setting up my firebase connection 
# firebase = firebase.FirebaseApplication("https://popping-torch-2216.firebaseio.com/", None)

# result = firebase.get('/', None)
# print "my firebase results: ",result



transit_firebase = firebase.FirebaseApplication("https://publicdata-transit.firebaseio.com", None)

result = transit_firebase.get('/', None)
print "results: ",result
print "values: ", result.val()