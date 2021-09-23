from app.model.Attendance import Attendance, OvertimeAttendance, OvertimeRequest, Employee, Division, Group, Position #import table
from app.controller.FaceController import recogFace, saveAttFace
from app import response, app, db
from flask import request, jsonify, abort
import math, calendar, datetime

def addTimeIn():
    try:
        client_id = request.form.get('client_id')
        employee_id = request.form.get('employee_id')
        overtime_id = request.form.get('overtime_id')
        time_in = request.form.get('time_in')
        time_in_lng = request.form.get('time_in_lng')
        time_in_lat = request.form.get('time_in_lat')
        time_in_img = request.form.get('time_in_img')
        attendance_status = 1
  
        dataWajah = recogFace(client_id, employee_id, time_in_img)
        if(dataWajah[1] == 401):
            return response.Unauthorized("Absen gagal, mohon untuk menggunakan wajah asli.")
        elif(dataWajah[1] == 404):
            return response.NotFound("Absen gagal, wajah tidak terdaftar.")
        else: 
            saveAttFace(client_id, employee_id, date, "overtimes", 'in', time_in_img)
            time_in = OvertimeAttendances(client_id=client_id, employee_id=employee_id, overtime_id=overtime_id, time_in=time_in, time_in_lng=time_in_lng, time_in_lat=time_in_lat, time_in_img=1, attendance_status=attendance_status)
            db.session.add(time_in)
            db.session.commit()
            return response.success('Sukses Menambahkan Data Absen Masuk Lembur')
            # return response.successWithData(data, 'Sukses Menambahkan Data Absen Masuk')
    except Exception as e:
        print(e)
        return "Gagal, periksa inputan"

def addTimeOut():
    try:
        client_id = request.form.get('client_id')
        employee_id = request.form.get('employee_id')
        attendance_id = request.form.get('attendance_id')
        date = request.form.get('date')
        time_out = request.form.get('time_out')
        time_out_lng = request.form.get('time_out_lng')
        time_out_lat = request.form.get('time_out_lat')
        time_out_img = request.form.get('time_out_img')

        dataWajah = recogFace(client_id, employee_id, time_out_img)
        if(dataWajah[1] == 401):
            return response.Unauthorized("Absen gagal, mohon untuk menggunakan wajah asli.")
        elif(dataWajah[1] == 404):
            return response.NotFound("Absen gagal, wajah tidak terdaftar.")
        else: 
            saveAttFace(client_id, employee_id, date, "overtimes", 'out', time_out_img)
            
            attendance = db.session.query(OvertimeAttendances).filter_by(id=attendance_id).first()

            attendance.time_out = time_out
            attendance.time_out_lng = time_out_lng
            attendance.time_out_lat = time_out_lat
            attendance.time_out_img = time_out_img

            db.session.commit()
            return response.success('Sukses Menambahkan Data Absen Pulang Lembur')
        
    except Exception as e:
        print(e)
        return "Gagal, periksa inputan"


def index(employee_id, date): #get employee overtime attendances
    try:
        # return employee_id
        date = date.split("-")
        year = int(date[0])
        month = int(date[1])
        num_days = calendar.monthrange(year, month)[1]
        first_day = datetime.date(year, month, 1)
        last_day = datetime.date(year, month, num_days)
        # print(first_day)
        # print(last_day)
        attendances = db.session.query(Attendance).filter(Attendance.employee_id==employee_id).filter(Attendance.date.between(first_day, last_day)).all()

        overtime_requests = db.session.query(OvertimeRequest, OvertimeAttendance).outerjoin(OvertimeAttendance, OvertimeRequest.id == OvertimeAttendance.overtime_id).filter(OvertimeRequest.employee_id==employee_id).filter(OvertimeRequest.date.between(first_day, last_day)).all()



        # overtime_attendances = db.session.query(OvertimeRequest).outerjoin(OvertimeAttendance, OvertimeAttendance.overtime_id == OvertimeRequest.id, isouter=True).filter(OvertimeRequest.employee_id==employee_id).filter(OvertimeRequest.date.between(first_day, last_day)).all()
        # overtime_attendances = db.session.query(OvertimeRequest, OvertimeAttendance).select_from(OvertimeRequest).join(OvertimeAttendance, OvertimeAttendance.overtime_id == OvertimeRequest.id).all()
        print("overtime_requests")
        print(overtime_requests)
        for r in overtime_requests:
            print(r[0].id)
        # return ""
        if len(overtime_requests): # ada datanya
            data = formatarray(overtime_requests)
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
        array.append(singleObjectOvertimeAttendance(i))
    
    return array

def singleObjectOvertimeAttendance(data):
    data = {
        'id': data[0].id,
        'client_id': data[0].client_id,
        'employee_id': data[0].employee_id,
        'date': data[0].date.strftime('%Y-%m-%d'),
        'start_from': data[0].start_from,
        'late_tolerance': data[0].late_tolerance,
        'ends_on': data[0].ends_on,
        'overtime_location': data[0].overtime_location,
        'status': data[0].status,
        'desc': data[0].desc,
        'overtime_day_type': data[0].overtime_day_type,
        'paid_by': data[0].paid_by,
        'amount': data[0].amount,
        'approved_by': data[0].approved_by,
        'time_in': data[1].time_in if not(data[1] is None) else "",
        # 'time_out': data.time_out,
        # 'time_out': data.time_out,
        # 'time_break_start': data.time_break_start,
        # 'break_duration': data.break_duration,
        # 'time_in_lng': data.time_in_lng,
        # 'time_in_lat': data.time_in_lat,
        # 'time_in_img': data.time_in_img,
        # 'time_out_lng': data.time_out_lng,
        # 'time_out_lat': data.time_out_lat,
        # 'time_out_img': data.time_out_img,
        # 'attendance_status': data.attendance_status,
        # 'created_at': data.created_at,
        # 'updated_at': data.updated_at,
    }

    return data

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