from sqlalchemy.orm import Session
from models import Geography as GeographyModel, School as SchoolModel, Student as StudentModel, ScholasticYear as ScholasticYearModel, Class as ClassModel, Attendance as AttendanceModel, Enrolment as EnrolmentModel, Incident as IncidentModel, ClassEnrolment as ClassEnrolmentModel
from faker import Faker
from datetime import date, datetime, timezone, timedelta
import random

def get_random_past_datetime():
    """Helper function to generate random past datetime"""
    days_ago = random.randint(1, 365)
    return datetime.now(timezone.utc) - timedelta(days=days_ago)

def populate_data(db: Session):
    faker = Faker()
    now = datetime.now(timezone.utc)

    # Add Geography Data with random past created_at dates
    geographies = [
        {"city": "King's Landing", "region": "Crownlands", "created_at": get_random_past_datetime()},
        {"city": "Winterfell", "region": "The North", "created_at": get_random_past_datetime()},
        {"city": "Highgarden", "region": "The Reach", "created_at": get_random_past_datetime()},
        {"city": "Sunspear", "region": "Dorne", "created_at": get_random_past_datetime()},
        {"city": "Pyke", "region": "Iron Islands", "created_at": get_random_past_datetime()},
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