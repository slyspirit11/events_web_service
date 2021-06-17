import random
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, create_admin
from .models import User, Role
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/sign-in', methods=['POST'])
def sign_in():
    create_admin()
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
        password = data['password']
        user = User.query.filter_by(email=email).first()
        status = "User with such email address does not exist"
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                status = "success"
                return jsonify({'data': {'status': status, 'user': user.serialize()}})
            else:
                status = "Incorrect password"
        return jsonify({'data': {'status': status, 'user': 'null'}})


@login_required
@auth.route('/sign-out', methods=['GET'])
def sign_out():
    logout_user()
    return jsonify({'status': 'success'})


@auth.route('/sign-up', methods=['POST'])
def sign_up():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']
        password_test = data['password_test']
        role1 = data['role1']
        role2 = data['role2']
        user = User.query.filter_by(email=email).first()
        status = 'User with such email address already exists'
        if user:
            return jsonify({'data': {'status': 'User with such email address already exists', 'user': 'null'}})
        elif password != password_test and len(password) == 0:
            return jsonify({'data': {'status': 'Passwords does not match', 'user': 'null'}})
        else:
            new_user = User(
                username=username,
                email=email,
                password=generate_password_hash(password, method='sha256'),
                active=True,
                first_name='',
                last_name='',
                score=random.randint(1, 50)
            )
            if role1:
                new_user.roles.append(Role.query.filter(
                    Role.name == 'Participant').first())
            elif role2 :
                new_user.roles.append(Role.query.filter(
                    Role.name == 'Organizer').first())
            else:
                raise Exception('Something wrong with roles')
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            status = 'success'
            return jsonify({'data': {'status': status, 'user': new_user.serialize()}})