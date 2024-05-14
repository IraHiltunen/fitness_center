# /register[get, post]
# /login
# /user_info [get]
# /user_info/<id>/balance_of_services
# /user_info/<id>/balance_of_services/<add_services>
# /user_info/<id>/balance_of_services/<book_service>
# /user_info/<id>/balance_of_services/<book_off_services>
# /user_info/<id>/<add_personal_info>
# /fitness_center [get]
# /fitness_center/<id> [get]
# /fitness_center/<id>/loyalty_program[get]
# /fitness_center/<id>/trainer [get]
# /fitness_center/<id>/trainer/<trainer_id>[get]
# /fitness_center/<id>/trainer/<trainer_id>/<schedule>
# /fitness_center/<id>/trainer/<trainer_id>/<ranking>[get, post, put]
# /fitness_center/<id>/trainer/<trainer_id>/<reviews>
# /fitness_center/<id>/services[get]
# /fitness_center/<id>/services/<service_id> [get]
# /fitness_center/<id>/services/<service_id>/<schedule>
# /fitness_center/<id>/services/<service_id>/<duration_of_training>
# /fitness_center/<id>/services/<service_id>/<max_person>

# if __name__ == '__main__':
# host = '127.0.0.1'
# port = 8080
# app.run(host=host, port=port, debug=True)

# @app.route("/")
# def hel():
#     return "hi?ira"
#
#
# @app.route("/user/<id>")
# def show():
#     return f'user name{}'


# /login [get, post]
# /user [get, put, post]
# /user/funds [get, post] гроші подивитися, додати
# /user/reservations [get, post]
# /user/reservations/<reservation_id> [get, put, delete]
# /user/checkout [get, post, put]
# /fitness_center [get]
# /fitness_center/<id> [get]
# /fitness_center/<id>/trainer [get]
# /fitness_center/<id>/trainer/<trainer_id> [get]
# /fitness_center/<id>/trainer/<trainer_id>/rating [get, post, put]
# /fitness_center/<id>/services [get]
# /fitness_center/<id>/services/<service_id> [get]
# /register [get, post]
# /fitness_center/<id>/loyalty_programs [get]

# get - отримати(без параметрів) отримаємо дані цілком(повну інф)
# post - створити щось нове(з параметрами)
# put - відредагувати(з параметрами)
# delete - (без параметрів) просто видаляємо

from flask import Flask

app = Flask(__name__)


@app.get('/register')  # відображає форму
def user_register_invitation():
    return 'please, sigh in'


@app.post('/register')
def user_register():
    return 'new user registered'


@app.get('/login')
def user_login_form():
    return 'enter credentials'


@app.post('/login')
def user_login():
    return 'new user logged in'


@app.get('/user')
def user_info():
    return 'user inf'


@app.post('/user')
def add_user_info():
    return 'user data were modified'


@app.put('/user')  # яка різниця з пост
def user_update():
    return 'user inf was successfully update'


@app.get('/funds')
def user_deposit_info():
    return 'user inf'


@app.post('/funds')
def add_funds():
    return 'user account wes modified'


@app.get('/reservations')
def get_reservation_list():
    return 'reservation list'


@app.post('/reservations')
def add_reservation():
    return 'reservation was added'


@app.get('/user/reservations/<reservation_id>/')
def get_reservation_id(reservation_id):
    return f'info about {reservation_id}'


@app.put('/user/reservations/<reservation_id>/')
def update_reservation_id(reservation_id):
    return f'this {reservation_id} was updated'


@app.delete('/user/reservations/<reservation_id>/')
def delete_reservation_id(reservation_id):
    return f'this {reservation_id} was deleted'


@app.get('/checkout')
def get_checkout_box():
    return 'checkout box'


@app.post('/checkout')
def add_training():
    return 'training was added'


@app.put('/checkout')  # яка різниця пост і пут???????????????????????????
def update_box():
    return 'checkout_box was updated'


@app.get('/fitness_center')
def fitness_center_info():
    return 'fitness_center info'


@app.get('/fitness_center/<gim_id>')
def get_gim_id_info(gim_id):
    return f' info about {gim_id} '


@app.get('/fitness_center/<gim_id>/trainer/')
def get_trainers(gim_id):
    return f'fitness center {gim_id} trainers list'


@app.get('/fitness_center/<gim_id>/trainer/<trainer_id>')
def get_trainer_info(gim_id, trainer_id):
    return f'fitness center {gim_id}, {trainer_id} info'


@app.get('/fitness_center/<gim_id>/trainer/<trainer_id>/score')  # отримати інф
def get_trainer_score(gim_id, trainer_id):
    return f'fitness center {gim_id}, trainer {trainer_id} has score: '


@app.post('/fitness_center/<gim_id>/trainer/<trainer_id>/score')  # віддати інф про
def set_trainer_score(gim_id, trainer_id):
    return f'in fitness center {gim_id} trainer {trainer_id} received some score'


@app.put('/fitness_center/<gim_id>/trainer/<trainer_id>/score')
def update_trainer_score(gim_id, trainer_id):
    return f'fitness center {gim_id} trainer {trainer_id} score was update'


@app.get('/fitness_center/<gim_id>/services/')
def get_services(gim_id):
    return f'fitness center {gim_id} service list'


@app.get('/fitness_center/<gim_id>/services/<service_id>')
def get_service_info(gim_id, service_id):
    return f'fitness center {gim_id}, service {service_id} info'


@app.get('/fitness_center/<gim_id>/loyalty_programs')  # отримати інф
def get_loyalty_prog_info(gim_id):
    return f'fitness center {gim_id} has such loyalty program'
