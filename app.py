from flask import Flask, render_template, json, redirect, url_for
from flask import request
import os
from db_connector.db_connector import connect_to_database, execute_query

app = Flask(__name__)

##### Routes #####

# home page that has links to other pages 
@app.route('/')

def index():
    return render_template("index.html")

# Pokemon page that handles adding, updating, filtering, and deleting Pokemon.
@app.route('/pokemon.html', methods = ['POST', 'GET', 'DELETE', 'PUT'])
def pokemon():
    db_connection = connect_to_database()
    regionQuery = 'SELECT * FROM Regions'  # populates dropdown menus
    typeQuery = 'SELECT * FROM Types'   # populates dropdown menus
    if request.method == 'GET':
        if request.values.get('searchButton') != None:  # if search button gets pressed, filter and redisplay
            pokedexNumber = request.values.get('Pokedex Number')
            if pokedexNumber == "":  # if form is left blank, remove filter
                query = "SELECT * FROM Pokemon"
                result = execute_query(db_connection, query).fetchall()
                regions = execute_query(db_connection, regionQuery).fetchall()
                types = execute_query(db_connection, typeQuery).fetchall()
                return render_template("pokemon.html", rows = result, regions = regions, types = types)
            else:  # reload and filter results
                query = "SELECT * FROM Pokemon WHERE pokemonId = %s"
                result = execute_query(db_connection, query, pokedexNumber).fetchone()
                regions = execute_query(db_connection, regionQuery).fetchall()
                types = execute_query(db_connection, typeQuery).fetchall()
                return render_template("filteredPokemon.html", rows = result, regions = regions, types = types, number = pokedexNumber)
        else:  # else it's just the initial page render
            query = "SELECT * FROM Pokemon"
            result = execute_query(db_connection, query).fetchall()
            regions = execute_query(db_connection, regionQuery).fetchall()
            types = execute_query(db_connection, typeQuery).fetchall()
            return render_template("pokemon.html", rows = result, regions = regions, types = types)
    if request.method == 'POST' and "addButton" in request.form:  # handle add new pokemon and M:M with type
        db_connection = connect_to_database()
        newPokemonId = request.form.get("Pokedex Number")
        pokemonName = request.form.get("Pokemon Name")
        pokemonGender  = request.form.get("Pokemon Gender")
        region = request.form.get("Pokemon Region")
        type1Id = request.form.get("Type1Id")
        type2Id = request.values.get("Type2Id")
        if type2Id is None:  # check type2 dropdown was left empty
            type2Id = "None"
        if type2Id == "None":  # check if type2 dropdown None was selected
            query = "Insert into Pokemon (pokemonId, pokemonName, pokemonGender, regionId, pokemonTypeId1, pokemonTypeId2) VALUES (%s, %s, %s, %s, %s, %s)"
            data = (newPokemonId, pokemonName, pokemonGender, region, type1Id, type2Id)
        else:
            query = "Insert into Pokemon (pokemonId, pokemonName, pokemonGender, regionId, pokemonTypeId1) VALUES (%s, %s, %s, %s, %s)"
            data = (newPokemonId, pokemonName, pokemonGender, region, type1Id)
        execute_query(db_connection, query, data)  # create new row in table
        query = "INSERT into PokemonTypes (pokemonId, typeId) VALUES (%s, %s)"
        data = (newPokemonId, type1Id)
        execute_query(db_connection, query, data)  #Insert into PokemonTypes and create M:M relationship
        pokemonTypeId1 = "SELECT pokemonTypeId FROM PokemonTypes WHERE pokemonId = %s and typeId = %s"
        data = (newPokemonId, type1Id)
        pokemonTypeId1 = execute_query(db_connection, pokemonTypeId1, data).fetchone() # Select the relevant pokemonTypeId1
        query = "INSERT into PokemonTypes (pokemonId, typeId) VALUES (%s, %s)"  # query for type2 if needed
        if type2Id != "None":  # if type2 was selected
            data = (newPokemonId, type2Id)
            execute_query(db_connection, query, data)  # insert it into PokemonTypes
            pokemonTypeId2 = "SELECT pokemonTypeId FROM PokemonTypes WHERE pokemonId = %s and typeId = %s"
            data = (newPokemonId, type2Id)
            pokemonTypeId2 = execute_query(db_connection, pokemonTypeId2, data).fetchone()  #select it from the PokemonTypes table
            data = (pokemonTypeId1, pokemonTypeId2, newPokemonId)
            query = "UPDATE Pokemon SET pokemonTypeId1 = %s, pokemonTypeId2 = %s WHERE pokemonId = %s "  # update the FKs into the Pokemon Table
        else:  # no type 2 selected
            data = (pokemonTypeId1, newPokemonId)
            query = "UPDATE Pokemon SET pokemonTypeId1 = %s WHERE pokemonId = %s "  # update only pokemonTypeId1
        execute_query(db_connection, query, data)
        return redirect(url_for("pokemon"))  # reload page

    if request.method == 'POST' and "updateButton" in request.form:  # if update is selected
        db_connection = connect_to_database()
        currentPokemonId = request.form.get("Current Pokedex Number")
        newPokemonId = request.form.get("New Pokedex Number")
        pokemonName = request.form.get("Pokemon Name")
        pokemonGender  = request.form.get("Pokemon Gender")
        region = request.form.get("Pokemon Region")
        type1Id = request.form.get("Type1Id")
        type2Id = request.form.get("Type2Id")
        if type2Id is None:  # check if type2 dropdown was left empty
            type2Id = "None"
        if type2Id != "None": # if none was selected from drodown
            data = (newPokemonId, pokemonName, pokemonGender, region, type1Id, type2Id, currentPokemonId)
            query = "UPDATE Pokemon SET pokemonId = %s, pokemonName = %s, pokemonGender = %s, regionId = %s, pokemonTypeId1 = %s, pokemonTypeId2 = %s WHERE pokemonId = %s"
            execute_query(db_connection, query, data)  # update the data
        else:  # update everything but type2
            data = (newPokemonId, pokemonName, pokemonGender, region, type1Id, currentPokemonId)
            query = "UPDATE Pokemon SET pokemonId = %s, pokemonName = %s, pokemonGender = %s, regionId = %s, pokemonTypeId1 = %s WHERE pokemonId = %s"
            execute_query(db_connection, query, data)
        return redirect(url_for("pokemon"))

    if request.method == 'POST' and "deleteButton" in request.form:  # if delete was selected
        db_connection = connect_to_database()
        query = "DELETE FROM Pokemon WHERE pokemonId = %s;"
        deleteId = request.form.get("Pokedex Number")
        result = execute_query(db_connection, query, deleteId)  # delete from db
        return redirect(url_for('pokemon'))  # reload page

