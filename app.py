from flask import Flask, render_template, json, redirect, url_for
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_brogdonk'
app.config['MYSQL_PASSWORD'] = '2584' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_brogdonk'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)



# Routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/pokemon.html')
def pokemon():
    return render_template("pokemon.html")

@app.route('/pokemontypes.html')
def pokemontypes():
    return render_template("pokemontypes.html")

@app.route('/regions.html')
def regions():
    return render_template("regions.html")

@app.route('/gyms.html')
def gyms():
    return render_template("gyms.html")

@app.route('/types.html')
def stats():
    return render_template("types.html")


# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=31278, debug=False)