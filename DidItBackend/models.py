from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
import logging as lg

from sqlalchemy import null

from .views import app

# Create database connection object
db = SQLAlchemy(app)
Session = sessionmaker(bind=db.engine)
session = Session()


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


class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id_1 = db.Column(db.Integer, nullable=False)
    user_id_2 = db.Column(db.Integer, nullable=False)
    request_date = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(200), nullable=False)
    last_update_date = db.Column(db.String(200), nullable=False)

    def __init__(self, user_id_1, user_id_2, request_date, status, last_update_date):
        self.user_id_1 = user_id_1
        self.user_id_2 = user_id_2
        self.request_date = request_date
        self.status = status
        self.last_update_date = last_update_date


class Support(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(200), nullable=False)

    def __init__(self, user_id, project_id, date, status):
        self.user_id = user_id
        self.project_id = project_id
        self.date = date
        self.status = status


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(200), nullable=False)
    message = db.Column(db.String(30000), nullable=False)

    def __init__(self, user_id, project_id, date, message):
        self.user_id = user_id
        self.project_id = project_id
        self.date = date
        self.message = message


class Update(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(200), nullable=False)
    old_value = db.Column(db.Integer, nullable=True)
    new_value = db.Column(db.Integer, nullable=True)
    message = db.Column(db.String(30000), nullable=True)

    def __init__(self, user_id, project_id, date, old_value, new_value, message):
        self.user_id = user_id
        self.project_id = project_id
        self.date = date
        self.message = message
        self.old_value = old_value
        self.new_value = new_value


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
    db.session.add(User("Some random dude", "Super Password", "Amazingly nice picture", "Snake", "Snake"
                        , "Damn"))
    db.session.commit()
    lg.info('Database as been update with two news users!')

    # Add Friendship
    db.session.add(Friendship(1, 2, "2020/01/01", "RECEIVED", "2020/01/01"))
    db.session.add(Friendship(3, 2, "2020/01/01", "ACCEPTED", "2020/01/01"))
    db.session.add(Friendship(1, 3, "2020/01/01", "SENDED", "2020/01/01"))
    db.session.commit()
    lg.info('Database as been update with 3 friendships!')

    # Add 3 Project by user
    db.session.add(Project(1, "Invite Eve to dinner twice a week", "Nice picture", "I would like to "
                                                                                   "go out a lot with Eve"
                           , "2019/12/01", "2020/01/30", 2, "go out to dinner", 1))
    db.session.add(Project(1, "Invite Eve to dancing twice a week", "Nice picture", "I would to go out a lot with Eve"
                           , "2019/12/01", "2020/02/24", 10, "fruits", 1))
    db.session.add(Project(1, "Invite Eve to the theater twice a week", "Nice picture", "I would to go"
                                                                                        " out a lot with Eve"
                           , "2019/12/01", "2020/12/30", 2, "go out to dinner", 1))
    db.session.add(Project(2, "Try out new fruits", "Nice picture", "I'll try to go vegan"
                           , "2019/12/01", "2019/12/30", 10, "fruits", 1))
    db.session.add(Project(2, "Get some sleep", "Nice picture", "I love to sleep so I decided to sleep"
                                                                " at least 10 hours"
                                                                " a day during one week"
                           , "2020/12/01", "2020/12/30", 70, "hours of sleep", 10))
    db.session.add(Project(2, "Find some idea for funny projects", "Nice picture", "I'm running out of funny project to"
                                                                                   "put in the database so I really"
                                                                                   "need to work hard on this one"
                           , "2019/12/01", "2019/12/30", 10, "projects", 1))
    db.session.add(Project(2, "Talk about my new boyfriend with Adam", "Nice picture", "It feel so good to talk with "
                                                                                       ", he is the best friend I good"
                                                                                       " image, I even live naked arou"
                                                                                       "nd him."
                           , "2019/12/01", "2019/12/30", 10, "projects", 1))
    db.session.add(Project(2, "Talk about my new boyfriend with Adam", "Nice picture", "It feel so good to talk with "
                                                                                       ", he is the best friend I good"
                                                                                       " image, I even live naked arou"
                                                                                       "nd him."
                           , "2019/12/01", "2019/12/30", 10, "projects", 1))
    db.session.add(Project(2, "Talk about my new boyfriend with Adam", "Nice picture", "It feel so good to talk with "
                                                                                       ", he is the best friend I good"
                                                                                       " image, I even live naked arou"
                                                                                       "nd him."
                           , "2019/12/01", "2019/12/30", 10, "projects", 1))
    db.session.add(Project(2, "Talk about my new boyfriend with Adam", "Nice picture", "It feel so good to talk with "
                                                                                       ", he is the best friend I good"
                                                                                       " image, I even live naked arou"
                                                                                       "nd him."
                           , "2019/12/01", "2019/12/30", 10, "projects", 1))
    db.session.add(Project(2, "Finish the list of projects", "Nice picture", "Coucou je suis très content poney bleu"
                           , "2019/12/01", "2019/12/30", 10, "projects", 1))
    db.session.commit()
    lg.info('Database as been update with one project!')

    # Add Supports
    db.session.add(Support(1, 4, "2020/01/01", "RECEIVED"))
    db.session.add(Support(1, 6, "2019/12/01", "SENDED"))
    db.session.add(Support(2, 1, "2019/12/12", "RECEIVED"))
    db.session.add(Support(3, 4, "2020/01/01", "SENDED"))
    db.session.add(Support(3, 5, "2020/01/01", "RECEIVED"))
    db.session.add(Support(3, 6, "2020/01/01", "SENDED"))
    db.session.commit()
    lg.info('Database as been update with 6 Supports!')

    # Add Comments
    db.session.add(Comment("1", "4", "2019/12/30", "J'adore ce projet ! Surtout n'abandonnes pas !!!! xD"))
    db.session.add(Comment("3", "4", "2019/12/30", "SsssssssSSssssssSSssssss some apple"))
    db.session.add(Comment("2", "1", "2019/12/30", "Trop bien ce projet!"))
    db.session.add(Comment("2", "1", "2019/12/31", "En faite j'aime pas"))
    db.session.commit()
    lg.info('Database as been update with 4 Comments!')

    # Add Update
    db.session.add(Update("1", "1", "2019/12/10", 0, 1, None))
    db.session.add(Update("2", "4", "2019/12/20", None, None, "I didn't do much progress but keep on trying!"))
    db.session.add(Update("1", "1", "2019/12/20", 1, 2, "Yeah another one done!"))
    db.session.add(Update("1", "2", "2019/12/20", 1, 2, "Nothing to show!"))
    db.session.commit()
    lg.info('Database as been update with 4 Updates!')
