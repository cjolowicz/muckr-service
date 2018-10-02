import flask_sqlalchemy
import flask_restless

def init_app(app):
    db = flask_sqlalchemy.SQLAlchemy(app)

    class Person(db.Model):
        id         = db.Column(db.Integer, primary_key=True)
        name       = db.Column(db.Unicode, unique=True)
        birth_date = db.Column(db.Date)

    class Computer(db.Model):
        id            = db.Column(db.Integer, primary_key=True)
        name          = db.Column(db.Unicode, unique=True)
        vendor        = db.Column(db.Unicode)
        purchase_time = db.Column(db.DateTime)
        owner_id      = db.Column(db.Integer,
                                  db.ForeignKey('person.id'))
        owner = db.relationship(
            'Person',
            backref=db.backref('computers', lazy='dynamic'))

    db.create_all()

    manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

    # Create API endpoints, which will be available at /api/<tablename> by
    # default.
    manager.create_api(Person, methods=['GET', 'POST', 'DELETE'])
    manager.create_api(Computer, methods=['GET'])
