from app import db
from dataclasses import dataclass
from marshmallow import Schema, fields


@dataclass
class Pokemon(db.Model):

    """
    The Pokemon model contains below fields
    id: int
    name: text
    type_1: text
    type 2: text
    total: int
    hp: int
    attack: int
    defense: int
    sp_atk: int
    sp_def: int
    speed: int
    generation: int
    legendary: boolean
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    type_1 = db.Column(db.Text, nullable=False)
    type_2 = db.Column(db.Text)
    total = db.Column(db.Integer, nullable=False, default=0)
    hp = db.Column(db.Integer, nullable=False, default=0)
    attack = db.Column(db.Integer, nullable=False, default=0)
    defense = db.Column(db.Integer, nullable=False, default=0)
    sp_atk = db.Column(db.Integer, nullable=False, default=0)
    sp_def = db.Column(db.Integer, nullable=False, default=0)
    speed = db.Column(db.Integer, nullable=False, default=0)
    generation = db.Column(db.Integer, nullable=False, default=1)
    legendary = db.Column(db.Boolean, nullable=False, default=False)


class PostPokemonSchema(Schema):
    name = fields.String(required=True)
    type_1 = fields.String(required=True)
    type_2 = fields.String(required=False, allow_none=True, default=None)
    total = fields.Integer(required=True, default=0)
    hp = fields.Integer(required=True, default=0)
    attack = fields.Integer(required=True, default=0)
    defense = fields.Integer(required=True, default=0)
    sp_atk = fields.Integer(required=True, default=0)
    sp_def = fields.Integer(required=True, default=0)
    speed = fields.Integer(required=True, default=0)
    generation = fields.Integer(required=True, default=1)
    legendary = fields.Boolean(required=True, default=False)


post_pokemon_schema = PostPokemonSchema()
post_pokemons_schema = PostPokemonSchema(many=True)


class PokemonSchema(PostPokemonSchema):
    id = fields.Integer(required=True)


pokemon_schema = PokemonSchema()
pokemons_schema = PokemonSchema(many=True)
