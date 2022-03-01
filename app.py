from flask import Flask, render_template, json, redirect, url_for
from flask import request
import os
from db_connector.db_connector import connect_to_database, execute_query

app = Flask(__name__)

# Routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/pokemon.html')
def pokemon():
    db_connection = connect_to_database()
    query = "SELECT * FROM Pokemon"
    result = execute_query(db_connection, query).fetchall()

    # query to add new pokemon
        # query to display gender dropdown
        # query to display region dropdown
        # query to display type 1
        # query to display type 2
    
    # query to search for a pokemon by pokedex number
    # query to search for a pokemon by name

    # query to delete pokemon by pokedex number
    return render_template("pokemon.html", rows = result)

@app.route('/pokemontypes.html')
def pokemontypes():
    # query to display pokemonTypes
        # query to display types dropdown
    
    # query to delete a pokemonTypeID relation by pokemonTypeID number

    return render_template("pokemontypes.html")

@app.route('/regions.html')
def regions():
    # query to display regions

    # query to add a region by name

    # query to show gyms by region (use regions dropdown, enter gym name)
        # query to display regions dropdown
    return render_template("regions.html")

@app.route('/gyms.html')
def gyms():
    # query to display gyms

    # query to add a gym by name

    # query to search a gym by name
    return render_template("gyms.html")

@app.route('/types.html')
def types():
    # query to display types

    # query to add a type by type name
    # query to search by pokemon type
        #query to display type drop down
    return render_template("types.html")


# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=31278, debug=False)