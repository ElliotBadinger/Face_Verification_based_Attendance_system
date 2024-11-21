# School Attendance System - POPIA Compliant Implementation

## Overview
A facial recognition-based student attendance system designed for real-time tracking through main school gate webcams, with comprehensive POPIA compliance and multi-user interface support.

## Key Features
- Real-time facial recognition processing
- POPIA (Protection of Personal Information Act) compliance
- Cultural considerations (e.g., hijab accommodation)
- Multi-user interface support
- Real-time notifications
- Secure data handling
- Audit logging

## Architecture

### Core Components
1. **FastAPI Backend**
   - Async support for better performance
   - JWT-based authentication
   - Role-based access control

2. **POPIA Compliance**
   - Consent management system
   - Data access logging
   - Privacy-preserving face data storage
   - Data retention policies

3. **Security Features**
   - Encrypted face data storage
   - Audit logging
   - Access control
   - Data privacy controls

4. **Database**
   - SQLAlchemy ORM
   - Migration support
   - Audit trails

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -e .
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize database:
```bash
python -m src.database init_db
```

5. Run the application:
```bash
uvicorn src.main:app --reload
```

## POPIA Compliance Features

### 1. Consent Management
- Explicit consent collection
- Consent withdrawal mechanism
- Cultural accommodation preferences
- Data retention preferences

### 2. Data Protection
- Encrypted face data storage
- Access control logging
- Data retention policies
- Privacy-preserving processing

### 3. Audit Trail
- Comprehensive logging
- Access tracking
- Data modifications
- Security events

### 4. Data Subject Rights
- Access request handling
- Data deletion mechanism
- Consent management
- Information correction

## Security Measures

### 1. Authentication
- JWT-based authentication
- Role-based access control
- MFA support
- Session management

### 2. Data Protection
- Face data encryption
- Secure key management
- Access logging
- Data isolation

### 3. System Security
- Rate limiting
- Input validation
- Error handling
- Security headers

## API Documentation

### Authentication Endpoints
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/refresh-token
- POST /api/auth/logout

### Student Management
- POST /api/students/
- GET /api/students/
- GET /api/students/{student_id}
- PUT /api/students/{student_id}
- DELETE /api/students/{student_id}

### Face Recognition
- POST /api/face/register
- POST /api/face/verify
- DELETE /api/face/remove

### POPIA Compliance
- POST /api/consent/record
- GET /api/consent/verify
- POST /api/consent/withdraw
- GET /api/data/access-request

## Development Guidelines

### Code Structure
```
src/
├── models/         # Database models
├── security/       # Security implementations
├── popia/          # POPIA compliance features
├── api/            # API endpoints
└── utils/          # Utility functions
```

### Best Practices
1. Always encrypt sensitive data
2. Log all data access
3. Validate cultural considerations
4. Implement proper error handling
5. Follow POPIA guidelines

## Testing

Run tests:
```bash
pytest
```

## Deployment

1. Set up production environment
2. Configure secure database
3. Enable HTTPS
4. Set up monitoring
5. Configure backups

## Contributing

1. Follow coding standards
2. Add tests for new features
3. Update documentation
4. Submit pull requests

## License
MIT License

## Support
Contact the development team for support.
