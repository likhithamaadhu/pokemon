# Below are in built import
from datetime import timezone, datetime
from collections import OrderedDict

# Below are installed import
from flask import Blueprint, request
from sqlalchemy import insert
from sqlalchemy.dialects.postgresql import insert as upsert
from sqlalchemy.exc import SQLAlchemyError

# Below are custom imports
from app import db, app
from app.models import Pokemon

# from run import app


pokemon_api = Blueprint("pokemon_api", __name__, url_prefix="/api/pokemons")


class PokemonException(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code


@pokemon_api.errorhandler(Exception)
def handle_exception(e):
    app.logger.exception(e)
    return {"success": False, "error": str(e)}, 400


@pokemon_api.errorhandler(SQLAlchemyError)
def handle_sql_exception(e):
    app.logger.exception(e)

    return {"success": False, "error": str(e)}, 400


@pokemon_api.errorhandler(PokemonException)
def handle_exception(e):
    app.logger.exception(e)

    return {"success": False, "error": e.message}, e.code


# -----------------Pokemon APIs-----------------


@pokemon_api.route("/", methods=["GET"])
@pokemon_api.route("/<pokemon_id>", methods=["GET"])
def get_pokemon(pokemon_id=None):
    """
    This API retrieves the requested Pokemons!!
    It gets single Pokemon or multiple pokemons.

    Payload:
        id : integer

    Query Params:
        sort(str) = column to sort on.
        order(str) = desc/asc
        search(str/int) = search object.
        search_column = column to search on.
        limit(int) = number of records per page
        page(int): page number to fecth.
    """
    pokemon = Pokemon.query
    if pokemon_id:
        pokemon_info = pokemon.filter_by(id=pokemon_id).first()

        if not pokemon_info:
            raise PokemonException("Data not found", 404)

        pokemon_info = {
            "id": pokemon_info.id,
            "name": pokemon_info.name,
            "type_1": pokemon_info.type_1,
            "type_2": pokemon_info.type_2,
            "total": pokemon_info.total,
            "hp": pokemon_info.hp,
            "attack": pokemon_info.attack,
            "defense": pokemon_info.defense,
            "sp_atk": pokemon_info.sp_atk,
            "sp_def": pokemon_info.sp_def,
            "speed": pokemon_info.speed,
            "generation": pokemon_info.generation,
            "legendary": pokemon_info.legendary,
        }

        return {
            "success": True,
            "pokemon": pokemon_info,
            "message": "Pokemon retrived sucessfully.",
        }, 200

    args = request.args

    sort = args.get("sort", "id")
    order = args.get("order", "asc")
    search = args.get("search")
    search_column = args.get("search_column", "name")
    limit = args.get("limit", 10, type=int)
    page_num = args.get("page", 1, type=int)

    # print(search_column, type(search_column))
    # print(search, type(search))

    try:
        if order not in ("asc", "desc"):
            raise ValueError("Invalid order by argument, only allowed 'asc', 'desc'")

        if sort not in (
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
        ):
            raise ValueError(
                "Invalid sort argument, only allowed 'id','name'\
                             ,'type_1','type_2','total','hp','attack'\
                             ,'defense','sp_atk','sp_def','speed','generation'"
            )

        text_columns = ("name", "type_1", "type_2")
        int_columns = (
            "total",
            "hp",
            "attack",
            "defense",
            "sp_atk",
            "sp_atk",
            "speed",
            "generation",
        )
        boolean_map = {"true": True, "false": False}

        if search:
            if isinstance(search, str) and search_column in int_columns:
                try:
                    search = int(search)
                except:
                    raise PokemonException("Cant search a string in int type columns")

            if search_column in int_columns:
                pokemon = pokemon.filter(getattr(Pokemon, search_column) == search)
            elif search_column in text_columns:
                pokemon = pokemon.filter(
                    getattr(Pokemon, search_column).ilike(f"%{search}%")
                )
            elif search_column == "legendary":
                if search in boolean_map:
                    pokemon = pokemon.filter(Pokemon.legendary == boolean_map[search])
                else:
                    raise PokemonException(
                        "Legendary column only takes 'true' or 'false' as search string"
                    )
            else:
                raise PokemonException("Invalid search column")

        pokemon = pokemon.order_by(getattr(getattr(Pokemon, sort), order)())

        pokemon = pokemon.paginate(page=page_num, per_page=limit, error_out=False)

        now = datetime.now(timezone.utc)

        pokemon_list = [
            {
                "id": i.id,
                "name": i.name,
                "type_1": i.type_1,
                "type_2": i.type_2,
                "total": i.total,
                "hp": i.hp,
                "attack": i.attack,
                "defense": i.defense,
                "sp_atk": i.sp_atk,
                "sp_def": i.sp_def,
                "speed": i.speed,
                "generation": i.generation,
                "legendary": i.legendary,
            }
            for i in pokemon.items
        ]
        if not pokemon_list:
            return {"msg": "No Content found"}, 204

        pokemon_data = dict(
            Pokemons=pokemon_list,
            total=pokemon.total,
            current_page=pokemon.page,
            per_page=pokemon.per_page,
            timestamp=now,
        )

    except Exception as error:
        return {"error": str(error)}, 404

    return (
        {
            "success": True,
            "task_list": pokemon_data,
            "message": "pokemons retrieved sucessfully.",
        },
        200,
    )


@pokemon_api.route("/", methods=["POST"])
def insert_pokemon():
    """
    This API creates Pokemons. when using this api then pass all values.

    Payload: {
        name(str): name of pokemon
        type_1(str): type_1
        type_2(str): type_2
        total(int): total value
        hp(int): hp value
        attack(int): attack value
        defense(int): defense value
        sp_atk(int): special attack value
        sp_def(int): special defense value
        speed(int): speed of pokemnon
        generation(int): generation of pokemon
        legendary(bool): true/false
        }
    """
    pokemon_info = request.json
    pokemon_info = pokemon_info.get("data")

    if not pokemon_info:
        return {"error": "data not found"}, 404

    try:
        db.session.execute(insert(Pokemon), pokemon_info)
        db.session.commit()
    except Exception as error:
        return {"error": str(error)}, 404

    now = datetime.now(timezone.utc)

    return {
        "success": True,
        "timestamp": now,
        "message": "Pokemon(s) added sucessfully.",
    }, 201


@pokemon_api.route("/", methods=["PUT"])
@pokemon_api.route("/<pokemon_id>", methods=["PUT"])
def update_pokemon(pokemon_id=None):
    """
    This API updates Pokemon.
    And if the Pokemon is not present in the database,
    then it inserts the data into databse.

    Payload:{
        id(int): id of pokemon
        name(str): name of pokemon
        type_1(str): type_1
        type_2(str): type_2
        total(int): total value
        hp(int): hp value
        attack(int): attack value
        defense(int): defense value
        sp_atk(int): special attack value
        sp_def(int): special defense value
        speed(int): speed of pokemnon
        generation(int): generation of pokemon
        legendary(bool): true/false
        }
    """

    if pokemon_id:
        record = request.json
        record["id"] = pokemon_id
        # print(record,type(record))
        pokemon_data = [record]
        # print(pokemon_data)

    else:
        pokemon_data = request.json.get("data")

    if not pokemon_data:
        return {"error": "Data not found"}, 404

    try:
        query = upsert(Pokemon).values(pokemon_data)
        # print(str(query))
        query = query.on_conflict_do_update(
            index_elements=[Pokemon.id],
            set_=dict(
                name=query.excluded.name,
                type_1=query.excluded.type_1,
                type_2=query.excluded.type_2,
                total=query.excluded.total,
                hp=query.excluded.hp,
                attack=query.excluded.attack,
                defense=query.excluded.defense,
                sp_atk=query.excluded.sp_atk,
                sp_def=query.excluded.sp_def,
                speed=query.excluded.speed,
                generation=query.excluded.generation,
                legendary=query.excluded.legendary,
            ),
        )

        # print(str(query))

        db.session.execute(query)
        db.session.commit()
    except Exception as error:
        return {"error": str(error)}, 404

    return {
        "success": True,
        "message": "Pokemon(s) updated sucessfully.",
    }, 200


@pokemon_api.route("/", methods=["DELETE"])
@pokemon_api.route("/<pokemon_id>", methods=["DELETE"])
def delete_pokemon(pokemon_id=None):
    """
    This API deletes the pokemons.
    It can delete single or multiple pokemons.

    Payload:
        for single:
            id(int): id of pokemon
         for multiple:
            [ids]
    """

    if pokemon_id:
        pokemon_info = Pokemon.query.filter_by(id=pokemon_id).first()

        if not pokemon_info:
            return {"error": "Pokemon not found"}, 404

        db.session.delete(pokemon_info)
        db.session.commit()

        return {"success": True, "message": "Pokemon deleted successfully"}, 200

    pokemon_id_list = request.json.get("data")

    if not pokemon_id_list:
        return {"error": "Data not found"}, 404

    pokemon_list = Pokemon.query.filter(Pokemon.id.in_(pokemon_id_list))

    count = pokemon_list.count()

    if not count:
        return {"Error": "No content"}, 204

    pokemon_list.delete()
    db.session.commit()

    return {
        "success": True,
        "message": f"Deleted {count} pokemons",
    }, 200
