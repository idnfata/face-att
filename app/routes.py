from app import app
from app.controller import FaceController, AttendanceController, OvertimeController
from flask import request

@app.route('/')
def index():
    return 'Face Recognition API'

@app.route('/is-has-face-stored/<client_id>/<employee_id>', methods=['GET'])
def hasFaceStored(client_id, employee_id):
    return FaceController.isUserHasFaceStored(client_id, employee_id)

@app.route('/attendances/<employee_id>/<date>/', methods=['GET'])
def attendances(employee_id, date):
    return AttendanceController.index(employee_id, date)


@app.route('/employee/attendance', methods=['POST', 'PUT'])
def EmployeeAttendance():
    if request.method == 'POST':
        return AttendanceController.addTimeIn()
    else:
        return AttendanceController.addTimeOut()

@app.route('/employee/overtime', methods=['POST', 'PUT'])
def EmployeeOvertime():
    if request.method == 'POST':
        return OvertimeController.addTimeIn()
    else:
        return OvertimeController.addTimeOut()

@app.route('/recognize-face', methods=['POST'])
def recognizeFace():
    return FaceController.recognizeFace()

@app.route('/save-face', methods=['POST'])
def saveFace():
    return FaceController.saveFace()

@app.route('/train-face/<client_id>', methods=['GET'])
def trainFace(client_id):
    return FaceController.trainFace(client_id)

app.run(debug=True)
