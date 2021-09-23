from app.model.Attendance import Attendance, OvertimeAttendance, OvertimeRequest, Employee, Division, Group, Position #import table
from app.controller.FaceController import recogFace, saveAttFace
from app import response, app, db
from flask import request, jsonify, abort
import math, calendar, datetime

def index(employee_id, date): #get employee attendances
    try:
        # return "division id " + str(division_id) + " group_id " + str(group_id)
        date = date.split("-")
        year = int(date[0])
        month = int(date[1])
        num_days = calendar.monthrange(year, month)[1]
        first_day = datetime.date(year, month, 1)
        last_day = datetime.date(year, month, num_days)

        attendances = db.session.query(Attendance).filter(Attendance.employee_id==employee_id).filter(Attendance.date.between(first_day, last_day)).all()
      
        
        if len(attendances): # ada datanya
            data = formatarray(attendances)
            # print(data)
            return response.successWithData(data, "data kehadiran")
        else: # tidak ada datanya
            return response.NotFound("Data tidak ditemukan")
        
    except Exception as e:
        print(e)
        return response.NotFound("Data tidak ditemukan.")




def formatarray(datas):
    array = []

    for i in datas:
        array.append(singleObject(i))
    
    return array

def singleObject(data):
    data = {
        'id': data.id,
        'client_id': data.client_id,
        'employee_id': data.employee_id,
        'date': data.date.strftime('%Y-%m-%d'),
        'time_in_schedule': data.time_in_schedule,
        'late_tolerance': data.late_tolerance,
        'time_out_schedule': data.time_out_schedule,
        'lng_schedule': data.lng_schedule,
        'lat_schedule': data.lat_schedule,
        'time_in': data.time_in,
        'time_out': data.time_out,
        'time_out': data.time_out,
        'time_break_start': data.time_break_start,
        'break_duration': data.break_duration,
        'time_in_lng': data.time_in_lng,
        'time_in_lat': data.time_in_lat,
        'time_in_img': data.time_in_img,
        'time_out_lng': data.time_out_lng,
        'time_out_lat': data.time_out_lat,
        'time_out_img': data.time_out_img,
        'is_late': data.is_late,
        'is_out_early': data.is_out_early,
        'is_overtime': data.is_overtime,
        'attendance_status': data.attendance_status,
        'created_at': data.created_at,
        'updated_at': data.updated_at,
    }

    return data

def addTimeIn():
    try:
        data = request.get_json()
        client_id = data['client_id']
        employee_id = data['employee_id']
        date = data['date']
        time_in_schedule = data['time_in_schedule']
        late_tolerance = data['late_tolerance']
        time_out_schedule = data['time_out_schedule']
        lng_schedule = data['lng_schedule']
        lat_schedule = data['lat_schedule']
        time_in = data['time_in']
        time_break_start = data['time_break_start']
        break_duration = data['break_duration']
        time_in_lng = data['time_in_lng']
        time_in_lat = data['time_in_lat']
        time_in_img = data['time_in_img']
        is_late = data['is_late']
        attendance_status = 1
     
        dataWajah = recogFace(client_id, employee_id, time_in_img)
        if(dataWajah[1] == 401):
            return response.Unauthorized("Absen gagal, mohon untuk menggunakan wajah asli.")
        elif(dataWajah[1] == 404):
            return response.NotFound("Absen gagal, wajah tidak terdaftar.")
        else: 
            saveAttFace(client_id, employee_id, date, "schedules", "in", time_in_img)
            time_in = Attendance(client_id=client_id, employee_id=employee_id, date=date, time_in_schedule=time_in_schedule, late_tolerance=late_tolerance, time_out_schedule=time_out_schedule, lng_schedule=lng_schedule, lat_schedule=lat_schedule, time_in=time_in, time_break_start=time_break_start, break_duration=break_duration, time_in_lng=time_in_lng, time_in_lat=time_in_lat, time_in_img=1, is_late=is_late, attendance_status=attendance_status)
            db.session.add(time_in)
            db.session.commit()
            return response.success('Sukses Menambahkan Data Absen Masuk')
    except Exception as e:
        print(e)
        return response.NotFound("Absen gagal, pastikan wajah jelas.")


def addTimeOut():
    try:
        attendance_id = request.form.get('attendance_id')
        time_out = request.form.get('time_out')
        is_overtime = request.form.get('is_overtime')
        is_out_early = request.form.get('is_out_early')
        time_out_lng = request.form.get('time_out_lng')
        time_out_lat = request.form.get('time_out_lat')
        time_out_img = request.form.get('time_out_img')
        attendance = db.session.query(Attendance).filter_by(id=attendance_id).first()

        dataWajah = recogFace(attendance.client_id, attendance.employee_id, time_out_img)
        if(dataWajah[1] == 401):
            return response.Unauthorized("Absen gagal, mohon untuk menggunakan wajah asli.")
        elif(dataWajah[1] == 404):
            return response.NotFound("Absen gagal, wajah tidak terdaftar.")
        else: 
            saveAttFace(attendance.client_id, attendance.employee_id, str(attendance.date), "schedules", "out", time_out_img)


            attendance.time_out = time_out
            attendance.is_overtime = is_overtime
            attendance.is_out_early = is_out_early
            attendance.time_out_lng = time_out_lng
            attendance.time_out_lat = time_out_lat
            attendance.time_out_img = time_out_img

            db.session.commit()
            return response.success('Sukses Menambahkan Data Absen Pulang')
    except Exception as e:
        print(e)
        return "Gagal, periksa inputan"

# def detailReport():