from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import Base, Geography as GeographyModel, School as SchoolModel, Student as StudentModel, ScholasticYear as ScholasticYearModel, Class as ClassModel, Attendance as AttendanceModel, Enrolment as EnrolmentModel, Incident as IncidentModel, ClassEnrolment as ClassEnrolmentModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from schemas import Geography, GeographyCreate, School, SchoolCreate, Student, StudentCreate, ScholasticYear, ScholasticYearCreate, Class, ClassCreate, Attendance, AttendanceCreate, Enrolment, EnrolmentCreate, Incident, IncidentCreate, ClassEnrolment, ClassEnrolmentCreate, PaginatedResponse
from data_generation import populate_data  # Import the data generation function

# Create a SQLite database
engine = create_engine('sqlite:///mock_school.db')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

# FastAPI application
app = FastAPI()

# Allow all origins for simplicity, you can restrict this to specific origins if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # List of allowed methods
    allow_headers=["*"],  # List of allowed headers
)

# Dependency to get the session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    populate_data(db)  # Call the data generation function

@app.get("/geographies/", response_model=PaginatedResponse[Geography])
def read_geographies(
    db: Session = Depends(get_db),
    page: Optional[int] = Query(None, description="Page number (only use one of page or offset)"),
    limit: int = Query(10, description="Number of geographies to retrieve"),
    offset: Optional[int] = Query(None, description="Number of geographies to skip (only use one of page or offset)"),
    sort: Optional[str] = Query(None, description="Field to sort by"),
    order: Optional[str] = Query(None, description="Sort order (asc or desc)")
):
    if offset is not None:
        current_offset = offset
    else:
        current_offset = (page - 1) * limit if page else 0

    query = db.query(GeographyModel)

    # Apply sorting
    if sort:
        sort_column = getattr(GeographyModel, sort, None)
        if sort_column:
            if order == "desc":
                sort_column = sort_column.desc()
            query = query.order_by(sort_column)

    geographies = query.offset(current_offset).limit(limit).all()
    total = db.query(GeographyModel).count()

    next_offset = current_offset + limit if current_offset + limit < total else None
    next_url = f"/geographies/?limit={limit}&offset={next_offset}" if next_offset else None
    
    return PaginatedResponse[Geography](items=geographies, total=total, next=next_url)

@app.post("/geographies/", response_model=Geography)
def create_geography(geo: GeographyCreate, db: Session = Depends(get_db)):
    geography = GeographyModel(**geo.dict())
    db.add(geography)
    db.commit()
    db.refresh(geography)
    return geography

@app.delete("/geographies/{geography_id}", response_model=Geography)
def delete_geography(geography_id: int, db: Session = Depends(get_db)):
    geography = db.query(GeographyModel).filter(GeographyModel.id == geography_id).first()
    
    if not geography:
        raise HTTPException(status_code=404, detail="Geography not found")
    
    db.delete(geography)
    db.commit()
    return geography

@app.get("/schools/", response_model=PaginatedResponse[School])
def read_schools(
    db: Session = Depends(get_db),
    page: Optional[int] = Query(None, description="Page number (only use one of page or offset)"),
    limit: int = Query(10, description="Number of schools to retrieve"),
    offset: Optional[int] = Query(None, description="Number of schools to skip (only use one of page or offset)"),
    sort: Optional[str] = Query(None, description="Field to sort by"),
    order: Optional[str] = Query(None, description="Sort order (asc or desc)")
):
    if offset is not None:
        current_offset = offset
    else:
        current_offset = (page - 1) * limit if page else 0

    query = db.query(SchoolModel)

    # Apply sorting
    if sort:
        sort_column = getattr(SchoolModel, sort, None)
        if sort_column:
            if order == "desc":
                sort_column = sort_column.desc()
            query = query.order_by(sort_column)

    schools = query.offset(current_offset).limit(limit).all()
    total = db.query(SchoolModel).count()

    next_offset = current_offset + limit if current_offset + limit < total else None
    next_url = f"/schools/?limit={limit}&offset={next_offset}" if next_offset else None
    
    return PaginatedResponse[School](items=schools, total=total, next=next_url)

@app.post("/schools/", response_model=School)
def create_school(school: SchoolCreate, db: Session = Depends(get_db)):
    school = SchoolModel(**school.dict())
    db.add(school)
    db.commit()
    db.refresh(school)
    return school

