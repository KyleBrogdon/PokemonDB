from flask import Flask, render_template, json, redirect, url_for
from flask import request
import os
from db_connector.db_connector import connect_to_database, execute_query

app = Flask(__name__)

# Routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/pokemonSearchResults')  # need to make this html
def pokemonSearch(pokedexNumber, pokemonSearchName):
    db_connection = connect_to_database()
    if pokedexNumber is None and pokemonSearchName is None:  # if both none
        return "No results found"
    elif pokedexNumber is None or pokemonSearchName is None:  # if one of them is none
        if pokedexNumber is None:  # no entry for pokedex number
            query = "SELECT * FROM Pokemon WHERE pokemonSearchName == pokemonName"
            result = execute_query(db_connection, query).fetchall()
            if result is None:  # if still none
                return "No results found"
            render_template ("pokemonSearchResults.html", rows = result)
        else:  # no entry for pokemon name
            query = "SELECT * FROM Pokemon WHERE pokedexNumber == pokemonId"
            result = execute_query(db_connection, query).fetchall()
            if result is None:  # if still none
                return "No results found"
            render_template ("pokemonSearchResults.html", rows = result)
    else:  # had inputs for both
        query = "SELECT * FROM Pokemon WHERE pokedexNumber == pokemonId and pokemonSearchName == pokemonName"
        result = execute_query(db_connection, query).fetchall()
        render_template ("pokemonSearchResults.html", rows = result)

@app.route('/pokemon.html', methods = ['POST', 'GET', 'DELETE', 'PUT'])
def pokemon():
    db_connection = connect_to_database()
    regionQuery = 'SELECT * FROM Regions'  # populates dropdown menus
    typeQuery = 'SELECT * FROM Types'   # populates dropdown menus
    if request.method == 'GET':
        if request.form.get('searchButton'):  # if search button gets pressed, redirect to search
            pokedexNumber = request.form['Pokedex Search']
            pokemonSearchName = request.form['Name Search']
            return redirect(url_for('pokemonSearchResults', pokedexNumber, pokemonSearchName))  # redirect and pass values to search result page
        else:  # else it's just the initial page render
            query = "SELECT * FROM Pokemon"
            result = execute_query(db_connection, query).fetchall()
            regions = execute_query(db_connection, regionQuery).fetchall()
            types = execute_query(db_connection, typeQuery).fetchall()
            return render_template("pokemon.html", rows = result, regions = regions, types = types)
    
    if request.method == 'POST':  # handle add new pokemon and M:M with type
        db_connection = connect_to_database()
        newPokemonId = request.form.get("Pokedex Number")
        pokemonName = request.form.get("Pokemon Name")
        pokemonGender  = request.form.get("Pokemon Gender")
        region = request.form.get("Pokemon Region")
        type1Id = request.form.get("Type1Id")
        type2Id = request.form.get("Type2Id")
        query = "Insert into Pokemon (pokemonId, pokemonName, pokemonGender, regionId, pokemonTypeId1, pokemonTypeId2) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (newPokemonId, pokemonName, pokemonGender, region, type1Id, type2Id)
        execute_query(db_connection, query, data)  # create new row in table
        query = "INSERT into PokemonTypes (pokemonId, typeId) VALUES (%s, %s)"
        data = (newPokemonId, type1Id)
        print(type1Id)
        execute_query(db_connection, query, data)
        print("error is past this")
        pokemonTypeId1 = "SELECT pokemonTypeId FROM PokemonTypes WHERE pokemonId = %s and typeId = %s"
        data = (newPokemonId, type1Id)
        pokemonTypeId1 = execute_query(db_connection, pokemonTypeId1, data).fetchone()  # error is here
        print("hello world")
        print (pokemonTypeId1)
        query = "INSERT into PokemonTypes (pokemonId, typeId) VALUES (%s, %s)"
        data = (newPokemonId, type2Id)
        print(type2Id)
        execute_query(db_connection, query, data)
        pokemonTypeId2 = "SELECT pokemonTypeId FROM PokemonTypes WHERE pokemonId = %s and typeId = %s"
        data = (newPokemonId, type2Id)
        pokemonTypeId2 = execute_query(db_connection, pokemonTypeId2, data).fetchone()
        data = (pokemonTypeId1, pokemonTypeId2)
        query = "UPDATE Pokemon SET pokemonType1Id = %s, pokemonType2Id = %s"
        execute_query(db_connection, query, data)
        return redirect(url_for("pokemon"))

    if request.method == 'PUT':
        pass
    # need update pokemon here

    if request.method == 'DELETE':
        db_connection = connect_to_database()
        query = "DELETE FROM Pokemon WHERE pokemonId = %s;"
        deleteId = request.form["Pokedex Number"]
        result = execute_query(db_connection, query, deleteId)
        return redirect(url_for('pokemon'))  # reload page

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
    app.run(port=31277, debug=False)