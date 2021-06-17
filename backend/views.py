from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from .models import User, Role, Event
from . import db


views = Blueprint('views', __name__)

weather = {
    "data":
    [    
        {
            "day": "1/6/2019",
            "temperature": "23",
            "windspeed": "16",
            "event": "Sunny"
        },
        {
            "day": "1/6/2020",
            "temperature": "24",
            "windspeed": "17",
            "event": "Windy"
        },
        {
            "day": "1/6/2021",
            "temperature": "25",
            "windspeed": "18",
            "event": "Rainy"
        },
        {
            "day": "1/6/2022",
            "temperature": "26",
            "windspeed": "199",
            "event": "Hurricane"
        }
    ]
}


@views.route('/')
def home():
    return render_template('index.html', user=current_user)


@views.route('/weatherReport/', methods=['GET'])
def weather_report():
    global weather
    return jsonify(weather)

@views.route('/create-event', methods=['POST'])
def create_event():
    if request.method == 'POST':
        data = request.get_json()
        organizer_id = data['user_id']
        description = data['description']
        date = data['date']
        location = data['location']
        team_size = data['team_size']
        new_event = Event(
            organizer_id=organizer_id,
            description=description,
            date=date,
            location=location,
            team_size=team_size,
        )
        db.session.add(new_event)
        organizer = User.query.filter_by(id=organizer_id).first()
        organizer.events.append(new_event)
        db.session.commit()
        
@views.route('/enter-event', methods=['POST'])
def create_team():
    if request.method == 'POST':
        data = request.get_json()
        participant_id = data['user_id']
        event_id = data['event_id']
        participant = User.query.filter_by(id=participant_id).first()
        event = Event.query.filder_by(id=event_id).first()
        participant.events.append(event)
        event.participants.append(participant)
        # MAGIC IS HERE
        # 1.в функцию передаются текущие участники события
        # 2.создаётся k команд
        # юзеры распределяются по командам
        db.session.commit()

@views.route('/get-event-list', methods=['POST'])
def get_event_list():
    if request.method == 'GET':
        events = Event.query.all()
        return jsonify({'data':[event.serialize() for event in events]})

# @views.route('/get-event-item', methods=['POST'])
# def create_team():
#     if request.method == 'GET':

