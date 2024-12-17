from pydantic import BaseModel
from datetime import date, datetime
from typing import Generic, List, Optional, TypeVar
from pydantic.generics import GenericModel

class GeographyBase(BaseModel):
    city: str
    region: str

class GeographyCreate(GeographyBase):
    pass

class Geography(GeographyBase):
    id: int

    class Config:
        from_attributes = True

class SchoolBase(BaseModel):
    name: str
    geography_id: int

class SchoolCreate(SchoolBase):
    pass

class School(SchoolBase):
    id: int

    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    first_name: str
    last_name: str

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True

class ScholasticYearBase(BaseModel):
    year: str

class ScholasticYearCreate(ScholasticYearBase):
    pass

class ScholasticYear(ScholasticYearBase):
    id: int

    class Config:
        from_attributes = True

class ClassBase(BaseModel):
    name: str
    scholastic_year_id: int

class ClassCreate(ClassBase):
    pass

class Class(ClassBase):
    id: int

    class Config:
        from_attributes = True

class AttendanceBase(BaseModel):
    student_id: int
    class_id: int
    present: bool
    attendance_date: date

class AttendanceCreate(AttendanceBase):
    pass

class Attendance(AttendanceBase):
    id: int

    class Config:
        from_attributes = True

class EnrolmentBase(BaseModel):
    student_id: int
    start_date: date
    end_date: Optional[date]

class EnrolmentCreate(EnrolmentBase):
    pass

class Enrolment(EnrolmentBase):
    id: int

    class Config:
        from_attributes = True

class IncidentBase(BaseModel):
    incident_type: str
    reported_datetime: datetime
    student_id: int

class IncidentCreate(IncidentBase):
    pass

class Incident(IncidentBase):
    id: int

    class Config:
        from_attributes = True

class ClassEnrolmentBase(BaseModel):
    enrolment_id: int
    class_id: int

class ClassEnrolmentCreate(ClassEnrolmentBase):
    pass

class ClassEnrolment(ClassEnrolmentBase):
    id: int

    class Config:
        from_attributes = True


# Define a generic type variable 
T = TypeVar('T') 

class PaginatedResponse(GenericModel, Generic[T]): 
    items: List[T] 
    total: int 
    next: Optional[str] = None