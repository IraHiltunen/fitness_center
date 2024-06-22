import datetime
import sqlite3

from fitness import SQLiteDatabase
# from utils import


def dict_factory(cursor, row): # for 4 hometask?
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


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
        query = f"SELECT * FROM {table}"
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

    def fetch_one(self, table, condition=None, join_table=None, join_condition=None):
        # join_condition = {"fitness_center.id": "service.name"} specify table and field!!!
        # join_condition = {"{join table}" :{"fitness_center.id": "service.name"}}
        query = f"SELECT * FROM {table}"
        conditions = []

        if join_table is not None:
            join_cond_list = []
            for key, val in join_condition.items():
                join_cond_list.append(f"{key}='{val}'")
            join_cond_str = ' and '.join(join_cond_list)
            join_str = f' JOIN {join_table} ON {join_cond_str}'
            query = query + join_str

        if condition is not None:
            for key, val in condition.items():
                conditions.append(f"{key}='{val}'")
            str_conditions = " AND ".join(conditions)
            str_conditions = " WHERE " + str_conditions
            query = query + str_conditions

        cursor = self.connection.cursor()
        cursor.execute(query)
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


    def delete_data(self, table, condition): # todo this func подозреваю,что не правильно тут сделала
        conditions = []

        query = f"DELETE FROM {table}"

        if condition is not None:
            for key, val in condition.items():
                conditions.append(f"{key} = {val}")
            str_conditions = ' AND '.join(conditions)
            query = query + " WHERE " + str_conditions

        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()


    def edit_data(self, table, data, condition):
        updated_values = []
        conditions = []
        for key, value in data.items():
            updated_values.append(f"{key} = {value}")
        set_clause = ', '.join(updated_values) # set_clause- встановити вираз
        query = f"Update {table} Set {set_clause}"

        if condition is not None:
            for key, val in condition.items():
                conditions.append(f"{key} = {val}")
            str_conditions = ' And '.join(conditions)
            str_conditions = ' Where ' + str_conditions
            query = query + str_conditions

        cursor = self.connection.cursor
        cursor.execute(query)
        self.connection.commit()


def clac_slots(coach_id, service_id, desired_date): # (user_id, coach_id, service_id)
    query = (f'select * from reservation'# це як приклад, по чому ми це робимо
             f'join service on service.id = reservation.service_id'
             f'where coach_id = {coach_id}')

    with SQLiteDatabase('db.db') as db:
        booked_time = db.fetch_one("reservation", {"coach_id": coach_id, "date": "31.05.2024"},
                                   {'service': 'service_id = reservation.service_id'})
                                   # join={'service': 'service_id = reservation.service_id'})
                                    # чому тут джоін
        coach_schedule = db.fetch_one("coach_schedule", {"coach_id": coach_id},
                                      {"date": "31.05.2024"})
        coach_capacity = db.fetch_one("coach_services", {"coach_id": coach_id,
                                      "service_id": service_id})
        service_info = db.fetch_one('service', {'service_id': id})

        start_dtime = datetime.datetime.strptime(coach_schedule["date"] +
                                ' ' + coach_schedule["start_time"], '%d.%m.%Y %H:%M')
        end_dtime = datetime.datetime.strptime(coach_schedule["date"] +
                                ' ' + coach_schedule["end_time"], '%d.%m.%Y %H:%M')
        current_dtime = start_dtime
        coach_schedule = {}

        while current_dtime < end_dtime:
            coach_schedule[current_dtime] = coach_capacity['capacity'] # max capacity for coach
            current_dtime = current_dtime + datetime.timedelta(minutes=15)

        for one_booking in booked_time:
            booking_date = one_booking["date"]
            booking_time = one_booking["time"]
            booking_duration = one_booking["duration"]
            one_booking_start = datetime.datetime.strptime(booking_date+' ' + booking_time, '%d.%m.%Y %H:%M')
            booking_end = one_booking_start + datetime.timedelta(minutes=booking_duration)
            current_dtime = one_booking_start
            while current_dtime < booking_end:
                coach_schedule[current_dtime] -= 1
                current_dtime = current_dtime + datetime.timedelta(minutes=15)

        result_times = []
        service_duration = service_info['duration']
        service_start_time = start_dtime
        while service_start_time < end_dtime:
            service_end_time = service_start_time + datetime.timedelta(minutes=service_duration)
            everything_is_free = True
            iter_start_time = service_start_time
            while iter_start_time < service_end_time:

                if coach_schedule[iter_start_time] == 0 or service_end_time > end_dtime:
                    everything_is_free = False
                    break
                iter_start_time += datetime.timedelta(minutes=15)

            if everything_is_free:
                result_times.append(service_start_time)

            service_start_time += datetime.timedelta(minutes=15)
        final_result = [datetime.datetime.strptime(el, '%H:%M')for el in result_times]
        return result_times



    print('')

clac_slots(1,1,2)