# Facilitates many to many relationship betweeen Pokemon and Types
@app.route('/pokemontypes.html', methods = ['GET', 'POST'])
def pokemontypes():
    db_connection = connect_to_database()
    if request.method == "GET":  # display table
        typeQuery = 'SELECT * FROM Types'
        types = execute_query(db_connection, typeQuery).fetchall()
        query = 'SELECT * FROM PokemonTypes'
        result = execute_query(db_connection, query).fetchall()
        return render_template('pokemontypes.html', rows = result, types = types)
    if request.method == "POST": # either add or delete
        if request.values.get("addNew") != None:  # if add
            pokemonId = request.values.get("Pokedex Number")
            type = request.values.get("TypeId")
            query = 'INSERT into PokemonTypes (pokemonId, typeId) VALUES (%s, %s)'
            data = (pokemonId, type)
            execute_query(db_connection, query, data)
            return redirect(url_for('pokemontypes'))
        else:  # must be delete
            pokemonTypeId = request.values.get("pokemonTypeId")
            query = 'DELETE FROM PokemonTypes WHERE pokemonTypeId = %s'
            execute_query(db_connection, query, pokemonTypeId)
            return redirect(url_for('pokemontypes'))

@app.route('/regions.html', methods = ['GET', 'POST'])
def regions():
    db_connection = connect_to_database()
    if request.method == 'GET':  # display table
        query = 'SELECT * FROM Regions'
        result = execute_query(db_connection, query).fetchall()
        return render_template('regions.html', rows = result)
    if request.method == 'POST':  # must be add region
        newType = request.values.get('Add Region')
        data = (newType,)
        query = 'INSERT into Regions (regionName) VALUES (%s)'
        execute_query(db_connection, query, data)
        return redirect(url_for('regions'))

@app.route('/gyms.html', methods = ['GET', 'POST'])
def gyms():
    db_connection = connect_to_database()
    if request.method == 'GET':  # display table and populate dropdown menus for add gym
        regionQuery = 'SELECT * FROM Regions'  # populates dropdown menus
        typeQuery = 'SELECT * FROM Types'   # populates dropdown menus
        query = 'SELECT * FROM Gyms'
        result = execute_query(db_connection, query).fetchall()
        regions = execute_query(db_connection, regionQuery).fetchall()
        types = execute_query(db_connection, typeQuery).fetchall()
        return render_template('gyms.html', rows = result, regions = regions, types = types)
    if request.method == 'POST':  # add new gym
        gymName = request.values.get('Add Gym')
        leaderName = request.values.get('Add Leader')
        regionId = request.values.get('Pokemon Region')
        typeId = request.values.get('TypeId')
        data = (gymName, leaderName, regionId, typeId)
        query = 'INSERT into Gyms (gymName, leaderName, regionId, typeId) VALUES (%s, %s, %s, %s)'
        execute_query(db_connection, query, data)
        return redirect(url_for('gyms'))

    return render_template("gyms.html")

@app.route('/types.html', methods = ['GET', 'POST'])
def types():
    db_connection = connect_to_database()
    if request.method == 'GET':  # display table
        query = 'SELECT * FROM Types'
        result = execute_query(db_connection, query).fetchall()
        return render_template('types.html', rows = result)
    if request.method == 'POST':  # add new type
        newType = request.values.get('please')
        data = (newType,)
        query = 'INSERT into Types (typeName) VALUES (%s)'
        execute_query(db_connection, query, data)
        return redirect(url_for('types'))

##### Listener #####
if __name__ == "__main__":

    #Start the app on port 31278
    app.run(port=31278, debug=True)