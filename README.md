# Running the API server

## option 1 (recommended)
```bash
uv run main.py  # will create an virutal 
```

1. will create an virutal enviroment
2. then uv installs dependancies
3. then uv  generates the mock data in sqllite and then runs the fastapi sever


### Outputs
Server started at http://127.0.0.1:8000
Documentation at http://127.0.0.1:8000/docs

## option 2

```bash
fastapi dev main.py  
```



# viewing data with duckdb
```bash
duckdb ./mock_school_analytic.db
```

```sql
INSTALL sqlite;
LOAD sqlite;


ATTACH 'mock_school.db' (TYPE SQLITE);
USE mock_school;

from schools;
```

### analytical queries

analytical sql queries to show how many students were enrolled each year for each school

```sql
SELECT 
    sch.name AS SchoolName,
    strftime('%Y', en.start_date) AS EnrolmentYear,
    COUNT(DISTINCT en.student_id) AS TotalStudents
FROM 
    enrolments en
JOIN 
    students st ON en.student_id = st.id
JOIN 
    schools sch ON sch.id = en.school_id -- Assuming there's a school_id in students table
GROUP BY 
    sch.name, EnrolmentYear
ORDER BY 
    sch.name, EnrolmentYear;
```

sql query that shows the students at a school and a row for each scholastic year they were at the school. order the rows by student then by enrolment date.

```sql
SELECT 
    st.id AS StudentID,
    st.first_name AS FirstName,
    st.last_name AS LastName,
    sch.name AS SchoolName,
    sy.year AS ScholasticYear,
    cls.name AS className,
    ce.calendar_year,
    en.start_date AS EnrolmentStartDate,
    en.end_date AS EnrolmentEndDate
FROM 
    students st
JOIN 
    enrolments en ON st.id = en.student_id
JOIN 
    schools sch ON en.school_id = sch.id
JOIN 
    class_enrolments ce ON en.id = ce.enrolment_id
JOIN 
    classes cls ON ce.class_id = cls.id
JOIN 
    scholastic_year sy ON cls.scholastic_year_id = sy.id
ORDER BY 
    st.id, ce.calendar_year;
```

# Entitity Relationship diagram

```mermaid
erDiagram
    Geography {
        int id PK
        string city
        string region
    }

    School {
        int id PK
        string name
        int geography_id FK
    }

    Student {
        int id PK
        string first_name
        string last_name
    }

    ScholasticYear {
        int id PK
        string year
    }

    Class {
        int id PK
        string name
        int scholastic_year_id FK
    }

    Attendance {
        int id PK
        int student_id FK
        int class_id FK
        boolean present
        date attendance_date
    }

    Enrolment {
        int id PK
        int student_id FK
        date start_date
        date end_date
    }

    Incident {
        int id PK
        string incident_type
        date reported_datetime
        int student_id FK
    }

    ClassEnrolment {
        int id PK
        int enrolment_id FK
        int class_id FK
    }

    Geography ||--o{ School: has
    School ||--o{ Student: has
    ScholasticYear ||--o{ Class: has
    Student ||--o{ Attendance: attends
    Class ||--o{ Attendance: has
    Student ||--o{ Enrolment: enrolled_in
    Enrolment ||--o{ ClassEnrolment: maps_to
    Class ||--o{ ClassEnrolment: has
    Student ||--o{ Incident: involved_in
```