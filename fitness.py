import datetime
import os

from jinja2.filters import do_map
from sqlalchemy import select
from flask import Flask, request, render_template, session, redirect
from functools import wraps

from models import Review, Service
from utils import SQLiteDatabase, clac_slots

import models
import database

from send_mail import add, send_mail

#import sqlite3
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

#
# app = Flask(__name__, template_folder='templates')
# # app.secret_key = "123456789"
# app.secret_key = os.environ.get("SESSION_SECRET_KEY")

app = Flask(__name__)
# Check Configuration section for more details
SESSION_TYPE = 'FileSystem'
app.config.from_object(__name__)
Session(app)


# def login_required(func):
#     @wraps(func)
#     def wr1(*args, **kwargs):
#         if session.get('user') is None:
#             return redirect('/login')
#         result = func(*args, **kwargs)
#         return result
#     return wr1


def login_required(func):
    @wraps(func)
    def wr1(*args, **kwargs):
        if 'user' in session:
            return func(*args, **kwargs)
        else:
            redirect('/login')
    return wr1
############################


@app.get('/')
def index():
    # from send_mail import add
    # add.delay(1, 2)
    #send_mail.delay("irajhdhj@gmail.com", "ira", "some text")
    #return render_template('index.html')
    return redirect('/fitness_center')


@app.get('/registration')  # відображає форму
def user_register_invitation():
    return render_template('registration.html')


def check_credentials(username, password): # перевіряє залогінився чи ні
    database.init_db()
    user = database.db_session.query(models.User).filter_by(
        login=username, password=password).first()

    # smth = database.db_session.execute(select(models.User).where(models.User.login==username, models.User.password=="ygjgh")).first()[0]

    # user = database.db_session.query(models.User).filter_by().all()
    # user = database.db_session.query(models.User).filter_by(login=username, password=password).first()

    # select(address_table.c.email_address).select_from(user_table)
    # .join(address_table, user_table.c.id == address_table.c.user_id)

    # зробити як user легше,якщо одна таблиця
    # зробити як smth легше,якщо складне багато джоінів

    return user


@app.post('/registration') # запис в базу даних все готово під алхімію
def post_register():
    form_data = request.form
    database.init_db()
    user1 = models.User(login=form_data["login"], password=form_data['password'],
                        birth_date=datetime.datetime.strptime(form_data["birth_date"], "%Y-%m-%d"),
                        phone=form_data['phone'], funds=form_data['funds'], email=form_data['email'])
    database.db_session.add(user1)
    database.db_session.commit()

    return redirect('/fitness_center')


@app.get('/login') # відображає форму
def user_login_form():
    user = session.get("user")
    # if user:
    #     return redirect('/user')# redirect будує якийсь обʼєкт з відповіддю(як return)
    return render_template('user_login.html')


@app.post('/login') # готово під алхімію
def user_login():
    login = request.form['login']
    password = request.form['password']
    user = check_credentials(login, password)
    if user is not None:
        session['user'] = {'id': user.id, 'login': user.login}
        return redirect('/user')
    else: # якщо не вдалася авторизація
        user_id = session.get('user', None)
        if user_id:
            return redirect('/user')
        return render_template('user_login.html')


@app.get('/logout')
@login_required
def logout():
    session.pop('user')
    return redirect('/login')


@app.get('/user/<user_id>')
@login_required
def get_user_info(user_id):
    #user = session.get("user_id")
    database.init_db()
    user_data = database.db_session.query(models.User.login, models.User.birth_date,
                                     models.User.phone).filter_by(
        id=user_id).first()
        #id=session.get('user_id')).first()
    if not user_data:
        return "User not found", 404
    return render_template('user_info.html', user_info=user_data)


@app.post('/user/<user_id>')# алхімія, але не впевнена,що вірно все
@login_required
def add_user_info(user_id):  # де використати user_id,можливо взагалі не трба його
    form_data = request.form
    database.init_db()
    new_data_user = models.User(login=form_data["login"], password=form_data['password'],
                                birth_date=datetime.datetime.strptime(form_data["birth_date"], "%y-%m-%d"),
                                phone=form_data['phone'])
    database.db_session.add(new_data_user)
    database.db_session.commit()
    return render_template('user_info.html', user_info=new_data_user) # user=new_data_user?????????


