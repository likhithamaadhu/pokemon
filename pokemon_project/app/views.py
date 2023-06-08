# Below are in built import
from datetime import timezone, datetime

# Below are installed import
from flask import Blueprint, request, url_for, current_app
from sqlalchemy import insert
from sqlalchemy.dialects.postgresql import insert as upsert
from sqlalchemy.exc import SQLAlchemyError

# Below are custom imports
from app import db
from app.models import (
    Pokemon,
    pokemons_schema,
    pokemon_schema,
    post_pokemons_schema,
)


pokemon_api = Blueprint("pokemon_api", __name__, url_prefix="/api/pokemons")


class PokemonException(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code


class DataNotFoundError(Exception):
    def __init__(self, message, code=404):
        self.message = message
        self.code = code


class NoContent(Exception):
    def __init__(self, message, code=204):
        self.message = message
        self.code = code


class UserError(Exception):
    def __init__(self, message):
        self.message = message


@pokemon_api.errorhandler(SQLAlchemyError)
def handle_sql_exception(e):
    current_app.logger.exception(e)

    return {"success": False, "error": str(e)}, 400


@pokemon_api.errorhandler(PokemonException)
def handle_pokemon_exception(e):
    current_app.logger.exception(e)

    return {"success": False, "error": e.message}, e.code


@pokemon_api.errorhandler(DataNotFoundError)
def handle_datanotfound_exception(e):
    current_app.logger.exception(e)

    return {"success": False, "error": e.message}, e.code


@pokemon_api.errorhandler(NoContent)
def handle_nocontent_exception(e):
    # current_app.logger.exception(e)

    return {"success": False, "error": e.message}, e.code


@pokemon_api.errorhandler(UserError)
def handle_usererror_exception(e):
    # current_app.logger.exception(e)

    return {"success": False, "error": e.message}


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
    args = request.args

    sort = args.get("sort", "id")
    order = args.get("order", "asc")
    search = args.get("search")
    search_column = args.get("search_column", "name")
    limit = args.get("limit", 10, type=int)
    page_num = args.get("page", 1, type=int)

    pokemon = Pokemon.query
    if pokemon_id:
        pokemon_info = pokemon.filter_by(id=pokemon_id).first()

        if not pokemon_info:
            raise DataNotFoundError(f"Data not found for Pokémon: {pokemon_id}")

        pokemon_info = pokemon_schema.dump(pokemon_info)

        return {
            "success": True,
            "pokemon": pokemon_info,
            "message": "Pokemon retrived sucessfully.",
        }, 200

    try:
        if order not in ("asc", "desc"):
            raise UserError("Invalid order by argument, only allowed 'asc', 'desc'")

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
            raise UserError(
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
        boolean_map = {"TRUE": True, "FALSE": False}

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
                search = search.upper()
                if search in boolean_map:
                    pokemon = pokemon.filter(Pokemon.legendary == boolean_map[search])
                else:
                    raise UserError(
                        "Legendary column only takes 'true' or 'false' as search string"
                    )
            else:
                raise PokemonException("Invalid search column")

        pokemon = pokemon.order_by(getattr(getattr(Pokemon, sort), order)())

        pokemon = pokemon.paginate(page=page_num, per_page=limit, error_out=False)

        now = datetime.now(timezone.utc)

        pokemon_list = pokemons_schema.dump(pokemon)

        if not pokemon_list:
            return {"message": "No Content found"}, 204

        if pokemon.has_next:
            next_url = url_for("pokemon_api.get_pokemon", page=pokemon.next_num)
        else:
            next_url = None

        pokemon_data = dict(
            Pokemons=pokemon_list,
            total=pokemon.total,
            current_page=pokemon.page,
            next_page=next_url,
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
    pokemon_data = request.json
    pokemon_data = pokemon_data.get("data")

    # validation of input data
    errors = post_pokemons_schema.validate(pokemon_data)
    if errors:
        return {"validationerror": errors}, 400

    if not pokemon_data:
        return {"error": "data not found"}, 404

    try:
        print("checking query")
        db.session.execute(insert(Pokemon), pokemon_data)
        db.session.commit()
        print("checking after commit")
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
        pokemon_data = [record]

    else:
        pokemon_data = request.json.get("data")

    if not pokemon_data:
        raise DataNotFoundError("Data not found")

    _pokemon_data = []
    for row in pokemon_data:
        row_id = row.get("id")
        if not row_id:  # throw error if ID not given
            raise UserError("ID not provided")

        pokemon = Pokemon.query.filter_by(id=row_id).first()

        if not pokemon:  # throw error if pokemon doesnt exist
            raise UserError("pokemon doesnt exist")
        pokemon = pokemon_schema.dump(pokemon)

        pokemon.update(row)
        _pokemon_data.append(pokemon)

    errors = pokemons_schema.validate(_pokemon_data)
    if errors:
        return {"validationerror": errors}, 400

    try:
        query = upsert(Pokemon).values(_pokemon_data)
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

    pokemon_id_list = [pokemon_id] if pokemon_id else request.json.get("data")

    if not pokemon_id_list:
        raise DataNotFoundError(f"Data not found")

    pokemon_list = Pokemon.query.filter(Pokemon.id.in_(pokemon_id_list))

    count = pokemon_list.count()

    if not count:
        raise NoContent(f"No content")

    pokemon_list.delete()
    db.session.commit()

    return {
        "success": True,
        "message": f"Deleted {count} pokemon(s)",
    }, 200
