# Below are in built import
import json
import urllib.request

# Below are installed import
from sqlalchemy import insert
from sqlalchemy.schema import DDL

# Below are custom imports
from app.models import Pokemon
from app import db


def download_data():
    print("Fetching data from URL")
    try:
        url = "https://coralvanda.github.io/pokemon_data.json"
        response = urllib.request.urlopen(url)
        data = response.read().decode("UTF-8")

        with open("data.json", "w") as file:
            file.write(data)
        print("Data saved/refreshed into file")
    except Exception as error:
        print("Unable to fetch data. Utilizing existing data.")
        print(str(error))

    try:
        with open("data.json", "r") as f:
            parsed_data = json.loads(f.read())
    except Exception as error:
        print("Unable to read data from File")
        print(str(error))

    return parsed_data

    # print(pokemon_data, type(pokemon_data), type(pokemon_data[0]))


def process_data():
    parsed_data = download_data()
    print("Processing Data")

    column_names = (
        "id",
        "name",
        "type_1",
        "type_2",
        "total",
        "hp",
        "attack",
        "defense",
        "sp_atk",
        "sp_def",
        "speed",
        "generation",
        "legendary",
    )

    pokemon_data = []
    id_list = []
    # final_dict = dict(zip(ini_list, list(ini_dict.values())))
    for row in parsed_data:
        row_id = row["#"]
        if row_id in id_list:
            row_id = max(id_list) + 1
            row["#"] = row_id

        processed_row = dict(zip(column_names, row.values()))
        pokemon_data.append(processed_row)
        id_list.append(row_id)

    return pokemon_data


def load_data():
    pokemon_data = process_data()
    count = len(pokemon_data)
    try:
        db.create_all()

        print("Inserting Data into Database")
        db.session.execute(insert(Pokemon), pokemon_data)
        # alter_sequence = DDL(f"ALTER SEQUENCE pokemon_id_seq RESTART WITH {count+1}")
        alter_sequence = DDL(f"SELECT setval('pokemon_id_seq', {count}, true);")
        db.session.execute(alter_sequence)
        db.session.commit()
        print(f"Data Load Complete, Inserted {count} records")
    except Exception as error:
        print("error", str(error))


load_data()
