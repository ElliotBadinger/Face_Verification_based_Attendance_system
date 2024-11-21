import os
import django
from PIL import Image
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Attendence_System.settings')
django.setup()

from attendence_sys.models import Student, Faculty

def verify_and_convert_image(image_path):
    """Verify and convert image to correct format"""
    try:
        logger.debug(f"Processing image: {image_path}")
        with Image.open(image_path) as img:
            # Get original format
            original_mode = img.mode
            logger.debug(f"Original image mode: {original_mode}")

            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
                logger.debug("Converted to RGB mode")

            # Convert to numpy array to verify format
            img_array = np.array(img)
            if img_array.dtype != np.uint8:
                img_array = img_array.astype(np.uint8)
                logger.debug("Converted array to uint8")

            # Verify array shape
            if len(img_array.shape) != 3 or img_array.shape[2] != 3:
                raise ValueError(f"Invalid image shape: {img_array.shape}")

            # Save back as high-quality JPEG
            img = Image.fromarray(img_array)
            img.save(image_path, 'JPEG', quality=95)
            logger.debug(f"Saved processed image to {image_path}")
            return True
    except Exception as e:
        logger.error(f"Error processing {image_path}: {str(e)}")
        return False

def convert_all_images():
    success_count = 0
    error_count = 0

    # Process Student Images
    students = Student.objects.all()
    for student in students:
        if student.profile_pic:
            try:
                image_path = student.profile_pic.path
                if verify_and_convert_image(image_path):
                    success_count += 1
                else:
                    error_count += 1
            except Exception as e:
                logger.error(f"Error with student {student.registration_id}: {str(e)}")
                error_count += 1

    # Process Faculty Images
    faculty = Faculty.objects.all()
    for f in faculty:
        if f.profile_pic:
            try:
                image_path = f.profile_pic.path
                if verify_and_convert_image(image_path):
                    success_count += 1
                else:
                    error_count += 1
            except Exception as e:
                logger.error(f"Error with faculty {f.firstname}: {str(e)}")
                error_count += 1

    # Process all images in static directory
    static_dir = 'static/images'
    for root, dirs, files in os.walk(static_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                if verify_and_convert_image(image_path):
                    success_count += 1
                else:
                    error_count += 1

    return success_count, error_count

if __name__ == '__main__':
    print("Starting image conversion process...")
    success, errors = convert_all_images()
    print(f"Image conversion complete!")
    print(f"Successfully processed: {success} images")
    print(f"Errors encountered: {errors} images")
