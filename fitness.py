
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
# post - створити щось нове(з параметрами)
# put - відредагувати(з параметрами)
# delete - (без параметрів) просто видаляємо

from flask import Flask, request
import sqlite3

app = Flask(__name__)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_from_db(query, many=True):
    con = sqlite3.connect('db.db') # db.sqbpro!???????????

    con.row_factory = dict_factory

    cur = con.cursor()
    cur.execute(query)
    if many:
        res = cur.fetchall()
    else:
        res = cur.fetchone()
    con.close()
    return res

def insert_to_db(query):
    con = sqlite3.connect('db.db')  # db.sqbpro!!!!!!!!!!!!!!!!!!
    cur = con.cursor()
    cur.execute(query)
    con.commit() # зафіксувати зміни
    con.close()


@app.get('/register')  # відображає форму
def user_register_invitation():
    return f"""<form action='/register' method='post'> # why post?!!!!
  <label for="login">login:</label><br>
  <input type="text" id="login" name="login"><br>
  <label for="password">password:</label><br>
  <input type="password" id="password" name="password">
  <label for="birth_date">birth_date:</label><br>
  <input type="date" id="birth_date" name="birth_date">
  <label for="phone">phone:</label><br>
  <input type="text" id="phone" name="phone">
  
  <input type="submit" value="Submit"
</form>"""


@app.post('/register') # запис в базу даних
def post_register():
    form_data = request.form
    insert_to_db(f'INSERT INTO user (login, password, birth_date, phone) VALUES (\'{form_data["login"]}\', \'{form_data["password"]}\', \'{form_data["birth_data"]}\', \'{form_data["phone"]}\')')
    return f'new user registered'
    # в чому різниця f'new user registered' 'enter credentials'


@app.get('/login')
def user_login_form():
    return f"""<form action='/login_form' method='post'>
      <label for="login">login:</label><br>
      <input type="text" id="login" name="login"><br>
      <label for="password">password:</label><br>
      <input type="password" id="password" name="password">
    
      <input type="ok" value="Ok"
    </form>"""

    # return 'enter credentials'


@app.post('/login')
def user_login():
    return 'new user logged in'


@app.get('/user')
def user_info():
    res = get_from_db('select login, phone,birth_date  from user where id=1')
    return {res}


@app.post('/user')
def add_user_info():
    return 'user data were modified'


@app.put('/user')  # яка різниця з пост
def user_update():
    return 'user inf was successfully update'


@app.get('/funds')
def user_deposit_info():
    res = get_from_db('select funds  from user where id=1')
    return {res}


@app.post('/funds')
def add_funds():
    return 'user account wes modified'


@app.get('/reservations')
def get_reservation_list():
    # smth wrong!!!!!!!!!!!!! по чому я повинна вибирати з бази(coach_id or user_id)?
    res = get_from_db('select service_id, date, time from reservation where id=1')
    return {res}

    # res = get_from_db(f'select service_id, date, time from reservation where id=1{gim_id}', False)
    # return str(res)


@app.post('/reservations')
def add_reservation():
    return 'reservation was added'


@app.get('/user/reservations/<reservation_id>/')
def get_reservation_id(reservation_id):
    res = get_from_db('select service_id  from reservation where id=1')
    return {res}

    # return f'info about {reservation_id}'


@app.put('/user/reservations/<reservation_id>/')
def update_reservation_id(reservation_id):
    return f'this {reservation_id} was updated'


@app.delete('/user/reservations/<reservation_id>/')
def delete_reservation_id(reservation_id):
    return f'this {reservation_id} was deleted'


@app.get('/checkout')
def get_checkout_box():# звідки взяти інф?
    return f"""<form action='/checkout' method='post'>
      <label for="checkout_box">checkout_box:</label><br>
      <input type="text" id="checkout_box" name="checkout_box"><br>
      <label for="password">password:</label><br>
      <input type="password" id="password" name="password">

      <input type="submit" value="Submit"
    </form>"""


@app.post('/checkout')  # оформлюємо замовленя
def add_training():
    return 'training was added'


@app.put('/checkout')  # редагуємо корзину
def update_box():
    return 'checkout_box was updated'


@app.get('/fitness_center')
def fitness_center_info():
    res = get_from_db('select name, address from fitness_center')
    return str(res)

    # gim_name = res[1]
    # birth_date = res[2]
    # # return str(res)
    # # return res
    # return {'phone': user_phone, 'birth_date': birth_date}

@app.get('/fitness_center/<gim_id>')
def get_gim_id_info(gim_id):
    res = get_from_db(f'select name, address from fitness_center where id=1{gim_id}', False)
    return str(res)


@app.get('/fitness_center/<gim_id>/coach/')
def get_coaches(gim_id):
    res = get_from_db(f'select coach* from fitness_center, where id=1{gim_id}', False)
    return res


@app.get('/fitness_center/<gim_id>/coach/<coach_id>')
def get_coach_info(gim_id, coach_id):
    res = get_from_db(f'select name, fitness_center_id, age, sex from coach where id=1{gim_id}, id=1{coach_id}', False)
    return str(res)


@app.get('/fitness_center/<gim_id>/coach/<coach_id>/score')  # відгук показати
def get_coach_score(gim_id, coach_id):
    res = get_from_db(f'select points, text from review where id=1{gim_id}, id=1{coach_id}', False)
    return res

    #return f'fitness center {gim_id}, trainer {coach_id} has score: '


@app.post('/fitness_center/<gim_id>/coach/<coach_id>/score')  # написати(створити) відгук про тренера
def set_trainer_score(gim_id, coach_id):
    return f'in fitness center {gim_id} trainer {coach_id} received some score'


@app.put('/fitness_center/<gim_id>/coach/<coach_id>/score')  # редагувати відгук про тренера
def update_trainer_score(gim_id, coach_id):
    return f'fitness center {gim_id} trainer {coach_id} score was update'


@app.get('/fitness_center/<gim_id>/services/')
def get_services(gim_id):
    res = get_from_db(f'select services* from service where id=1{gim_id}', False)
    return res


@app.get('/fitness_center/<gim_id>/services/<service_id>')
def get_service_info(gim_id, service_id):
    res = get_from_db(f'select name, description, price, max_attendees from service where id=1{gim_id} ,id=1{service_id}', False)
    return str(res)


@app.get('/fitness_center/<gim_id>/loyalty_programs')  # отримати інф
def get_loyalty_prog_info(gim_id): #???????????? де взяти інф
    res = get_from_db(f'select loyalty_programs from ????? where id=1{gim_id}', False)
    return  res

    # return f'fitness center {gim_id} has such loyalty program'

