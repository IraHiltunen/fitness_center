
# @app.route("/")
# def hel():
#     return "hi?ira"
#
# @app.route("/user/<id>")
# def show():
#     return f'user name{}'

# get - отримати(без параметрів) отримаємо дані цілком(повну інф)
# post - створити щось нове(з параметрами)!!!  як правило в REST
# put - відредагувати(з параметрами) !!!  як правило в REST
# delete - (без параметрів) просто видаляємо
# Flask port 5000

# SELECT Orders.OrderID, Customers.CustomerName, Orders.OrderDate що вибираємо з таблиць
# FROM Orders  з якої таблиці вибираємо
# INNER JOIN Customers ON Orders.CustomerID=Customers.CustomerID;
#              join яку ще таблицю ON умова, за якою їх обʼєднуємо

# Select * from reservation
#     join service on service.id = reservation.service_id обʼєднати з табл сервіс за умови:
#                     в табл сервіс id = в табл резервейшн cervice_id
#     join coach_schedule on reservation.date = coach_schedule.date and reservation.coach_id=coach_schedule.coach
#     where reservation.coach_id = 1

from flask import Flask, request, render_template, session, redirect
from flask_session import Session
from functools import wraps
#import sqlite3
# import utils
import os
from send_mail import add

from utils import SQLiteDatabase
from utils import clac_slots

app = Flask(__name__, template_folder='templates')
# app.secret_key = "123456789"
app.secret_key = os.environ.get("SESSION_SECRET_KEY")


