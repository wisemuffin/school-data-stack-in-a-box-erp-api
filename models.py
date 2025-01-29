from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, timezone

Base = declarative_base()

class Geography(Base):
    __tablename__ = 'geography'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    region = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

class School(Base):
    __tablename__ = 'schools'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    geography_id = Column(Integer, ForeignKey('geography.id'))
    geography = relationship('Geography')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    socio_economic_status = Column(String)  # New column
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

class ScholasticYear(Base):
    __tablename__ = 'scholastic_year'
    id = Column(Integer, primary_key=True)
    year = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

class Class(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)
    subject = Column(String)  # New column
    name = Column(String)
    scholastic_year_id = Column(Integer, ForeignKey('scholastic_year.id'))
    scholastic_year = relationship('ScholasticYear')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

class Attendance(Base):
    __tablename__ = 'attendances'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    class_id = Column(Integer, ForeignKey('classes.id'))
    present = Column(Boolean)
    attendance_date = Column(Date)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

class Enrolment(Base):
    __tablename__ = 'enrolments'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    school_id = Column(Integer, ForeignKey('schools.id'))
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

class Incident(Base):
    __tablename__ = 'incidents'
    id = Column(Integer, primary_key=True)
    incident_type = Column(String)
    reported_datetime = Column(Date)
    student_id = Column(Integer, ForeignKey('students.id'))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

class ClassEnrolment(Base):
    __tablename__ = 'class_enrolments'
    id = Column(Integer, primary_key=True)
    enrolment_id = Column(Integer, ForeignKey('enrolments.id'))
    class_id = Column(Integer, ForeignKey('classes.id'))
    calendar_year = Column(Integer)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
