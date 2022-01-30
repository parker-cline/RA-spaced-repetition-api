import os
from sqlalchemy import Column, String, Integer, create_engine, Sequence, func
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
'''
setup_db(app):
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    database_name = 'local_db_name'
    default_database_path = "postgres://{}:{}@{}/{}".format(
        'postgres', 'password', 'localhost:5432', database_name)
    database_path = os.getenv('DATABASE_URL', default_database_path)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


'''
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


def db_add_data():
    User(id=1, name='kris').insert()
    Question(question='What is 2 + 2?',
             answer='4',
             category='basic_math',
             difficulty=1).insert()
    Question(question='What is 4 + 4?',
             answer='8',
             category='basic_math',
             difficulty=1).insert()
    Question(question='What is 8 * 8?',
             answer='64',
             category='basic_math',
             difficulty=2).insert()
    UserQuestion(user_id=1, question_id=1, interval=1, curr_time=1).insert()
    UserQuestion(user_id=1, question_id=2, interval=1, curr_time=1).insert()
    UserQuestion(user_id=1, question_id=3, interval=1, curr_time=1).insert()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = db.Column(String(50), nullable=False)
    userquestions = db.relationship('UserQuestion', backref='user', lazy=True)
    curr_question_id = db.Column(Integer, db.ForeignKey('question.id'))

    def __repr__(self):
        return "<User(name='%s')>" % (self.name)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(Integer, primary_key=True)
    question = db.Column(String(50), nullable=False)
    answer = db.Column(String(50), nullable=False)
    category = db.Column(String(50))
    difficulty = db.Column(Integer)
    userquestions = db.relationship('UserQuestion',
                                    backref='question',
                                    lazy=True)

    def __repr__(self):
        return "<Question(question='%s', answer='%s', category='%s', difficulty='%s')>" % (
            self.question, self.answer, self.category, self.difficulty)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class UserQuestion(db.Model):
    # tracks spaced repetition
    id = db.Column(Integer, primary_key=True)
    curr_time = db.Column(Integer)
    interval = db.Column(Integer)
    user_id = db.Column(Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(Integer,
                            db.ForeignKey('question.id'),
                            nullable=False)

    def __repr__(self):
        return "<UserQuestion(interval='%s', user_id='%s', question_id='%s')>" % (
            self.interval, self.user_id, self.question_id)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