def login_required(func):
    @wraps(func)
    def wr1(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect('/login')
        result = func(*args, **kwargs)
        return result
    return wr1()

############################


@app.get('/')# todo template for this
def index():
    add.delay(1, 2)
    return render_template('index.html')


@app.get('/registration')  # відображає форму
def user_register_invitation():
    return render_template('registration.html')


def check_credentials(username, password): #... перевіряє залогінився чи ні
    with SQLiteDatabase('db.db') as db:
        user = db.fetch_one("user", {"login": username, "password": password})
    return user is not None

@app.post('/registration') # запис в базу даних
def post_register():
    form_data = request.form

    with SQLiteDatabase('db.db') as db:
        # form_data = request.form # у кого-то так не знаю треба мені чи ні
        # user_name = form_data.get('username')
        # password = form_data.get('password')
        # birthday = form_data.get('birthday')
        # phone = form_data.get('phone')
        db.add_data("user", {"login": form_data["login"], "password": form_data['password'],
                             "birth_date": form_data["birth_date"], "phone": form_data['phone']})
    return 'user registered'


@app.get('/login') # відображає форму
def user_login_form():
    user = session.get("user_id")
    if user:
        return redirect('/user')# redirect будує якийсь обʼєкт з відповіддю(як return)
    return render_template('user_login.html')


@app.post('/login')
def user_login():
    login = request.form['login']
    password = request.form['password']
    if check_credentials(login, password):# чи це треба?
        with SQLiteDatabase('db.db') as db:
            user = db.fetch_one("user", {"login": login})
        session['user_id'] = user['id']
        return redirect('/user')


@app.get('/logout')
@login_required
def logout():
    session.pop('user_id')
    return redirect('/login')


@app.get('/user/<user_id>')
@login_required
def get_user_info(user_id):
    with SQLiteDatabase('db.db') as db:
        res = db.fetch_one("user", {'id': user_id})
    return render_template('user_info.html', user=res)


@app.post('/user/<user_id>')# мабуть щось переробити треба
@login_required
def add_user_info(user_id):
    with SQLiteDatabase('db.db') as db:
        res = db.fetch_one("user", {'id': user_id})
    return render_template('user_info.html', user=res)


@app.get('/funds')
@login_required
def user_deposit_info(user_id):
    with SQLiteDatabase('db.db') as db:
        # res = db.fetch_one('select funds from user where id=1', user_id)

        res = db.fetch_one("user", {"id": user_id}, columns=['funds.id as funds_id'])
        return render_template('funds.html', funds=res['funds'])


@app.post('/funds')# todo this
def add_funds():
    return 'user account wes modified'


@app.get('/user/reservations') # список резервацій юзера
@login_required
def get_reservation_list():
    user_id = session.get('user_id', None)
    with SQLiteDatabase('db.db') as db:
        #services = db.fetch_one("service", columns=['id', 'name'])
        reservations = db.fetch_one("reservation", join={'user': 'reservation.user_id = user.id',
                            'service': 'reservation.service_id = service.id',
                            'fitness_center': 'service.fitness_center_id = fitness_center.id'},
                            columns=['reservation.id as reservation_id', 'reservation.date',
                                    'reservation.time', 'user.login as user_name',
                                    'service.name as service_name', 'fitness_center as fitness_center'],
                            condition={'user_id': user_id})
        return render_template('get_reservation_list.html',
                       reservations=reservations) #, services=services)

    from_dict = request.form
    service_id = form_dict['service_id']
    coach_id = form_dict['coach_id']
    slot_id = form_dict['slot_id']



@app.post('/user/reservations')# додати резервацію
@login_required
def add_reservation():
    user_id = session.get('user_id', None)
    with SQLiteDatabase('db.db') as db:
        db.add_data("reservation", {'user_id': user_id['id'],
                                    'service_id': request.form.get('service_id'),
                                    'date': request.form.get('date'),
                                    'time': request.form.get('time')})

    send_mail('ira.jhdhj@gmail.com', 'test_subject', )

    return redirect('/user/reservations')


@app.post('/user/reservations/<reservation_id>')# редагувати резервацію
@login_required
def rebuild_reservation(reservation_id):


@app.post('/user/reservations/<reservation_id>/delete')# видалити резервацію
@login_required
def delete_reservation(reservation_id):

    return 'reservation was deleted'


@app.get('/user/reservations/<reservation_id>')# отримати інф про конкретну резервацію
@login_required
def get_reservation_id(reservation_id):
    with SQLiteDatabase('db.db') as db:
        reservation = db.fetch_one('reservation', {'reservation_id': reservation_id},
                                   join={'user': 'reservation.user_id = user.id',
                                        'service': 'reservation.service_id = service.id'},
                columns=['reservation.id as reservation_id', 'reservation.date',
                'reservation.time', 'user.login as user_name', 'service.name as service_name'])
        if reservation:
            return render_template('get_service_info.html',
                                                    reservation=reservation)
        else:
            return f"reservation {reservation_id} not found"



@app.post('/pre_reservation')
@login_required
def pre_reservation():
    user = session.get('user', None)
    coach = request.form['coach']
    service = request.form['service']
    desired_date = request.form['desired_date']
    time_slots = clac_slots(coach, service, desired_date)
    return render_template('pre_reservation.html', form_info={'coach': coach,
                                                                'service': service,
                                                                'desered_date': desired_date,
                                                                'time_slots': time_slots})


@app.get('/checkout')
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
    with SQLiteDatabase('db.db') as db:
        res = db.fetch_all('select * from fitness_center ')
        return render_template('fitness_center_info.html', fitness_center_info=res)

    # res = get_from_db('select name, address from fitness_center')
    # return str(res)


@app.get('/fitness_center/<gim_id>')
def get_gim_id_info(gim_id):
    with SQLiteDatabase('db.db') as db:
        res = db.fetch_one('select * from fitness_center where id=1', gim_id)
        return render_template('get_gim_id_info.html', get_gim_id_info=res['get_gim_id_info'])


@app.get('/fitness_center/<gim_id>/coaches/')# чи потрібен список тренерів?
def get_coaches(gim_id):
    with SQLiteDatabase('db.db') as db:
        res = db.fetch_all('select * from coach ', gim_id)
        return render_template('get_coaches.html', get_coaches=res)


@app.get('/fitness_center/<gim_id>/coach/')
def get_coach(gim_id):
    with SQLiteDatabase('db.db') as db:
        res = db.fetch_one('coach', {'gim_id': gim_id},
                           join={'gim': 'coach.gim_id = gim.id'},
                           columns={'coach.id as coach_id', 'coach.name as coach_name',
                                    'gim.name as gim_name'})
        return render_template('get_coach.html', get_coach=res)

@app.get('/fitness_center/<gim_id>/coach/<coach_id>')
def get_coach_info(gim_id, coach_id):
    with SQLiteDatabase('db.db') as db:
        res = db.fetch_one("coach",{'gim_id': gim_id, 'coach_id': coach_id},
                           join={'gim': 'coach_id = gim_id'},
                           columns=['coach.id as coach_id', 'coach.name as coach_name',
                                    'gim.name as gim_name'])
        return render_template('get_coach_info.html', get_coach_info=res)

    # if res is not None:
    #     return  render_template('get_coach_info.html', get_coach_info=res)
    # else:
    #     return "service is not found "


@app.get('/fitness_center/<gim_id>/coaches/<coach_id>/score')  # відгук показати
@login_required
def get_coach_score(gim_id, coach_id):
    # user_id = session.get('user_id', None)
    with SQLiteDatabase('db.db') as db:
        # серед всіх відгуків знайти відгук кор-ча і ним заповнити форму
        score = db.fetch_one("score", # тут всі відгуки!!!!!!!!!!!
                            join={'coach': 'score.coach_id = coach.id',
                                  'gim': 'score.gim_id = gim.id',
                                  'user': 'score.user_id = user.id'},
                             columns=['score.text', 'score.points', 'user.login',
                                      'gim.name as gim_name', 'coach.name as coach_name'],
                             condition={"score.user_id": session.get("user_id")})
    return render_template('get_coach_score.html', score=score)

        # res = db.fetch_one('select * from review where id=1 and coach_id=1', gim_id, coach_id)
        # return render_template('get_coach_score.html', get_coach_score=res['get_coach_score'])


@app.post('/fitness_center/<gim_id>/coaches/<coach_id>/score') # написати(створити) відгук про тренера
@login_required
def set_trainer_score(gim_id, coach_id):
    #form_data = request.form
    user_id = session.get('user_id')
    points = request.form.get('points')
    review = request.form.get('review')

    with SQLiteDatabase('db.db') as db:
        reviews = db.fetch_one("review",
                               condition={'coach_id': coach_id, 'user_id': user_id['id']})
        if reviews is not None:
            db.edit_data("review", {'points': points, 'review': review},
                         condition={'coach_id': coach_id, 'user_id': user_id['id']})
        else:
            db.add_data("review", {'coach_id': coach_id, 'gim_id': gim_id,
                          'user_id': user_id, 'points': points, 'text': review})
    return 'score updated'
    #return redirect(where?)# чи треба тут редірект


@app.get('/fitness_center/<gim_id>/services/')# чи тут щось треба?
def get_services(gim_id):
    with SQLiteDatabase('db.db') as db:
        res = db.fetch_all("service", {"gim_id": gim_id},
                          join={'gim': 'service.gim_id = gim.id'},
                          columns=['service.id as service_id', 'service.name', 'service.time',
                                   'service.description','service.max_attendees',
                                   'service.duration', 'gim.name as gim_name'])
    return render_template('services.html', services=res)


@app.get('/fitness_center/<gim_id>/services/<service_id>')
def get_service_info(gim_id, service_id):
    with SQLiteDatabase('db.db') as db:
        res = db.fetch_one('service', {'gim_id': gim_id, 'service_id': service_id},
                           join={'gim': 'service.gim_id = gim.id'},
                           columns=['service.id as service_id', 'service.name', 'service.duration'
                                    'service.description','service.max_attendees',
                                    'gim.name as gim_name'])
    return render_template('get_service_info.html', get_service_info=res)
        # if res is not None:
        #     return  render_template('get_service_info.html', get_service_info=res)
        # else:
        #     return "service is not found "


@app.get('/fitness_center/<gim_id>/loyalty_programs')  # отримати інф
def get_loyalty_prog_info(gim_id): # тут просто текст буде
    res = get_from_db(f'select loyalty_programs from ????? where id=1{gim_id}', )
    return res


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    app.run(host=host, port=port, debug=True)