# @app.get('/funds')# вирішили не треба
# @login_required
# def user_deposit_info():
#     database.init_db()
#     data = database.db_session.query(models.User.id, models.User.login,
#                                      models.User.funds).filter_by(
#         id=session.get('user_id')).first()
#     return render_template('funds.html', funds=data['funds'])
#
#
# @app.post('/funds')# вирішили не треба
# @login_required
# def add_funds():
#     #form_data = request.form якщо є та форма в html
#     database.init_db()
#     new_data_user = models.User.add_funds(5)
#     database.db_session.add(new_data_user)
#     database.db_session.commit()
#     return 'user account was modified'


@app.get('/user/reservations')# список резервацій юзера
@login_required
def get_reservation_list():
    #user = session.get('user', None)

    user = session.get('user')
    if not user:
        return redirect('/login')
    #form_data = request.form # тільки якщо в темплейті є та форма!!
    database.init_db()
    reservations = (database.db_session.query(models.Reservation.id,
                                              models.Reservation.date,
                                              models.Reservation.time,
                                              models.Service.name.label('service_name'),
                                              models.Coach.name.label('coach_name'))
                    .join(models.Service, models.Reservation.service_id == models.Service.id)
                    .join(models.Coach, models.Reservation.coach_id == models.Coach.id)
                    .filter(models.Reservation.user_id == user['id'])
                    .all())

    return render_template('get_reservation_list.html', reservations=reservations)


@app.post('/user/reservations')# додати резервацію начебто зробила
@login_required
def add_reservation():
    user_id = session.get('user_id', None)
    if not user_id:
        return redirect('/login')

    form_dict = request.form
    service_id = form_dict['service_id']
    coach_id = form_dict['coach_id']
    slot_id = form_dict['slot_id']
    result = clac_slots(1,1,1)
    database.init_db()
    new_reservation = models.Reservation(user_id=session.get("user_id"),
                                         coach_id=form_dict["coach_id"],
                                         service_id=form_dict["service_id"],
                                         date=["date"], time=["time"])

    # new_reservation = models.Reservation(user_id=user_id,
    #                                      coach_id=coach_id,
    #                                      service_id=service_id,
    #                                      date=date,
    #                                      time=time)

    database.db_session.add(new_reservation)
    database.db_session.commit()

    send_mail("irajhdhj@gmail.com", "test_subject", "some text")
    return redirect('/user/reservations')


@app.post('/user/reservations/<reservation_id>/delete')# видалити резервацію
@login_required
def delete_reservation(reservation_id):
    database.init_db()
    database.db_session.query(models.Reservation).filter_by(id=reservation_id,
                                                            user=session.get('user_id')).delete()
    database.db_session.commit()
    return redirect('/user/reservations')


@app.get('/user/reservations/<reservation_id>')# отримати інф про конкретну резервацію
@login_required
def get_reservation_id(reservation_id):
    columns = (models.Reservation.id, models.Reservation.date, models.Reservation.time,
               models.Coach.name.label('coach.name'),
               models.Service.name.label('service.name'),
               models.User.login.label('user.login'))
    data = (database.db_session.query(*columns).join(models.User).join(models.Service).join(models.Coach)).filter(
        models.User.id == session.get('user_id'), models.Reservation.id == reservation_id).first()
    return render_template('reservation.html', reservation=data)# res=data?????




#     with SQLiteDatabase('db.db') as db:
#         reservation = db.fetch_one('reservation', {'reservation_id': reservation_id},
#                                    join_table={'user': 'reservation.user_id = user.id',
#                                                'service': 'reservation.service_id = service.id'},
#                 join_condition=['reservation.id as reservation_id', 'reservation.date',
#                 'reservation.time', 'user.login as user_name', 'service.name as service_name'])
#         if reservation:
#             return render_template('get_service_info.html',
#                                                     reservation=reservation)
#         else:
#             return f"reservation {reservation_id} not found"



