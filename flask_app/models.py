from . import db

class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cat_id = db.Column(db.String(50))
    weight = db.Column(db.String(50))
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    origin = db.Column(db.String(50))
    life_span = db.Column(db.String(20))
    intelligence = db.Column(db.Integer)

    def __init__(self, cat_id, weight, name, description, origin, life_span, intelligence):
        self.cat_id = cat_id
        self.weight = weight
        self.name = name
        self.description = description
        self.origin = origin
        self.life_span = life_span
        self.intelligence = intelligence