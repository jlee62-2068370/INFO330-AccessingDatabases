import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

con = sqlite3.connect('../pokemon.sqlite')

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue
    # Analyze the pokemon whose pokedex_number is in "arg"
    weakness = []
    strong = []
    print("Analyzing " + arg)

    # You will need to write the SQL, extract the results, and compare
    # Remember to look at those "against_NNN" column values; greater than 1
    # means the Pokemon is strong against that type, and less than 1 means
    # the Pokemon is weak against that type
    cursor = con.cursor()
    if (arg.isnumeric()):
        name_types = ("SELECT p.name, pv.type1, pv.type2 FROM pokemon p JOIN pokemon_types_view pv ON p.name = pv.name WHERE p.id = " + arg + ";")
        cursor.execute(name_types)
    elif (arg is not None):
        name_types = ('SELECT p.name, pv.type1, pv.type2 FROM pokemon p JOIN pokemon_types_view pv ON p.name = pv.name WHERE p.name = "' + arg + '";')
        cursor.execute(name_types)
    result = cursor.fetchone()


    for type in types:
        sql = ("SELECT pv.against_" + type + " " +
            "FROM pokemon_types_battle_view pv " +
            "WHERE type1name = '" + result[1] + "' AND type2name = '" + result[2] +"';")
        cursor.execute(sql)
        test = cursor.fetchone()
        if (test[0] > 1.0):
            weakness.append(type)
        elif (test[0] < 1.0):
            strong.append(type)
    print(result[0] + " (" + result[1] + " " + result[2] + ") " + "is strong against", strong ,"but is weak against", weakness)

con.close()


answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")