@app.post('/pre_reservation') # зі сторінки тренера? тут треба доробити
@login_required
def pre_reservation():
    # user = session.get('user', None)
    coach = request.form['coach']
    service = request.form['service']
    desired_date = request.form['desired_date']

    time_slots = clac_slots(coach, service, desired_date)
    return render_template('pre_reservation.html',
                           form_info={'coach': coach,
                                      'service': service,
                                      'desired_date': desired_date,
                                      'time_slots': time_slots})


@app.get('/fitness_center')
def fitness_center_info():
    database.init_db()
    columns = (models.FitnessCenter.id, models.FitnessCenter.address,
               models.FitnessCenter.name, models.FitnessCenter.contacts)
    data = database.db_session.query(*columns).all()
    return render_template('fitness_center_info.html',
                           fitness_center=data)


@app.get('/fitness_center/<fitness_center_id>')
def get_fitness_center_id_info(fitness_center_id):
    database.init_db()
    columns = (models.FitnessCenter.id, models.FitnessCenter.address,
               models.FitnessCenter.name, models.FitnessCenter.contacts)
    data = database.db_session.query(*columns).filter_by(id=fitness_center_id).first()
    return render_template('fitness_center_id_info.html',
                            fitness_center_id=data)


@app.get('/fitness_center/<fitness_center_id>/coaches')# списоk тренерів цього клубу
def get_coaches(fitness_center_id):
    database.init_db()
    columns = (models.Coach.id,
               models.FitnessCenter.name,
               models.Coach.name,
               models.Coach.age,
               models.Coach.sex)
    data = (database.db_session.query(*columns).join(models.FitnessCenter)).filter(
        models.Coach.fitness_center_id == fitness_center_id).all()
    return render_template('get_coaches.html',
                           coaches=data, fitness_center_id=fitness_center_id)

@app.get('/fitness_center/<fitness_center_id>/coaches/<coach_id>')
def get_coach(fitness_center_id, coach_id):
    database.init_db()

    coach = (database.db_session.query(
        models.Coach.id,
        models.Coach.name,
        models.Coach.age,
        models.Coach.sex,
        models.Coach.fitness_center_id,
        models.FitnessCenter.name.label('fitness_center_name')
    )
    .join(models.FitnessCenter)
    .filter(models.Coach.fitness_center_id == fitness_center_id,
            models.Coach.id == coach_id)
    .first())
    return render_template('get_coach.html', coach=coach)


    # service selection for reservation треба доробити таблицю для цього сервісу
    # columns = (models.CoachCapacity.service.label('service.id'),
    #            models.Service.name.label('service.name'))
    # service_data = (database.db_session.query(*columns).join(models.Service).join(models.Coach)).filter(
    #     models.CoachCapacity.coach == coach_id, models.Coach.fitness_center_id == fitness_center_id).all()
    #
    # return render_template('get_coach.html', res=data,
    #                        service=service_data, coach=coach_id, fitness_center_id == fitness_center_id)

#++++++++++++++++++++ example for join ++++++++++++++++
# @app.get('/fitness_center/<fitness_center_id>/coach/<coach_id>')
# def get_coach_info(coach_id):
#     with SQLiteDatabase('db.db') as db:
#         res = db.fetch_one("coach", {'coach_id': coach_id})
#
#     return render_template('get_coach_info.html', res=res)
#
#     приклад як джоін робити
#     res = db.fetch_one("coach", condition={'coach_id': coach_id},
#                            join_table={'coach_services'},
#                    join_condition={'coach.id = coach_services.coach_id})
#

