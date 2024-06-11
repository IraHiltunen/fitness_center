
# if __name__ == '__main__':
# host = '127.0.0.1'
# port = 8080
# app.run(host=host, port=port, debug=True)

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

# SELECT Orders.OrderID, Customers.CustomerName, Orders.OrderDate що вибираємо з таблиць
# FROM Orders  з якої таблиці вибираємо
# INNER JOIN Customers ON Orders.CustomerID=Customers.CustomerID; join яку ще таблицю ON умова, за якою їх обʼєднуємо

from flask import Flask, request, render_template, session, redirect
from functools import wraps
import sqlite3

app = Flask(__name__)



class SQLiteDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = dict_factory # dict_factory(cursor, row)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

    def fetch_all(self, table, condition=None, join_table=None, join_condition=None):
        # join_condition = {"fitness_center.id": "service.name"} вказати таблицю і поле!!!
        # join_condition = {"{join table}" :{"fitness_center.id": "service.name"}}
        query = f"SELECT * FROM{table}"
        conditions = []

        if join_table is not None:
            join_cond_list = []
            for key, val in join_condition.items():
                conditions.append(f"{key}='{val}' ")
            join_cond_str = ' and '.join(join_cond_list)
            join_str = f' join {join_table} on {join_cond_str} '
            query = query + join_str

        if condition is not None:
            for key, val in condition.items():
                conditions.append(f"{key}='{val}' ")
            str_conditions = "and ".join(conditions)
            str_conditions = " where " + str_conditions
            query = query + str_conditions

        cursor = self.connection.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        if res:
            return res
        return None

    def fetch_one(self, query, *args, **kwargs): # доробити
        cursor = self.connection.cursor()
        cursor.execute(query, *args, **kwargs)
        res = cursor.fetchone()
        if res:
            return res
        return None

    def add_data(self, table, data): # renamed commit
        keys = []
        vals = []
        for key, value in data.items():
            keys.append(key)
            vals.append("'" + str(value) + "'")

        str_keys = ', '.join(keys)
        str_vals = ', '.join(vals)
        query = f"""INSERT INTO {table} ({str_keys}) VALUES ({str_vals})"""
        cursor = self.connection.cursor
        cursor.execute(query)
        self.connection.commit()

    # def commit(self, query, *args, **kwargs):
    #     cursor = self.connection.cursor()
    #     cursor.execute(query, *args, **kwargs)
    #     self.connection.commit()

############################

def dict_factory(cursor, row): # for 4 hometask?
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_from_db(query, many=True): # for 4 hometask?
    con = sqlite3.connect('db.db')

    con.row_factory = dict_factory

    cur = con.cursor()
    cur.execute(query)
    if many:
        res = cur.fetchall()
    else:
        res = cur.fetchone()
    con.close()
    return res

def insert_to_db(query): # for 4 hometask?
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    cur.execute(query)
    con.commit() # зафіксувати зміни
    con.close()


@app.get('/registration')  # відображає форму
def user_register_invitation():
    return render_template('registration.html')

#     return f"""<form action='/register' method='post'> # why post?!!!!
#   <label for="login">login:</label><br>
#   <input type="text" id="login" name="login"><br>
#   <label for="password">password:</label><br>
#   <input type="password" id="password" name="password">
#   <label for="birth_date">birth_date:</label><br>
#   <input type="date" id="birth_date" name="birth_date">
#   <label for="phone">phone:</label><br>
#   <input type="text" id="phone" name="phone">
#
#   <input type="submit" value="Submit"
# </form>"""


# def check_credentials(username, password): //це чиєсь... поки не знаю що)
#     with SQLiteDatabase('db.db') as db:
#         user = db.fetchone('select * from user where login =  and password =', (username, password))
#     return user is not None

@app.post('/registration') # запис в базу даних
def post_register():
    form_data = request.form

    with SQLiteDatabase('db.db') as db:
        db.add_data("user", {"login": form_data["login"], "password": form_data['password'],
                             "birth_date" : form_data["birth_date"], "phone": form_data['phone']})
    return 'user registered'



@app.get('/login')
def user_login_form():
    return render_template('/user_login.html')# or /login_form???
    # return f"""<form action='/login_form' method='post'>
    #   <label for="login">login:</label><br>
    #   <input type="text" id="login" name="login"><br>
    #   <label for="password">password:</label><br>
    #   <input type="password" id="password" name="password">
    #   <input type="ok" value="Ok"
    # </form>"""

    # return 'enter credentials'


@app.post('/login')
def user_login():
    return 'new user logged in'


@app.get('/user')# показати усіх юзерів???????
def user_info():
    with SQLiteDatabase('db.db') as db:
        res = db.fetch_all("user")
        # res = get_from_db('select login, phone,birth_date  from user where id=1')
        return res

@app.get('user/<user_id>')
def get_user_info():
    with SQLiteDatabase('db.db') as db:
        res = db.fetch_one('SELECT login, phone, birth_date FROM user where id = 1', user_info)
        return render_template('user_info.html', user_info=res)


@app.post('/user')
def add_user_info():
    return 'user data were modified'


@app.put('/user')
def user_update():
    return 'user inf was successfully updated'


@app.get('/funds') # @app.get('/funds/<user_id>') чи потрібен тут юзер???
def user_deposit_info(user_id):
    with SQLiteDatabase('db.db') as db:
        res = db.fetch_one('select funds from user where id=1', user_id)

    # res = get_from_db('select funds from user where id=1')
        return render_template('funds.html', funds=res['funds'])


@app.post('/funds') # @app.get('/funds/<user_id>')
def add_funds():
    return 'user account wes modified'


