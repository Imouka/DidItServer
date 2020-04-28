import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
import logging as lg

from sqlalchemy import null

from .database_query.utils_project import create_project
from .views import app

# Create database connection object
db = SQLAlchemy(app)
Session = sessionmaker(bind=db.engine)
session = Session()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.String(200), nullable=True)
    description = db.Column(db.String(200), nullable=True)
    icon = db.Column(db.String(200), nullable=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    last_connection_date = db.Column(db.DateTime, nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __init__(self, login_id, first_name, last_name, description=None, icon=None, last_connection_date=None):
        self.login_id = login_id
        self.description = description
        self.icon = icon
        self.first_name = first_name
        self.last_name = last_name
        self.last_connection_date = last_connection_date


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    logo = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    project_start_date = db.Column(db.DateTime, nullable=False)
    project_end_date = db.Column(db.DateTime, nullable=False)
    objective = db.Column(db.Integer, nullable=False)
    pas = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, title, logo, description, project_start_date, project_end_date, objective,
                 pas):
        self.user_id = user_id
        self.title = title
        self.logo = logo
        self.description = description
        self.project_start_date = project_start_date
        self.project_end_date = project_end_date
        self.objective = objective
        self.pas = pas


class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id_1 = db.Column(db.Integer, nullable=False)
    user_id_2 = db.Column(db.Integer, nullable=False)
    request_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(200), nullable=False)
    last_update_date = db.Column(db.DateTime, nullable=False)

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
    date = db.Column(db.DateTime, nullable=False)
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
    date = db.Column(db.DateTime, nullable=False)
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
    date = db.Column(db.DateTime, nullable=False)
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
    db.session.add(
        User("qsdl", "Adam", "What's my name", description="Young Man that Is in Love", icon="Good looking picture"
             , last_connection_date=datetime.datetime.strptime('2000-12-30 23:20:00', '%Y-%m-%d %H:%M:%S')))
    db.session.add(
        User("qsdl", "Eve", "What's my name", description="Young Woman that Is in Love", icon="Good looking picture"
             , last_connection_date=datetime.datetime.strptime('2000-12-30 23:20:00', '%Y-%m-%d %H:%M:%S')))
    db.session.add(User("qsdl", "Snake", "Snake", description="Some random dude", icon="Amazingly nice picture"
                        , last_connection_date=datetime.datetime.strptime('2000-12-30 23:20:00', '%Y-%m-%d %H:%M:%S')))
    db.session.add(User("qsdl", "John", "Tommy", description="I am a normal user", icon="This is a picture"
                        , last_connection_date=datetime.datetime.strptime('2000-12-30 23:20:00', '%Y-%m-%d %H:%M:%S')))
    db.session.add(User("qsdl", "Tommy", "John", description="I am a normal user", icon="This is a picture"
                        , last_connection_date=datetime.datetime.strptime('2000-12-30 23:20:00', '%Y-%m-%d %H:%M:%S')))
    db.session.add(User("qsdl", "Emma", "Bort", description="I am a normal user", icon="This is a picture"
                        , last_connection_date=datetime.datetime.strptime('2000-12-30 23:20:00', '%Y-%m-%d %H:%M:%S')))
    db.session.add(User("qsdl", "Francois", "Mat", description="I am a normal user", icon="This is a picture"
                        , last_connection_date=datetime.datetime.strptime('2000-12-30 23:20:00', '%Y-%m-%d %H:%M:%S')))
    db.session.add(User("qsdl", "Lise", "Bort", description="I am a normal user", icon="This is a picture"
                        , last_connection_date=datetime.datetime.strptime('2000-12-30 23:20:00', '%Y-%m-%d %H:%M:%S')))
    db.session.add(User("qsdl", "Louise", "Mat", description="I am a normal user", icon="This is a picture"
                        , last_connection_date=datetime.datetime.strptime('2000-12-30 23:20:00', '%Y-%m-%d %H:%M:%S')))
    db.session.add(User("qsdl", "Mumu", "Juju", description="I am a normal user", icon="This is a picture"
                        , last_connection_date=datetime.datetime.strptime('2000-12-30 23:20:00', '%Y-%m-%d %H:%M:%S')))
    db.session.commit()
    lg.info('Database as been update with two news users!')

    # Add Friendship
    db.session.add(Friendship(1, 2, datetime.datetime.strptime('2019-12-01 08:08:08', '%Y-%m-%d %H:%M:%S'), "SENDED",
                              datetime.datetime.strptime('2020-01-01 08:08:08', '%Y-%m-%d %H:%M:%S')))
    db.session.add(Friendship(3, 2, datetime.datetime.strptime('2019-12-01 08:08:08', '%Y-%m-%d %H:%M:%S'), "ACCEPTED",
                              datetime.datetime.strptime('2020-01-01 08:08:08', '%Y-%m-%d %H:%M:%S')))
    db.session.add(Friendship(1, 3, datetime.datetime.strptime('2019-12-01 08:08:08', '%Y-%m-%d %H:%M:%S'), "SENDED",
                              datetime.datetime.strptime('2020-01-01 08:08:08', '%Y-%m-%d %H:%M:%S')))
    db.session.commit()
    lg.info('Database as been update with 3 friendships!')

    # Add 3 Project by user
    create_project(1, "Invite Eve to dinner twice a week", "Nice picture",
                   "I would like to go out a lot with Eve", '2019-12-01 10:10:10', '2020-12-30 10:10:10', 2, 1,
                   "1995-12-30 15:20:12")
    create_project(1, "Invite Eve to dancing twice a week", "Nice picture", "I would to go out a lot with Eve"
                   ,  '2019-12-01 10:10:10', '2020-12-30 10:10:10', 10, 1, "1995-12-30 15:20:12")
    create_project(1, "Invite Eve to the theater twice a week", "Nice picture", "I would to go out a lot with Eve"
                   ,  '2019-12-01 10:10:10', '2020-12-30 10:10:10', 2, 1, "1995-12-30 15:20:12")
    create_project(2, "Try out new fruits", "Nice picture", "I'll try to go vegan" ,  '2019-12-01 10:10:10',
                   '2020-12-30 10:10:10', 10, 1, "1995-12-30 15:20:12")
    create_project(2, "Get some sleep", "Nice picture", "I love to sleep so I decided to sleep"
                                                        " at least 10 hours"
                                                        " a day during one week"
                   ,  '2019-12-01 10:10:10', '2020-12-30 10:10:10', 70, 10, "1995-12-30 15:20:12")
    create_project(2, "Find some idea for funny projects", "Nice picture", "I'm running out of funny project to"
                                                                           "put in the database so I really"
                                                                           "need to work hard on this one"
                   , '2019-12-01 10:10:10', '2020-12-30 10:10:10', 10, 1, "1995-12-30 15:20:12")
    create_project(2, "Talk about my new boyfriend with Adam", "Nice picture", "It feel so good to talk with "
                                                                               ", he is the best friend I good"
                                                                               " image, I even live naked arou"
                                                                               "nd him."
                   ,  '2019-12-01 10:10:10', '2020-12-30 10:10:10', 10, 1, "1995-12-30 15:20:12")
    create_project(2, "Talk about my new boyfriend with Adam", "Nice picture", "It feel so good to talk with "
                                                                               ", he is the best friend I good"
                                                                               " image, I even live naked arou"
                                                                               "nd him."
                   , '2019-12-01 10:10:10', '2020-12-30 10:10:10', 10, 1, "1995-12-30 15:20:12")
    create_project(2, "Talk about my new boyfriend with Adam", "Nice picture", "It feel so good to talk with "
                                                                               ", he is the best friend I good"
                                                                               " image, I even live naked arou"
                                                                               "nd him."
                   , '2019-12-01 10:10:10',  '2020-12-30 10:10:10', 10, 1, "1995-12-30 15:20:12")
    create_project(2, "Talk about my new boyfriend with Adam", "Nice picture", "It feel so good to talk with "
                                                                               ", he is the best friend I good"
                                                                               " image, I even live naked arou"
                                                                               "nd him."
                   , '2019-12-01 10:10:10', '2020-12-30 10:10:10', 10, 1, "1995-12-30 15:20:12")
    create_project(2, "Finish the list of projects", "Nice picture", "Coucou je suis très content poney bleu"
                   ,  '2019-12-01 10:10:10', '2020-12-30 10:10:10', 10, 1, "1995-12-30 15:20:12")
    db.session.commit()
    lg.info('Database as been update with one project!')

    # Add Supports
    db.session.add(Support(1, 4, datetime.datetime.strptime('2019-12-01 07:07:07', '%Y-%m-%d %H:%M:%S'), "ACCEPTED"))
    db.session.add(Support(1, 6, datetime.datetime.strptime('2019-12-01 07:07:07', '%Y-%m-%d %H:%M:%S'), "SENDED"))
    db.session.add(Support(2, 1, datetime.datetime.strptime('2019-12-01 07:07:07', '%Y-%m-%d %H:%M:%S'), "ACCEPTED"))
    db.session.add(Support(3, 4, datetime.datetime.strptime('2019-12-01 07:07:07', '%Y-%m-%d %H:%M:%S'), "SENDED"))
    db.session.add(Support(3, 5, datetime.datetime.strptime('2019-12-01 07:07:07', '%Y-%m-%d %H:%M:%S'), "ACCEPTED"))
    db.session.add(Support(3, 6, datetime.datetime.strptime('2019-12-01 07:07:07', '%Y-%m-%d %H:%M:%S'), "SENDED"))
    db.session.commit()
    lg.info('Database as been update with 6 Supports!')

    # Add Comments
    db.session.add(Comment("1", "4", datetime.datetime.strptime('2019-12-30 07:07:07', '%Y-%m-%d %H:%M:%S'), "J'adore ce projet ! Surtout n'abandonnes pas !!!! xD"))
    db.session.add(Comment("3", "4", datetime.datetime.strptime('2019-12-30 07:07:07', '%Y-%m-%d %H:%M:%S'), "SsssssssSSssssssSSssssss some apple"))
    db.session.add(Comment("2", "1", datetime.datetime.strptime('2019-12-30 07:07:07', '%Y-%m-%d %H:%M:%S'), "Trop bien ce projet!"))
    db.session.add(Comment("2", "1", datetime.datetime.strptime('2019-12-30 07:07:07', '%Y-%m-%d %H:%M:%S'), "En faite j'aime pas"))
    db.session.commit()
    lg.info('Database as been update with 4 Comments!')

    # Add Update
    db.session.add(Update("1", "1", datetime.datetime.strptime('2019-12-20 16:19:00', '%Y-%m-%d %H:%M:%S'), 0, 1, None))
    db.session.add(Update("2", "4", datetime.datetime.strptime('2019-12-20 16:19:00', '%Y-%m-%d %H:%M:%S'), None, None, "I "
                                                                                                                  "didn't do much progress but keep on trying!"))
    db.session.add(Update("1", "1", datetime.datetime.strptime('2019-12-20 16:19:00', '%Y-%m-%d %H:%M:%S'), 1, 2, "Yeah "
                                                                                                            "another "
                                                                                                            "one "
                                                                                                            "done!"))
    db.session.add(Update("1", "2", datetime.datetime.strptime('2019-12-20 16:19:00', '%Y-%m-%d %H:%M:%S'), 1, 2, "Nothing "
                                                                                                            "to "
                                                                                                            "show!"))
    db.session.commit()
    lg.info('Database as been update with 4 Updates!')
