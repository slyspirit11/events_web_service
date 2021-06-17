from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import *

class UserEvents(db.Model):
    __tablename__ = 'user_events'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer(), db.ForeignKey('events.id'))

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

class UserTeams(db.Model):
    __tablename__ = 'user_teams'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    team_id = db.Column(db.Integer(), db.ForeignKey('teams.id', ondelete='CASCADE'))


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime(), default=func.now())
    location = db.Column(db.DateTime(), nullable=False)
    participants = db.relationship('User', secondary='user_events', back_populates='events')
    team_size = db.Column(db.Integer(), nullable=False, server_default='2')
    # teams = db.Column('Team', back_populates='event')
    # информация о кол-ве участников в команде и кол-ве самих команд
    # также информация фиксирован размер команд или нет(может навсегда его фиксированным сделать)
    def serialize(self):
        return {
            'id': self.id,
            'organizer_id': self.organizer_id,
            'description': self.description,
            'date': self.date,
            'location': self.location,
            'team_size': self.team_size
        }

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False, default='')
    score = db.Column(db.Integer(), nullable=False, server_default='1')
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')
    # created_events
    # entered_events
    # solution: if role == Organizer: events==created_evente
    # else: events==entered_events
    roles = db.relationship('Role', secondary='user_roles', back_populates='users')
    events = db.relationship('Event', secondary='user_events',  back_populates='participants')
    teams = db.relationship('Team', secondary='user_teams', back_populates='members')
    def serialize(self):
        return {
            'id': self.id,
            'active': self.active,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'score': self.score,
            'roles': [role.serialize() for role in self.roles],
            'events': [event.serialize() for event in self.events],
            'teams': [team.serialize() for team in self.teams]
        }



class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    users = db.relationship('User', secondary='user_roles', back_populates='roles')
    def serialize(self):
        return self.name


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False, server_default=f'Команда {id}')
    event_id = db.Column(db.Integer(), db.ForeignKey('events.id'), nullable=False)
    score = db.Column(db.Integer(), nullable=False, server_default='0')
    members = db.relationship('User', secondary='user_teams', back_populates='teams')
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'event_id': self.event_id,
            'score': self.score,
        }


# class Survey(db.Model):
#     __tablename__ = 'surveys'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(100), nullable=False, server_default=f'Вопрос {id}')
#     event_id = db.Column(db.Integer(), db.ForeignKey('events.id'), nullable=False)
#     score = db.column(db.Integer(), nullable=False, server_default=0)

# class Question(db.Model):
#     __tablename__ = 'questions'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(100), nullable=False, server_default=f'Команда {id}')