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

#from send_mail import add

#import sqlite3
from flask_session import Session

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


app = Flask(__name__, template_folder='templates')
# app.secret_key = "123456789"
app.secret_key = os.environ.get("SESSION_SECRET_KEY")


# def login_required(func):
#     @wraps(func)
#     def wr1(*args, **kwargs):
#         if session.get('user') is None:
#             return redirect('/login')
#         result = func(*args, **kwargs)
#         return result
#     return wr1()

def login_required(func):
    @wraps(func)
    def wr1(*args, **kwargs):
        if 'user' in session:
            return func(*args, **kwargs)
        else:
            redirect('/login')
    return wr1()
############################


@app.get('/')
def index():
    #return render_template('index.html')
    return redirect('/fitness_center_info')


@app.get('/registration')  # відображає форму
def user_register_invitation():
    return render_template('registration.html')


def check_credentials(username, password): # перевіряє залогінився чи ні
    database.init_db()
    user = database.db_session.query(models.User).filter_by(
        login=username, password=password).first()# all()

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
                        birth_date=datetime.datetime.strptime(form_data["birth_date"], "%y-%m-%d"),
                        phone=form_data['phone'])
    database.db_session.add(user1)
    database.db_session.commit()

    return "user registered"


@app.get('/login') # відображає форму
def user_login_form():
    user = session.get("user")
    if user:
        return redirect('/user')# redirect будує якийсь обʼєкт з відповіддю(як return)
    return render_template('user_login.html')


@app.post('/login') # готово під алхімію
def user_login():
    login = request.form['login']
    password = request.form['password']
    user = check_credentials(login, password)
    if user is not None:
        session['user'] = {'id': user.id, 'login': user.login}
        return redirect('/user')
    else:
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
    user = session.get("user_id")
    #user = session.get(user_id) #чому так не можу?
    database.init_db()
    #?????????????
    data = database.db_session.query(models.User.login, models.User.birth_date,
                                     models.User.phone).filter_by(
        id=session.get('user_id')).first()

    columns = (models.User.login, models.User.birth_date,
               models.User.phone)#, models.User.email)
    data2 = database.db_session.query(*columns).filter_by(
        id=session.get('user_id')).first()
    return render_template('user_info.html', user_info=data)# user=data?????????

    # with SQLiteDatabase('db.db') as db:
    #     res = db.fetch_one("user", {'id': user_id})
    # return render_template('user_info.html', user_info=res) #? user=res ????????????


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

    # with SQLiteDatabase('db.db') as db:
    #     res = db.fetch_one("user", {'id': user_id})
    # return render_template('user_info.html', user=res)


@app.get('/funds')
@login_required
def user_deposit_info(user_id):# де використати user_id,
    database.init_db()
    data = database.db_session.query(models.User.id, models.User.login,
                                     models.User.funds).filter_by(
        id=session.get('user_id')).first()
    return render_template('funds.html', funds=data['fund'])

    # with SQLiteDatabase('db.db') as db:
    #     res = db.fetch_one("user", {"id": user_id})
    #     return render_template('funds.html', funds=res['funds'])


@app.post('/funds')# todo this
#@login_required # чи треба тут це?!!!!!!!!!!!!!!!!!!
def add_funds():
    form_data = request.form
    database.init_db()
    new_data_user = models.User.add_funds() # ??????????
    new_data_user2 = models.User.withdraw()
    database.db_session.add(new_data_user)
    database.db_session.add(new_data_user2)
    database.db_session.commit()
    return 'user account was modified'


