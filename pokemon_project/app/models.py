from app import db


class Pokemon(db.Model):

    """
    The Pokemon model contains below fields
    id	:	int
    name	:	text
    type_1	:	text
    type 2	:	text
    total	:	int
    hp	    :	int
    attack	:	int
    defense	:	int
    sp_atk	:	int
    sp_def	:	int
    speed	:	int
    generation	:	int
    legendary	:   boolean
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    type_1 = db.Column(db.Text)
    type_2 = db.Column(db.Text)
    total = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    sp_atk = db.Column(db.Integer)
    sp_def = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    generation = db.Column(db.Integer)
    legendary = db.Column(db.Boolean, default=False)

    def __init__(
        self,
        name,
        type_1,
        type_2,
        total,
        hp,
        attack,
        defense,
        sp_atk,
        sp_def,
        speed,
        generation,
        legendary,
    ):
        self.name = name
        self.type_1 = type_1
        self.type_2 = type_2
        self.total = total
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sp_atk = sp_atk
        self.sp_def = sp_def
        self.speed = speed
        self.generation = generation
        self.legendary = legendary

    def __repr__(self):
        return "{} - {} - {} - {} - {} - {} - {} - {} \
                - {} - {} - {} - {}".format(
            self.name,
            self.type_1,
            self.type_2,
            self.total,
            self.hp,
            self.attack,
            self.defense,
            self.sp_atk,
            self.sp_def,
            self.speed,
            self.generation,
            self.legendary,
        )
