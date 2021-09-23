from app import db
from sqlalchemy.ext.automap import automap_base

Base = automap_base()
Base.prepare(db.engine, reflect=True)
Attendance = Base.classes.attendances
OvertimeRequest = Base.classes.employee_overtime_requests
OvertimeAttendance = Base.classes.employee_overtime_attendances
Employee = Base.classes.employees
Division = Base.classes.divisions
Group = Base.classes.groups
Position = Base.classes.positions
