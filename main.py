from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Base, Geography as GeographyModel, School as SchoolModel, Student as StudentModel, ScholasticYear as ScholasticYearModel, Class as ClassModel, Attendance as AttendanceModel, Enrolment as EnrolmentModel, Incident as IncidentModel, ClassEnrolment as ClassEnrolmentModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List
from schemas import Geography, GeographyCreate, School, SchoolCreate, Student, StudentCreate, ScholasticYear, ScholasticYearCreate, Class, ClassCreate, Attendance, AttendanceCreate, Enrolment, EnrolmentCreate, Incident, IncidentCreate, ClassEnrolment, ClassEnrolmentCreate
from faker import Faker
from datetime import date
import random

# Create a SQLite database
engine = create_engine('sqlite:///mock_school.db')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

# FastAPI application
app = FastAPI()

# Dependency to get the session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def populate_data():
    db = SessionLocal()
    faker = Faker()

    # Clear existing data
    db.query(GeographyModel).delete()
    db.query(SchoolModel).delete()
    db.query(StudentModel).delete()
    db.query(ScholasticYearModel).delete()
    db.query(ClassModel).delete()
    db.query(EnrolmentModel).delete()
    db.query(ClassEnrolmentModel).delete()
    db.query(AttendanceModel).delete()
    db.query(IncidentModel).delete()

    # Add Geography Data
    geographies = [
        {"city": "King's Landing", "region": "Crownlands"},
        {"city": "Winterfell", "region": "The North"},
        {"city": "Highgarden", "region": "The Reach"},
        {"city": "Sunspear", "region": "Dorne"},
        {"city": "Pyke", "region": "Iron Islands"},
    ]

    geo_objects = [GeographyModel(**geo) for geo in geographies]
    db.add_all(geo_objects)
    db.commit()

    # Add Schools
    schools = [
        {"name": "King's Landing Elementary School", "geography_id": geo_objects[0].id},
        {"name": "Winterfell High School", "geography_id": geo_objects[1].id},
        {"name": "Highgarden Comprehensive School", "geography_id": geo_objects[2].id},
    ]

    school_objects = [SchoolModel(**school) for school in schools]
    db.add_all(school_objects)
    db.commit()

    # Assign socio-economic status and add Students
    ses_options = ["High", "Medium", "Low"]
    students = [StudentModel(first_name=faker.first_name(), last_name=faker.last_name(), socio_economic_status=random.choice(ses_options)) for _ in range(100)]
    db.add_all(students)
    db.commit()

    # Add Scholastic Years and Classes
    years = ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
    subjects = ["English", "Maths", "Science"]
    year_objects = [ScholasticYearModel(year=year) for year in years]
    db.add_all(year_objects)
    db.commit()

    class_objects = []
    for year_obj in year_objects:
        for subject in subjects:
            class_name = f"{subject} {year_obj.year}"
            class_obj = ClassModel(subject=subject, name=class_name, scholastic_year_id=year_obj.id)
            class_objects.append(class_obj)
    db.add_all(class_objects)
    db.commit()

    # Add Enrolments
    for student in students:
        enrolment_start = faker.date_between(start_date='-6y', end_date='-1y')
        enrolment_end = faker.date_between(start_date='-1y', end_date='today') if random.random() > 0.8 else None
        school_id = random.choice(school_objects).id
        enrolment = EnrolmentModel(student_id=student.id, school_id=school_id, start_date=enrolment_start, end_date=enrolment_end)
        db.add(enrolment)
        db.commit()

        # Calculate the number of years the student is enrolled 
        num_years_enrolled = (enrolment.end_date or date.today()).year - enrolment.start_date.year + 1

        # Enrol each student in classes based on the number of years enrolled 
        for i in range(num_years_enrolled): 
            if i >= len(years): 
                break 
            for subject in ["English", "Maths", "Science"]: 
                class_name = f"{subject} {years[i]}" 
                class_obj = db.query(ClassModel).filter(ClassModel.name == class_name).first() 
                class_enrolment = ClassEnrolmentModel(enrolment_id=enrolment.id, class_id=class_obj.id, calendar_year=enrolment.start_date.year + i - 1) 
                db.add(class_enrolment)

    db.commit()

    # Add Attendances
    for enrolment in db.query(EnrolmentModel).all():
        for _ in range(10):
            attendance_date = faker.date_between(start_date=enrolment.start_date, end_date=enrolment.end_date or date.today())
            student = db.query(StudentModel).filter(StudentModel.id == enrolment.student_id).first()
            if student.socio_economic_status == "Low":
                present = random.random() < 0.2  # Lower attendance rate
            elif student.socio_economic_status == "Medium":
                present = random.random() < 0.1  # Lower attendance rate
            else:
                present = random.choice([True, False])
            attendance = AttendanceModel(student_id=enrolment.student_id, class_id=random.choice(class_objects).id, present=present, attendance_date=attendance_date)
            db.add(attendance)
    db.commit()

    # Add Incidents
    for _ in range(50):
        incident_date = faker.date_between(start_date='-6y', end_date='today')
        student = random.choice(students)
        if student.socio_economic_status == "Low":
            incident_multiplier = 3 
        elif student.socio_economic_status == "Medium":
            incident_multiplier = 2
        else:
            incident_multiplier = 1
        for _ in range(incident_multiplier):
            incident = IncidentModel(incident_type=random.choice(["Poor Behaviour", "Injury"]), reported_datetime=incident_date, student_id=student.id)
            db.add(incident)
    db.commit()

@app.get("/geographies/", response_model=List[Geography])
def read_geographies(db: Session = Depends(get_db)):
    return db.query(GeographyModel).all()

@app.post("/geographies/", response_model=Geography)
def create_geography(geo: GeographyCreate, db: Session = Depends(get_db)):
    geography = GeographyModel(**geo.dict())
    db.add(geography)
    db.commit()
    db.refresh(geography)
    return geography

@app.get("/schools/", response_model=List[School])
def read_schools(db: Session = Depends(get_db)):
    return db.query(SchoolModel).all()

@app.post("/schools/", response_model=School)
def create_school(school: SchoolCreate, db: Session = Depends(get_db)):
    school = SchoolModel(**school.dict())
    db.add(school)
    db.commit()
    db.refresh(school)
    return school

@app.get("/students/", response_model=List[Student])
def read_students(db: Session = Depends(get_db)):
    return db.query(StudentModel).all()

@app.post("/students/", response_model=Student)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    student = StudentModel(**student.dict())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@app.get("/classes/", response_model=List[Class])
def read_classes(db: Session = Depends(get_db)):
    return db.query(ClassModel).all()

@app.post("/classes/", response_model=Class)
def create_class(class_: ClassCreate, db: Session = Depends(get_db)):
    class_ = ClassModel(**class_.dict())
    db.add(class_)
    db.commit()
    db.refresh(class_)
    return class_

@app.get("/attendances/", response_model=List[Attendance])
def read_attendances(db: Session = Depends(get_db)):
    return db.query(AttendanceModel).all()

@app.post("/attendances/", response_model=Attendance)
def create_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    attendance = AttendanceModel(**attendance.dict())
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance

@app.post("/reset/")
def reset_state():
    global session
    session.close()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    return {"message": "State reset successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
