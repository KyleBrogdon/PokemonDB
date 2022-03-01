-- Project Group 44
-- Kyle Brogdon & Rebecca Paolucci


-------------- pokemon.html -------------------
--Display Pokemon Table
SELECT * FROM Pokemon;

-- Query to add a new Pokemon:
-- Colon : used to show variables
INSERT into Pokemon (pokemonId, pokemonName, pokemonGender, regionId, pokemonTypeId1, pokemonTypeId2)
VALUES (:pokedexNumber, :pokemonName, :pokemonGender, :regionId, :type1, :type2);


-- Update a pokemon
-- Colon : used to show variables
UPDATE Pokemon SET
    pokemonId = :pokedexNumber,
    pokemonName = :pokemonName,
    pokemonGender = :pokemonGender,
    regionId = :regionId,
    pokemonTypeId1 = :type1,
    pokemonTypeId2 = :type2;

-- Search for a pokemon by pokemonId or pokemonName
-- Colon : used to show variables
SELECT * FROM Pokemon where pokemonId = :pokemonId OR pokemonName = :pokemonName;

-- Delete a pokemon by pokemonID
-- Colon : used to show variables
DELETE FROM Pokemon where pokemonId = :pokemonId;


-------------- pokemonTypes.html -------------------
-- Display pokemonTypes Table
SELECT * FROM PokemonTypes;

-- Create a new M:M relationship between Pokemon and Types (max of 2)
-- Colon : used to show variables
INSERT into PokemonTypes (pokemonId, typeID)
VALUES (:pokemonId, :type1Id);

-- Delete a M:M relationship between Pokemon and Types
-- Colon : used to show variables
DELETE FROM PokemonTypes WHERE pokemonTypeId = :pokemonTypeId

--------------types.html -------------------
-- Display Types table
SELECT * FROM Types;

-- Add a type
-- Colon : used to show variables
INSERT into Types (typeName) VALUES (:typeName)

-- Search pokemon by type -----maybe need some help with this one, have to use intersectional table for M:M relationship search
-- Colon : used to show variables
SELECT pokemonTypeId FROM PokemonTypes where typeId = :typeId as searchType
RIGHT JOIN Pokemon
ON Pokemon.pokemonTypeId1 = searchType OR Pokemon.pokemonTypeID2 = searchType

-------------- gyms.html -------------------
--Display Gyms table
SELECT * FROM Gyms;

--Add a gym
-- Colon : used to show variables
INSERT into Gyms (gymName, leaderName, regionId, typeId)
VALUES (:gymName, :leaderName, :regionId, :typeId);

--Search by gym name
SELECT * FROM Gyms WHERE gymName = :gymName;

-------------- regions.html -------------------
--Displays Regions table
SELECT * FROM Regions;

--Add a region
-- Colon : used to show variables
INSERT into Regions (regionName) VALUES (:regionName);

--Show gyms by region
-- Colon : used to show variables
SELECT * FROM Gyms WHERE regionId = :regionId;