@app.get('/user/reservations')# список резервацій юзера
@login_required
def get_reservation_list():
    # user = session.get('user', None)
    # with SQLiteDatabase('db.db') as db:
    #     services = db.fetch_all("service", join_table=['id', 'name'])# можливо не треба сервіси
    #     reservations = db.fetch_all("reservation", condition={'user_id': user,
    #             'service_id': service.id},#можливо 'service_id': service.id взагалі не треба???
    #                                 join_table={'service'},
    #                                 join_condition={reservation.service_id = service.id})
    #     return render_template('get_reservation_list.html',
    #                    reservations=reservations, services=services)

    form_data = request.form
    database.init_db()
    reservations = database.db_session.query(models.User(login=form_data["login"]),
                    models.Service(name=form_data["name"]),
                    models.Coach(name=form_data["name"]),
                    models.Reservation(id=int(form_data["id"]),date=form_data["date"],time=form_data["time"]))
    return render_template('get_reservation_list.html', ????=reservations)  # ?????????


@app.post('/user/reservations')# додати резервацію начебто зробила
@login_required
def add_reservation():
    user_id = session.get('user_id', None)
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
    database.db_session.add(new_reservation)
    database.db_session.commit()
    return redirect('/user/reservations')

    # #send_mail('ira.jhdhj@gmail.com', 'test_subject', )



@app.post('/user/reservations/<reservation_id>')# редагувати резервацію
@login_required
def rebuild_reservation(reservation_id):
    pass


@app.post('/user/reservations/<reservation_id>/delete')# видалити резервацію
@login_required
def delete_reservation(reservation_id):
    # user_id = session.get('user_id', None) не знаю чи треба це
    # from_dict = request.form
    # service_id = from_dict['service_id']
    # coach_id = from_dict['coach_id']
    # slot_id = from_dict['slot_id']
    # result = clac_slots(1,2,4)
    database.init_db()
    database.db_session.query(models.Reservation).filter_by(id=reservation_id,
                                                            user=session.get('user_id')).delete()
    database.db_session.commit()
    return redirect('/user/reservations')

    # with SQLiteDatabase('db.db') as db:
    #     db.delete_data("reservation", {'reservation' : reservation_id,
    #                                                 'user_id': user_id['id'],
    #                                                 'service_id': service_id['id'],
    #                                                 'coach_id' : coach_id['id'],
    #                                                 'date': request.form.get('date'),
    #                                                 'time': request.form.get('time')})
    #
    # # send_mail('ira.jhdhj@gmail.com', 'test_subject', )
    #
    # return redirect('/user/reservations')


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


@app.get('/checkout')# можливо не треба це робити, бо не хочу
@login_required
def get_checkout_box():# звідки взяти інф?
    return f"""<form action='/checkout' method='post'>
      <label for="checkout_box">checkout_box:</label><br>
      <input type="text" id="checkout_box" name="checkout_box"><br>
     
      <input type="submit" value="Submit"
    </form>"""


