# School Attendance System
## Project Overview
A facial recognition-based student attendance system for real-time tracking of 496 students through main school gate webcams, with multi-user interface support for teachers, parents, and administrators.

### Key Technical Requirements
- Real-time facial recognition processing
- POPIA (Protection of Personal Information Act) compliance
- Support for cultural considerations (hijab accommodation)
- Multi-user interface (30+ teachers, parents, administrators)
- Real-time notifications
- Integration with school policies
- Scale: ~500 concurrent users

## Current Project Structure
```
school-attendance-system/
├── src/
│   ├── api/
│   ├── models/
│   │   ├── base.py
│   │   ├── user.py
│   │   └── student.py
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── tests/
│   ├── docs/
│   └── main.py
├── venv/
├── .env
├── requirements.txt
└── README.md
```

## Current Implementation Status

### Implemented Components
1. Basic project structure
2. Database models for Users and Students
3. FastAPI application setup
4. Basic CORS middleware configuration
5. Database connection setup with MySQL

### Core Dependencies
```python
fastapi
uvicorn
python-jose[cryptography]
passlib[bcrypt]
python-multipart
mysqlclient
sqlalchemy
python-dotenv
pydantic[email]
```

## Immediate Development Priorities

### 1. Authentication System
Status: Needs Implementation
Priority: High
Required Files:
- `src/api/auth.py`
- `src/schemas/auth_schema.py`
- `src/services/auth_service.py`

Key Features to Implement:
```python
# Required endpoints
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/refresh-token
- POST /api/auth/logout
```

### 2. Student Management
Status: Basic Models Created, Needs Full Implementation
Priority: High
Required Files:
- `src/api/students.py`
- `src/schemas/student_schema.py`
- `src/services/student_service.py`

Key Features to Implement:
```python
# Required endpoints
- POST /api/students/
- GET /api/students/
- GET /api/students/{student_id}
- PUT /api/students/{student_id}
- DELETE /api/students/{student_id}
```

### 3. Face Recognition Integration
Status: Not Started
Priority: Medium
Required Files:
- `src/services/face_recognition_service.py`
- `src/utils/image_processing.py`
- `src/schemas/face_data_schema.py`

Implementation Notes:
```python
# Key components needed
- Face detection preprocessing
- Face encoding storage
- Real-time matching algorithm
- Privacy-preserving data handling
```

## Database Schema Details

### Current Tables
1. users
2. students

### Pending Tables
```sql
-- Need to implement
CREATE TABLE face_data (
    id BINARY(16) PRIMARY KEY,
    student_id BINARY(16),
    encoded_data LONGBLOB,
    created_at DATETIME,
    valid_until DATETIME,
    is_active BOOLEAN
);

CREATE TABLE attendance (
    id BINARY(16) PRIMARY KEY,
    student_id BINARY(16),
    check_in_time DATETIME,
    check_out_time DATETIME,
    status VARCHAR(50),
    is_late BOOLEAN,
    late_slip_ref VARCHAR(100)
);

CREATE TABLE consents (
    id BINARY(16) PRIMARY KEY,
    student_id BINARY(16),
    face_recognition BOOLEAN,
    notifications BOOLEAN,
    valid_until DATETIME,
    guardian_signature VARCHAR(255)
);
```

## POPIA Compliance Checkpoints

### Current Implementation
- Basic database structure with privacy considerations

### Pending Implementation
1. Data Protection Measures
```python
# Required components
- Encryption at rest
- Secure data transmission
- Access logging
- Data retention policies
```

2. Consent Management
```python
# Required features
- Explicit consent collection
- Consent withdrawal mechanism
- Data access requests handling
- Data deletion workflow
```

## Next Implementation Steps

### 1. Authentication System
```python
# Priority implementation
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/register")
async def register_user():
    # Implement user registration
    pass

@router.post("/login")
async def login_user():
    # Implement user login
    pass
```

### 2. Data Validation Schemas
```python
# Priority implementation
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: str
```

### 3. Student Management API
```python
# Priority implementation
from fastapi import APIRouter, Depends
from typing import List

router = APIRouter()

@router.post("/")
async def create_student():
    # Implement student creation
    pass

@router.get("/")
async def list_students():
    # Implement student listing
    pass
```

## Testing Requirements

### Unit Tests
Required Files:
- `src/tests/test_auth.py`
- `src/tests/test_students.py`
- `src/tests/test_face_recognition.py`

### Integration Tests
Required Files:
- `src/tests/integration/test_attendance_flow.py`
- `src/tests/integration/test_notification_flow.py`

## Security Considerations

### Current Implementation
- Basic password hashing setup
- Session management structure

### Pending Implementation
1. Rate Limiting
2. JWT Token Management
3. Role-Based Access Control
4. Audit Logging

## Hardware Requirements

### Camera Setup
- HD Cameras (1080p minimum)
- Wide-angle coverage (120° minimum)
- Edge processing unit specifications

### Server Requirements
- CPU: 4+ cores
- RAM: 16GB minimum
- Storage: 500GB SSD minimum
- Network: 1Gbps minimum

## Learning Resources

### Core Technologies
1. FastAPI: https://fastapi.tiangolo.com/tutorial/
2. MySQL: https://dev.mysql.com/doc/refman/8.0/en/tutorial.html
3. SQLAlchemy: https://docs.sqlalchemy.org/en/14/tutorial/

### Additional Skills
1. Face Recognition: https://github.com/ageitgey/face_recognition
2. JWT Authentication: https://jwt.io/introduction
3. POPIA Compliance: https://popia.co.za/

## Development Timeline

### Phase 1 (Current Phase) - 4-6 weeks
- [x] Project structure setup
- [x] Basic database models
- [ ] Authentication system
- [ ] Basic API endpoints

### Phase 2 - 4-6 weeks
- [ ] Face recognition integration
- [ ] Privacy controls
- [ ] Data encryption

### Phase 3 - 6-8 weeks
- [ ] User interfaces
- [ ] Notification system
- [ ] Integration testing