@app.get('/fitness_center/<fitness_center_id>/coaches/<coach_id>/score')  # всі відгуки показати
@login_required
def get_coach_score(fitness_center_id, coach_id):
    #user = session.get('user', None)
    database.init_db()
    # reviews = (database.db_session.query(models.Review.id, models.Review.text,
    #                                   models.Review.points, models.User.login,
    #                                   models.Coach.name.label('coach_name'))
    #                                   .join(models.User, models.User.id == models.Review.user_id, isouter=True)
    #                                   .join(models.Coach, models.Coach.id == models.Review.coach_id)
    #                                   .filter(models.Coach.fitness_center_id == fitness_center_id,
    #                                           models.Coach.id == coach_id)
    #                                   .all())
    reviews = (database.db_session.query(models.Review.points, models.Review.text, models.Coach.id)
               #.join(models.User, models.User.id == models.Review.user_id)
               .filter(models.Review.coach_id == coach_id)
               .all())
    if not reviews:
        return render_template('get_coach_score.html',
                               fitness_center_id=fitness_center_id, coach_id=coach_id,
                               message="No reviews found for this coach")
    return render_template('get_coach_score.html', coach_id=coach_id,
                           fitness_center_id=fitness_center_id,
                           reviews= reviews)#reviews=score)
                           #score=data, points=points, text=text)

    # data = (database.db_session.query(*columns)
    #              .join(models.User, models.User.id == models.Review.user_id, isouter=True)
    #              .join(models.Coach, models.Coach.id == models.Coach.id, isouter=True)
    #              .filter(models.Coach.fitness_center_id == fitness_center_id,
    #                      models.Coach.id == coach_id)).all()


@app.get('/fitness_center/<fitness_center_id>/coaches/<coach_id>/form_score') # написати(створити) відгук про тренера
@login_required
def form_for_score(fitness_center_id, coach_id):
    return render_template('form_for_score.html', fitness_center_id=fitness_center_id,
                           coach_id=coach_id)


@app.post('/fitness_center/<fitness_center_id>/coaches/<coach_id>/fill_score') # написати(створити) відгук про тренера
@login_required
def set_coach_score(fitness_center_id, coach_id):
    form_data = request.form
    user = session.get('user', None)
    points = form_data.get('points')
    text = form_data.get('text')

    user_review = database.db_session.query(models.Review(user_id=user['id'],
                                                   coach_id=coach_id,
                                                   fitness_center_id=fitness_center_id,
                                                   points=int(points),
                                                   text=text))
    database.db_session.add(user_review)
    database.db_session.commit()

    return redirect('/fitness_center/<fitness_center_id>/coaches/<coach_id>')


@app.get('/fitness_center/<fitness_center_id>/services')
def get_services(fitness_center_id):
    services = database.db_session.query(
        models.Service.id,
        models.Service.name,
        models.Service.duration,
        models.Service.price,
        models.Service.description,
        models.Service.max_attendees,
        models.Service.fitness_center_id
    ).filter(
        models.Service.fitness_center_id == fitness_center_id
    ).all()

    return render_template('services.html', services=services,
                           fitness_center_id=fitness_center_id)

# не треба,бо вся інф є в сервісес
# @app.get('/fitness_center/<fitness_center_id>/services/<service_id>')
# def get_service_info(fitness_center_id, service_id):
#     database.init_db()
#
#     service = database.db_session.query(
#         models.Service.id,
#         models.Service.name,
#         models.Service.duration,
#         models.Service.price,
#         models.Service.description,
#         models.Service.max_attendees,
#         models.FitnessCenter.name.label('fitness_center_name')
#     ).join(models.FitnessCenter).filter(
#         models.Service.id == service_id,
#         models.Service.fitness_center_id == fitness_center_id
#     ).first()
#
#     if not service:
#         return render_template('services.html', message="Service not found.")
#
#     return render_template('get_service_info.html', service=service)

    # with SQLiteDatabase('db.db') as db:
    #     res = db.fetch_one('service', {'fitness_center_id': fitness_center_id, 'service_id': service_id},
    #                        join={'fitness_center': 'service.fitness_center_id = fitness_center.id'},
    #                        columns=['service.id as service_id', 'service.name', 'service.duration'
    #                                 'service.description','service.max_attendees',
    #                                 'fitness_center.name as fitness_center_name'])

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8080
    app.run(host=host, port=port, debug=True)
