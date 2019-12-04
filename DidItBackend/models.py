from flask_sqlalchemy import SQLAlchemy

import logging as lg
from .views import app

# Create database connection object
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    icon = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    last_connection_date = db.Column(db.String(200), nullable=False)

    def __init__(self, description, password, icon, first_name, last_name, last_connection_date):
        self.description = description
        self.password = password
        self.icon = icon
        self.first_name = first_name
        self.last_name = last_name
        self.last_connection_date = last_connection_date


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    logo = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    project_start_date = db.Column(db.String(200), nullable=False)
    project_end_date = db.Column(db.String(200), nullable=False)
    objective = db.Column(db.Integer, nullable=False)
    label_objective = db.Column(db.String(200), nullable=False)
    pas = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, title, logo, description, project_start_date, project_end_date, objective,
                 label_objective, pas):
        self.user_id = user_id
        self.title = title
        self.logo = logo
        self.description = description
        self.project_start_date = project_start_date
        self.project_end_date = project_end_date
        self.objective = objective
        self.label_objective = label_objective
        self.pas = pas


def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    lg.info('Database initialized!')


def populate_db():
    # Add 2 users ("Adam","Eve")
    db.session.add(User("Young Man that Is in Love", "Super Password", "Good looking picture", "Adam", "What's my name"
                        , "yesterday"))
    db.session.add(User("Young Woman that Is in Love", "Super Password", "Good looking picture", "Eve", "What's my name"
                        , "a long time ago"))
    db.session.commit()
    lg.info('Database as been update with two news users!')

    # Add 1 Project by user
    db.session.add(Project(1, "Invite Eve to dinner twice a week", "Nice picture", "I would to go out a lot with Eve"
                           , "01/01/0000", "02/10/3000", 2, "go out to dinner", 1))
    db.session.commit()
    lg.info('Database as been update with one project!')
