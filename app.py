from flask import Flask, render_template, json, redirect, url_for
from flask import request
import os
from db_connector.db_connector import connect_to_database, execute_query

app = Flask(__name__)

# Routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/pokemonSearchResults')
def pokemonSearch(pokedexNumber, pokemonSearchName):
    db_connection = connect_to_database()
    if pokedexNumber is None and pokemonSearchName is None:  # if both none
        return "No results found"
    elif pokedexNumber is None or pokemonSearchName is None:  # if one of them is none
        if pokedexNumber is None:
            query = "SELECT * FROM Pokemon WHERE pokemonSearchName == pokemonName"
            result = execute_query(db_connection, query).fetchall()
            if result is None:  # if still none
                return "No results found"
            render_template ("pokemonSearchResults.html", rows = result)
        else:
            query = "SELECT * FROM Pokemon WHERE pokedexNumber == pokemonId and pokemonSearchName == pokemonName"
            result = execute_query(db_connection, query).fetchall()
            if result is None:  # if still none
                return "No results found"
            render_template ("pokemonSearchResults.html", rows = pokemonSearchName)

@app.route('/pokemon.html', methods = ['POST', 'GET'])
def pokemon():
    db_connection = connect_to_database()
    regions = 'SELECT * FROM Regions'  #populate dropdowns later
    types = 'SELECT * FROM Types'   # populate dropdowns later
    if request.method == 'GET':
        if request.form.get('searchButton'):  # if search button gets pressed, treat as get
            pokedexNumber = request.form['Pokedex Search']
            pokemonSearchName = request.form['Name Search']
            return redirect(url_for('pokemonSearchResults', pokedexNumber, pokemonSearchName))  # redirect and pass values to search result page
        else:  # else it's just the initial render, add regions and types here with jinja later
            query = "SELECT * FROM Pokemon"
            result = execute_query(db_connection, query).fetchall()
            return render_template("pokemon.html", rows = result)
    
    if request.method == 'POST':  # handle add new pokemon
        pass

    # query to add new pokemon
        # query to display region dropdown
        # query to display type 1
        # query to display type 2

    # query to delete pokemon by pokedex number


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
    app.run(port=31479, debug=False)