@app.delete("/schools/{school_id}", response_model=School)
def delete_school(school_id: int, db: Session = Depends(get_db)):
    school = db.query(SchoolModel).filter(SchoolModel.id == school_id).first()
    
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    db.delete(school)
    db.commit()
    return school

@app.get("/students/", response_model=PaginatedResponse[Student])
def read_students(
    db: Session = Depends(get_db),
    page: Optional[int] = Query(None, description="Page number (only use one of page or offset)"),
    limit: int = Query(10, description="Number of students to retrieve"),
    offset: Optional[int] = Query(None, description="Number of students to skip (only use one of page or offset)"),
    sort: Optional[str] = Query(None, description="Field to sort by"),
    order: Optional[str] = Query(None, description="Sort order (asc or desc)")
):
    if offset is not None:
        current_offset = offset
    else:
        current_offset = (page - 1) * limit if page else 0
        
    query = db.query(StudentModel)

    # Apply sorting
    if sort:
        sort_column = getattr(StudentModel, sort, None)
        if sort_column:
            if order == "desc":
                sort_column = sort_column.desc()
            query = query.order_by(sort_column)

    students = query.offset(current_offset).limit(limit).all()
    total = db.query(StudentModel).count()

    next_offset = current_offset + limit if current_offset + limit < total else None
    next_url = f"/students/?limit={limit}&offset={next_offset}" if next_offset else None
    
    return PaginatedResponse[Student](items=students, total=total, next=next_url)

@app.post("/students/", response_model=Student)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    student = StudentModel(**student.dict())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@app.delete("/students/{student_id}", response_model=Student)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(student)
    db.commit()
    return student

@app.get("/classes/", response_model=PaginatedResponse[Class])
def read_classes(
    db: Session = Depends(get_db),
    page: Optional[int] = Query(None, description="Page number (only use one of page or offset)"),
    limit: int = Query(10, description="Number of classes to retrieve"),
    offset: Optional[int] = Query(None, description="Number of classes to skip (only use one of page or offset)"),
    sort: Optional[str] = Query(None, description="Field to sort by"),
    order: Optional[str] = Query(None, description="Sort order (asc or desc)")
):
    if offset is not None:
        current_offset = offset
    else:
        current_offset = (page - 1) * limit if page else 0

    query = db.query(ClassModel)

    # Apply sorting
    if sort:
        sort_column = getattr(ClassModel, sort, None)
        if sort_column:
            if order == "desc":
                sort_column = sort_column.desc()
            query = query.order_by(sort_column)

    classes = query.offset(current_offset).limit(limit).all()
    total = db.query(ClassModel).count()

    next_offset = current_offset + limit if current_offset + limit < total else None
    next_url = f"/classes/?limit={limit}&offset={next_offset}" if next_offset else None
    
    return PaginatedResponse[Class](items=classes, total=total, next=next_url)

@app.post("/classes/", response_model=Class)
def create_class(class_: ClassCreate, db: Session = Depends(get_db)):
    class_ = ClassModel(**class_.dict())
    db.add(class_)
    db.commit()
    db.refresh(class_)
    return class_

@app.delete("/classes/{class_id}", response_model=Class)
def delete_class(class_id: int, db: Session = Depends(get_db)):
    class_ = db.query(ClassModel).filter(ClassModel.id == class_id).first()
    
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    
    db.delete(class_)
    db.commit()
    return class_

@app.get("/attendances/", response_model=PaginatedResponse[Attendance])
def read_attendances(
    db: Session = Depends(get_db),
    page: Optional[int] = Query(None, description="Page number (only use one of page or offset)"),
    limit: int = Query(10, description="Number of attendances to retrieve"),
    offset: Optional[int] = Query(None, description="Number of attendances to skip (only use one of page or offset)"),
    sort: Optional[str] = Query(None, description="Field to sort by"),
    order: Optional[str] = Query(None, description="Sort order (asc or desc)")
):
    if offset is not None:
        current_offset = offset
    else:
        current_offset = (page - 1) * limit if page else 0

    query = db.query(AttendanceModel)

    # Apply sorting
    if sort:
        sort_column = getattr(AttendanceModel, sort, None)
        if sort_column:
            if order == "desc":
                sort_column = sort_column.desc()
            query = query.order_by(sort_column)

    attendances = query.offset(current_offset).limit(limit).all()
    total = db.query(AttendanceModel).count()

    next_offset = current_offset + limit if current_offset + limit < total else None
    next_url = f"/attendances/?limit={limit}&offset={next_offset}" if next_offset else None
    
    return PaginatedResponse[Attendance](items=attendances, total=total, next=next_url)

