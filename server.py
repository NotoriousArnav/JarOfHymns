from flask import Flask, redirect, session
from datetime import datetime, timedelta
from flask import *
import pyrebase
import random
import string
import json
import os

#Initialize Firebase
with open('firebase.config.json','rt') as firebase_conf: firebase=pyrebase.initialize_app(json.load(firebase_conf))
auth = firebase.auth()
db = firebase.database()

app = Flask('JarOfHyms')
app.secret_key = ''.join([random.choice(f"{string.ascii_lowercase}{string.ascii_uppercase}{string.digits}") for x in range(24)])
app.permanent_session_lifetime = timedelta(days=2)

#Import views
try:
    import indexRouter,PlayerRouter
    print('Imported Views')
except Exception as E:
    print('Could not Import Routers', '\n', E)

#Wrappers

#User login, registration and profile management
@app.route('/login', methods=['GET','POST'])
def login_handler():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session.permanent = True
            session['user']=user
            return redirect('/')
        except:
            return 'Login Failed'
    elif request.method == 'GET':
        try:
            if session['user']:
                return redirect('/')
        except:
            return render_template('login.jinja')

@app.route('/register', methods=['GET','POST'])
def registration_handler():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm_pass']
        try:
            print('') if password==confirm else exec("raise Exception('Passwords are not the same')")
            user = auth.create_user_with_email_and_password(email, password)
            user = auth.sign_in_with_email_and_password(email, password)
            session.permanent = True
            session['user']=user
            return redirect('/')
        except:
            return 'Could not Register the user'
    elif request.method =='GET':
        try:
            if session['user']:
                return redirect('/')
        except:
            return render_template('register.jinja')

@app.get('/sessionLogout')
def logoutSession():
    session.pop('user',None)
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True, port=8080)
