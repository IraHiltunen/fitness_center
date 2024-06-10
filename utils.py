import datetime

from fitness import SQLiteDatabase
from utils


def clac_slots(coach_id, service_id, desired_date):
    query = (f'select * from reservation'
             f'join service on service.id = reservation.service_id'
             f'where coach_id = {coach_id}')

    with SQLiteDatabase('db.db') as db:
        booked_time = db.select_method("reservation", {"coach_id": coach_id}, join={'service': 'service_id = reservation.service_id'}, fetchall=True)
        coach_schedule = db.select_method("coach_schedule", {"coach_id": coach_id}, "date": "31.05.2024"}, fetchall=False)
        coach_capacity = db.select_method("coach_service", {"coach_id": coach_id}, "service_id": service_id}, fetchall=False)
        service_info = db.select_method('service', {'service_id': id})

        start_dtime = datetime.datetime.strptime(coach_schedule["date"]+' '+coach_schedule["start_time"], '%d.%m.%Y %H:%M')
        end_dtime = datetime.datetime.strptime(coach_schedule["date"] + ' ' + coach_schedule["start_time"], '%d.%m.%Y %H:%M')
        current_dtime = start_dtime
        coach_schedule = {}
        while current_dtime < end_dtime:
            coach_schedule[current_dtime] = coach_capacity['capacity']
            current_dtime = current_dtime + datetime.timedelta(minutes=15)
        for one_booking in booked_time:
            booking_date = one_booking["date"]
            booking_time = one_booking["time"]
            booking_duration = one_booking["duration"]
            one_booking_start = datetime.datetime.strptime(booking_date+' ' + booked_time, '%d.%m.%Y %H:%M')
            booking_end = one_booking_start + datetime.timedelta(minutes=booking_duration)
            current_dtime = one_booking_start
            while current_dtime < booking_end:
                coach_schedule[current_dtime] -= 1
                current_dtime = current_dtime + datetime.timedelta(minutes=15)
        result_times = []
        service_duration = service_info['duration']
        service_start_time = start_dtime
        while service_start_time < end_dtime :
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
        return  result_times



    print('')

clac_slots(1,1,2)

