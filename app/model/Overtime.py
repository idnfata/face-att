from app import db
from sqlalchemy.ext.automap import automap_base

Base = automap_base()
Base.prepare(db.engine, reflect=True)
OvertimeAttendances = Base.classes.employee_overtime_attendances
