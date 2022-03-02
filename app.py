from flask import Flask, render_template, json, redirect, url_for
from flask import request
import os
from db_connector.db_connector import connect_to_database, execute_query

app = Flask(__name__)

# Routes
@app.route('/')
def index():
    return render_template("index.html")


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
        type2Id = request.form.get("Type2Id")
        print (type2Id == "None")
        if type2Id == "None":
            query = "Insert into Pokemon (pokemonId, pokemonName, pokemonGender, regionId, pokemonTypeId1, pokemonTypeId2) VALUES (%s, %s, %s, %s, %s, %s)"
            data = (newPokemonId, pokemonName, pokemonGender, region, type1Id, type2Id)
        else:
            query = "Insert into Pokemon (pokemonId, pokemonName, pokemonGender, regionId, pokemonTypeId1) VALUES (%s, %s, %s, %s, %s)"
            data = (newPokemonId, pokemonName, pokemonGender, region, type1Id)
        execute_query(db_connection, query, data)  # create new row in table
        query = "INSERT into PokemonTypes (pokemonId, typeId) VALUES (%s, %s)"
        data = (newPokemonId, type1Id)
        execute_query(db_connection, query, data)
        pokemonTypeId1 = "SELECT pokemonTypeId FROM PokemonTypes WHERE pokemonId = %s and typeId = %s"
        data = (newPokemonId, type1Id)
        pokemonTypeId1 = execute_query(db_connection, pokemonTypeId1, data).fetchone() 
        query = "INSERT into PokemonTypes (pokemonId, typeId) VALUES (%s, %s)"
        if type2Id != "None":
            data = (newPokemonId, type2Id)
            execute_query(db_connection, query, data)
            pokemonTypeId2 = "SELECT pokemonTypeId FROM PokemonTypes WHERE pokemonId = %s and typeId = %s"
            data = (newPokemonId, type2Id)
            pokemonTypeId2 = execute_query(db_connection, pokemonTypeId2, data).fetchone()
            data = (pokemonTypeId1, pokemonTypeId2, newPokemonId)
        if type2Id != "None":
            query = "UPDATE Pokemon SET pokemonTypeId1 = %s, pokemonTypeId2 = %s WHERE pokemonId = %s "
        else:
            data = (pokemonTypeId1, newPokemonId)
            query = "UPDATE Pokemon SET pokemonTypeId1 = %s WHERE pokemonId = %s "
        execute_query(db_connection, query, data)
        return redirect(url_for("pokemon"))

    if request.method == 'POST' and "updateButton" in request.form:
        db_connection = connect_to_database()
        currentPokemonId = request.form.get("Current Pokedex Number")
        newPokemonId = request.form.get("New Pokedex Number")
        pokemonName = request.form.get("Pokemon Name")
        pokemonGender  = request.form.get("Pokemon Gender")
        region = request.form.get("Pokemon Region")
        type1Id = request.form.get("Type1Id")
        type2Id = request.form.get("Type2Id")
        print(type2Id)
        if type2Id != "None":
            data = (newPokemonId, pokemonName, pokemonGender, region, type1Id, type2Id, currentPokemonId)
            query = "UPDATE Pokemon SET pokemonId = %s, pokemonName = %s, pokemonGender = %s, regionId = %s, pokemonTypeId1 = %s, pokemonTypeId2 = %s WHERE pokemonId = %s"
            execute_query(db_connection, query, data)
        else:
            data = (newPokemonId, pokemonName, pokemonGender, region, type1Id, currentPokemonId)
            query = "UPDATE Pokemon SET pokemonId = %s, pokemonName = %s, pokemonGender = %s, regionId = %s, pokemonTypeId1 = %s WHERE pokemonId = %s"
            execute_query(db_connection, query, data)
        return redirect(url_for("pokemon"))

    if request.method == 'POST' and "deleteButton" in request.form:
        db_connection = connect_to_database()
        query = "DELETE FROM Pokemon WHERE pokemonId = %s;"
        deleteId = request.form.get("Pokedex Number")
        result = execute_query(db_connection, query, deleteId)
        return redirect(url_for('pokemon'))  # reload page


@app.route('/pokemontypes.html', methods = ['GET', 'POST'])
def pokemontypes():
    db_connection = connect_to_database()
    if request.method == "GET":
        typeQuery = 'SELECT * FROM Types'
        types = execute_query(db_connection, typeQuery).fetchall()
        query = 'SELECT * FROM PokemonTypes'
        result = execute_query(db_connection, query).fetchall()
        return render_template('pokemontypes.html', rows = result, types = types)
    if request.method == "POST":
        if request.values.get("addNew") != None:
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

@app.route('/regions.html')
def regions():
    # query to display regions

    # query to add a region by name
    return render_template("regions.html")

@app.route('/gyms.html', methods = ['GET', 'POST'])
def gyms():
    db_connection = connect_to_database()
    if request.method == 'GET':
        regionQuery = 'SELECT * FROM Regions'  # populates dropdown menus
        typeQuery = 'SELECT * FROM Types'   # populates dropdown menus
        query = 'SELECT * FROM Gyms'
        result = execute_query(db_connection, query).fetchall()
        regions = execute_query(db_connection, regionQuery).fetchall()
        types = execute_query(db_connection, typeQuery).fetchall()
        return render_template('gyms.html', rows = result, regions = regions, types = types)
    if request.method == 'POST':
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
    if request.method == 'GET':
        query = 'SELECT * FROM Types'
        result = execute_query(db_connection, query).fetchall()
        return render_template('types.html', rows = result)
    if request.method == 'POST':
        print(request.form.get('please'))
        newType = request.values.get('please')
        print(newType)
        data = (newType,)
        query = 'INSERT into Types (typeName) VALUES (%s)'
        execute_query(db_connection, query, data)
        return redirect(url_for('types'))
    # query to add a type by type name

    #return render_template("types.html")


# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=31277, debug=True)