@app.post("/attendances/", response_model=Attendance)
def create_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    attendance = AttendanceModel(**attendance.dict())
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance

@app.delete("/attendances/{attendance_id}", response_model=Attendance)
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)):
    attendance = db.query(AttendanceModel).filter(AttendanceModel.id == attendance_id).first()
    
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    
    db.delete(attendance)
    db.commit()
    return attendance

@app.get("/enrolments/", response_model=PaginatedResponse[Enrolment])
def read_enrolments(
    db: Session = Depends(get_db),
    page: Optional[int] = Query(None, description="Page number (only use one of page or offset)"),
    limit: int = Query(10, description="Number of enrolments to retrieve"),
    offset: Optional[int] = Query(None, description="Number of enrolments to skip (only use one of page or offset)"),
    sort: Optional[str] = Query(None, description="Field to sort by"),
    order: Optional[str] = Query(None, description="Sort order (asc or desc)")
):
    if offset is not None:
        current_offset = offset
    else:
        current_offset = (page - 1) * limit if page else 0

    query = db.query(EnrolmentModel)

    # Apply sorting
    if sort:
        sort_column = getattr(EnrolmentModel, sort, None)
        if sort_column:
            if order == "desc":
                sort_column = sort_column.desc()
            query = query.order_by(sort_column)

    enrolments = query.offset(current_offset).limit(limit).all()
    total = db.query(EnrolmentModel).count()

    next_offset = current_offset + limit if current_offset + limit < total else None
    next_url = f"/enrolments/?limit={limit}&offset={next_offset}" if next_offset else None
    
    return PaginatedResponse[Enrolment](items=enrolments, total=total, next=next_url)

@app.post("/enrolments/", response_model=Enrolment)
def create_enrolment(enrolment: EnrolmentCreate, db: Session = Depends(get_db)):
    enrolment = EnrolmentModel(**enrolment.dict())
    db.add(enrolment)
    db.commit()
    db.refresh(enrolment)
    return enrolment

@app.delete("/enrolments/{enrolment_id}", response_model=Enrolment)
def delete_enrolment(enrolment_id: int, db: Session = Depends(get_db)):
    enrolment = db.query(EnrolmentModel).filter(EnrolmentModel.id == enrolment_id).first()
    
    if not enrolment:
        raise HTTPException(status_code=404, detail="Enrolment not found")
    
    db.delete(enrolment)
    db.commit()
    return enrolment

@app.get("/incidents/", response_model=PaginatedResponse[Incident])
def read_incidents(
    db: Session = Depends(get_db),
    page: Optional[int] = Query(None, description="Page number (only use one of page or offset)"),
    limit: int = Query(10, description="Number of incidents to retrieve"),
    offset: Optional[int] = Query(None, description="Number of incidents to skip (only use one of page or offset)"),
    sort: Optional[str] = Query(None, description="Field to sort by"),
    order: Optional[str] = Query(None, description="Sort order (asc or desc)")
):
    if offset is not None:
        current_offset = offset
    else:
        current_offset = (page - 1) * limit if page else 0

    query = db.query(IncidentModel)

    # Apply sorting
    if sort:
        sort_column = getattr(IncidentModel, sort, None)
        if sort_column:
            if order == "desc":
                sort_column = sort_column.desc()
            query = query.order_by(sort_column)

    incidents = query.offset(current_offset).limit(limit).all()
    total = db.query(IncidentModel).count()

    next_offset = current_offset + limit if current_offset + limit < total else None
    next_url = f"/incidents/?limit={limit}&offset={next_offset}" if next_offset else None
    
    return PaginatedResponse[Incident](items=incidents, total=total, next=next_url)

@app.post("/incidents/", response_model=Incident)
def create_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    incident = IncidentModel(**incident.dict())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident

@app.delete("/incidents/{incident_id}", response_model=Incident)
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(IncidentModel).filter(IncidentModel.id == incident_id).first()
    
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    db.delete(incident)
    db.commit()
    return incident

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