@app.post('/checkout')  # оформлюємо замовленя
@login_required
def add_training():
    return 'training was added'


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
    data = database.db_session.query(*columns).filter_by(id=fitness_center_id.first()
    return render_template('fitness_center_id_info.html',
                           fitness_center_id=data['fitness_center_id'])


@app.get('/fitness_center/<fitness_center_id>/coaches/')
def get_coaches(fitness_center_id):
    database.init_db()
    columns = (models.Coach.id.label('coach.id'),
               models.FitnessCenter.name.label('fitness_center.name'),
               models.Coach.name.label('coach.name'),
               models.Coach.age.label('coach.age'),
               models.Coach.sex.label('coach.sex'))
    data = (database.db_session.query(*columns).join(models.FitnessCenter)).filter(
        models.Coach.fitness_center_id == fitness_center_id).all()
    # що тут = data?????? coaches?????/
    return render_template('get_coach.html', ???=data, fitness_center_id=fitness_center_id)

@app.get('/fitness_center/<fitness_center_id>/coaches/coach/')
def get_coach(fitness_center_id, coach_id):
    database.init_db()
    columns = (models.FitnessCenter.name.label('fitness_center.name'),
               models.Coach.name.label('coach.name'),
               models.Coach.age.label('coach.age'),
               models.Coach.sex.label('coach.sex'))
    data = (database.db_session.query(*columns).join(models.FitnessCenter)).filter(
        models.Coach.fitness_center_id == fitness_center_id, models.Coach.id).first()
    return render_template('get_coach.html') # coach=data ??????????

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
def get_coach_score(coach_id):
    user = session.get('user', None)
    database.init_db() # не знаю що тут робити
    columns = (models.Review.points.label('review.points'),
               models.Coach.name.label('coach.name'),
               models.Review.text.label('review.text'),
               models.User.login.label('user.login'),
               models.User.id.label('user.id'))
    data = (database.db_session.query(*columns)
                 .join(models.User, models.User.id == models.Review.user_id, isouter=True)
                 .join(models.Coach, models.Coach.id == models.Coach.id, isouter=True)
                 .filter(models.Coach.fitness_center_id == fitness_center_id,
                         models.Coach.id == coach_id)).all()

    return render_template('get_coach_score.html',
                           score=data,
                           points=points, text=text)


@app.post('/fitness_center/<fitness_center_id>/coaches/<coach_id>/score') # написати(створити) відгук про тренера
@login_required
def set_coach_score(coach_id):
    form_data = request.form
    user = session.get('user', None)
    points = request.form.get('points')
    text = request.form.get('text')

    user_review = database.db_session.query(Review(user_id=user['id'],
                                                   coach_id=coach_id,
                                                   fitness_center_id=fitness_center_id,
                                                   points=int(points),
                                                   text=text))
    database.db_session.add(user_review)
    database.db_session.commit()

    return redirect('/score')


@app.get('/fitness_center/<fitness_center_id>/services/')# чи тут щось треба?
def get_services(fitness_center_id):
    database.init_db()
    # services = database.db_session.query(models.Service).filter_by(
    #     models.Service.fitness_center_id == fitness_center_id).all()

    columns = (models.Service.id.label('service.id'),
               models.Service.name.label('service.name'),
               models.Service.description, models.Service.duration, models.Service.price,
               models.FitnessCenter.name.label('fitness_center_id.name'))
    data = ((database.db_session.query(*columns).join(models.FitnessCenter)).
            filter(models.Service.fitness_center_id == fitness_center_id).all())

    return render_template('services.html',
                           fitness_center_id=fitness_center_id)

    # with SQLiteDatabase('db.db') as db:
    #     res = db.fetch_all("service", {"fitness_center_id": fitness_center_id},
    #                       join={'fitness_center': 'service.fitness_center_id = fitness_center.id'},
    #                       columns=['service.id as service_id', 'service.name', 'service.time',
    #                                'service.description','service.max_attendees',
    #                                'service.duration', 'fitness_center.name as fitness_center_name'])

@app.get('/fitness_center/<fitness_center_id>/services/<service_id>')
def get_service_info(fitness_center_id, service_id):
    database.init_db()
    columns = (models.Service.name.label('service.name'),
               models.Service.description, models.Service.duration,
               models.Service.price,models.FitnessCenter.name.label('fitness_center_id.name'))
    data = (database.db_session.query(*columns).join(models.FitnessCenter)).filter(
        models.Service.fitness_center_id == fitness_center_id,
        models.Service.id == service_id).first()

    return render_template('get_service_info.html', service_name=data)


    # with SQLiteDatabase('db.db') as db:
    #     res = db.fetch_one('service', {'fitness_center_id': fitness_center_id, 'service_id': service_id},
    #                        join={'fitness_center': 'service.fitness_center_id = fitness_center.id'},
    #                        columns=['service.id as service_id', 'service.name', 'service.duration'
    #                                 'service.description','service.max_attendees',
    #                                 'fitness_center.name as fitness_center_name'])




# @app.get('/fitness_center/<gim_id>/loyalty_programs')  # отримати інф
# def get_loyalty_prog_info(gim_id): # тут просто текст буде
#     res = get_from_db(f'select loyalty_programs from ????? where id=1{gim_id}', )
#     return res


if __name__ == '__main__':
    host = '127.0.0.1' # '0.0.0.0' в чому різниця
    port = 8080
    app.run(host=host, port=port, debug=True)