@app.get('/reservations_list') # '/user/reservations'
@login_required
def get_reservation_list():
    # res = get_from_db('select * from reservation where id=1{user_id}')
    # return {res}

    user = session.get('user', None)
    with SQLiteDatabase('db.db') as db:
        services = db.select_method("service", columns=['id', 'name'], fetch_all=True)
        reservations = db.select_method("reservation", join={'user': 'reservation.user_id = user_id',
                                                             'service': 'reservation.service_id = service_id',
                                                             'fitness_center': 'service.fitness_center_id = fitness_center.id'},
                                        columns=['reservation.id as reservation_id', 'reservation.date',
                                                 'reservation.time', 'user.login as user_name',
                                                 'service.name as service_name', 'fitness_center as fitness_center'],
                                        condition={'user_id': user['id']}, fetch_all=True)
    return render_template('reservations_list.html', reservations=reservations, services=services)

    from_dict = request.form
    service_id = form_dict['service_id']
    coach_id = form_dict['coach_id']
    slot_id = form_dict['slot_id']



@app.post('/reservations')
def add_reservation():
    return 'reservation was added'


@app.get('/user/reservations/<reservation_id>/')
def get_reservation_id(reservation_id):
    with SQLiteDatabase('db.db') as db:
        res = db.fetch_one('select service_id from reservation where id=1', reservation_id)
        return render_template('get_service_info.html', get_service_info=res['get_service_info'])


@app.put('/user/reservations/<reservation_id>/')#????????
def update_reservation_id(reservation_id):
    return f'this {reservation_id} was updated'


@app.delete('/user/reservations/<reservation_id>/')#?????????
def delete_reservation_id(reservation_id):
    return f'this {reservation_id} was deleted'


@app.get('/checkout')
def get_checkout_box():# звідки взяти інф?
    return f"""<form action='/checkout' method='post'>
      <label for="checkout_box">checkout_box:</label><br>
      <input type="text" id="checkout_box" name="checkout_box"><br>
     
      <input type="submit" value="Submit"
    </form>"""


@app.post('/checkout')  # оформлюємо замовленя
def add_training():
    return 'training was added'


@app.put('/checkout')  # редагуємо корзину
def update_box():
    return 'checkout_box was updated'


@app.get('/fitness_center')# чи є таке у нас??? можливо треба одразу з айді
def fitness_center_info():
    with SQLiteDatabase  ('db.db') as db:
        res = db.fetch_all('select * from fitness_center ')
        return render_template('/fitness_center_info.html')

    # res = get_from_db('select name, address from fitness_center')
    # return str(res)


@app.get('/fitness_center/<gim_id>') #чим відрізняється просто від фітнес центра
def get_gim_id_info(gim_id):
    with SQLiteDatabase('db.db') as db:
        res = db.fetch_one('select * from fitness_center where id=1', gim_id)
        return render_template('get_gim_id_info.html', get_gim_id_info=res['get_gim_id_info'])
    # res = get_from_db(f'select name, address from fitness_center where id=1{gim_id}', False)
    # return str(res)


@app.get('/fitness_center/<gim_id>/coach/')
def get_coaches(gim_id):
    with SQLiteDatabase('db.db') as db:
        res = db.fetch_all('select * from coach ', gim_id)
        return render_template('/get_coaches.html')


@app.get('/fitness_center/<gim_id>/coach/<coach_id>')
def get_coach_info(gim_id, coach_id):
    with SQLiteDatabase('db.db') as db:
        res = db.fetch_one('select * from coach where id=1', gim_id, coach_id)
        return render_template('get_coach_info.html', get_coach_info=res['get_coach_info'])

@app.post('/pre_reservation')
@login_required
def pre_reservation():
    user = session.get('user', None)
    coach = request.form['coach']
    service = request.form['service']
    desired_date = request.form['desired_date']
    time_slots = clac_slots(coach, service, desired_date)
    return render_template('pre_reservation.html', form_info = {'coach': coach,
                                                                'service':service,
                                                                'desered_date':desired_date,
                                                                'time_slots':time_slots})

@app.get('/fitness_center/<gim_id>/coach/<coach_id>/score')  # відгук показати
def get_coach_score(gim_id, coach_id):
    with SQLiteDatabase('db.db') as db:
        res = db.fetch_one('select * from review where id=1 and coach_id=1', gim_id, coach_id)
        return render_template('get_coach_score.html', get_coach_score=res['get_coach_score'])


@app.post('/fitness_center/<gim_id>/coach/<coach_id>/score')  # написати(створити) відгук про тренера
def set_trainer_score(gim_id, coach_id):
    return f'in fitness center {gim_id} trainer {coach_id} received some score'


@app.put('/fitness_center/<gim_id>/coach/<coach_id>/score')  # редагувати відгук про тренера
def update_trainer_score(gim_id, coach_id):
    return f'fitness center {gim_id} trainer {coach_id} score was update'


@app.get('/fitness_center/<gim_id>/services/')
def get_services(gim_id):
    with SQLiteDatabase('db.db') as db:
        res = db.fetch_all("service", {"gim_id":gim_id})
        return res


@app.get('/fitness_center/<gim_id>/services/<service_id>')
def get_service_info(gim_id, service_id):
    with SQLiteDatabase('db.db') as db:
        res = db.fetch_one('select * from service where service_id=1 and gim_id=1', gim_id, service_id)
        return render_template('get_service_info.html', get_service_info=res['get_service_info'])

    # res = get_from_db(f'select name, description, price, max_attendees from service where id=1{gim_id}  and id=1{service_id}', False)
    # return str(res)


@app.get('/fitness_center/<gim_id>/loyalty_programs')  # отримати інф
def get_loyalty_prog_info(gim_id): # тутпросто текст буде
    res = get_from_db(f'select loyalty_programs from ????? where id=1{gim_id}', False)
    return res

    # return f'fitness center {gim_id} has such loyalty program'

