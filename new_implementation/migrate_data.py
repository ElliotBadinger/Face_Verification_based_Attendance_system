import os
import sys
import django
import logging
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_django():
    """Setup Django environment"""
    try:
        # Add the parent directory to Python path
        parent_dir = str(Path(__file__).resolve().parent.parent)
        sys.path.append(parent_dir)
        
        # Setup Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Attendence_System.settings')
        django.setup()
        logger.info("Django environment setup complete")
    except Exception as e:
        logger.error(f"Failed to setup Django environment: {str(e)}")
        sys.exit(1)

def setup_new_db():
    """Setup new database"""
    try:
        from src.database import init_db
        init_db()
        logger.info("New database initialized")
    except Exception as e:
        logger.error(f"Failed to initialize new database: {str(e)}")
        sys.exit(1)

def migrate_users():
    """Migrate user data"""
    try:
        from django.contrib.auth.models import User as DjangoUser
        from attendence_sys.models import Faculty
        from src.models.user import User, UserRole
        from src.database import get_db
        
        with get_db() as db:
            # Migrate faculty users
            faculties = Faculty.objects.all()
            for faculty in faculties:
                django_user = faculty.user
                new_user = User(
                    email=django_user.email,
                    hashed_password="needs_reset",  # Require password reset
                    first_name=faculty.firstname,
                    last_name=faculty.lastname,
                    role=UserRole.TEACHER,
                    phone_number=faculty.phone,
                    requires_password_change=True
                )
                db.add(new_user)
            
            db.commit()
            logger.info("Users migrated successfully")
    except Exception as e:
        logger.error(f"Failed to migrate users: {str(e)}")
        return False
    return True

def migrate_students():
    """Migrate student data"""
    try:
        from attendence_sys.models import Student as DjangoStudent
        from src.models.student import Student
        from src.database import get_db
        
        with get_db() as db:
            students = DjangoStudent.objects.all()
            for old_student in students:
                new_student = Student(
                    registration_id=old_student.registration_id,
                    first_name=old_student.firstname,
                    last_name=old_student.lastname,
                    grade=f"{old_student.year}",
                    cultural_considerations={
                        "branch": old_student.branch,
                        "section": old_student.section
                    },
                    # POPIA compliance fields
                    consent_given=False,  # Require new consent
                    consent_date=datetime.utcnow(),
                    data_retention_date=datetime.utcnow(),
                    purpose_of_collection="Student attendance tracking"
                )
                db.add(new_student)
            
            db.commit()
            logger.info("Students migrated successfully")
    except Exception as e:
        logger.error(f"Failed to migrate students: {str(e)}")
        return False
    return True

def migrate_face_data():
    """Migrate face recognition data"""
    try:
        from src.models.face_data import FaceData
        from src.security.encryption import EncryptionService
        from src.database import get_db
        import face_recognition
        import os
        
        encryption_service = EncryptionService()
        
        with get_db() as db:
            # Get all student image paths
            image_dir = os.path.join('static', 'images', 'Student_Images')
            for root, dirs, files in os.walk(image_dir):
                for file in files:
                    if file.endswith(('.jpg', '.jpeg', '.png')):
                        try:
                            # Load and encode face
                            image_path = os.path.join(root, file)
                            image = face_recognition.load_image_file(image_path)
                            face_encodings = face_recognition.face_encodings(image)
                            
                            if face_encodings:
                                # Get student ID from filename
                                student_id = file.split('.')[0]
                                
                                # Encrypt face encoding
                                encrypted_data, key_id = encryption_service.encrypt_face_data(
                                    face_encodings[0]
                                )
                                
                                # Create new face data record
                                face_data = FaceData(
                                    student_id=student_id,
                                    encoding_data=encrypted_data,
                                    encryption_key_id=key_id,
                                    is_active=True,
                                    quality_score=90  # Default score
                                )
                                db.add(face_data)
                        except Exception as e:
                            logger.warning(f"Failed to migrate face data for {file}: {str(e)}")
                            continue
            
            db.commit()
            logger.info("Face data migrated successfully")
    except Exception as e:
        logger.error(f"Failed to migrate face data: {str(e)}")
        return False
    return True

def main():
    """Main migration function"""
    logger.info("Starting data migration...")
    
    # Setup environments
    setup_django()
    setup_new_db()
    
    # Perform migrations
    success = all([
        migrate_users(),
        migrate_students(),
        migrate_face_data()
    ])
    
    if success:
        logger.info("Migration completed successfully")
    else:
        logger.error("Migration completed with errors")

if __name__ == "__main__":
    main()
