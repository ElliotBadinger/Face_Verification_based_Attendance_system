import os
import django
from PIL import Image

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Attendence_System.settings')
django.setup()

from attendence_sys.models import Student, Faculty

def convert_image(image_path):
    if os.path.exists(image_path):
        try:
            img = Image.open(image_path)
            if img.mode != 'RGB':
                print(f"Converting {image_path} to RGB...")
                img = img.convert('RGB')
                img.save(image_path, 'JPEG', quality=95)
                print(f"Successfully converted {image_path}")
        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")

def convert_all_images():
    # Convert Student Images
    students = Student.objects.all()
    for student in students:
        if student.profile_pic:
            image_path = student.profile_pic.path
            convert_image(image_path)

    # Convert Faculty Images
    faculty = Faculty.objects.all()
    for f in faculty:
        if f.profile_pic:
            image_path = f.profile_pic.path
            convert_image(image_path)

    # Also convert any images in the static directory
    static_dir = 'static/images'
    for root, dirs, files in os.walk(static_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                convert_image(image_path)

if __name__ == '__main__':
    print("Starting image conversion process...")
    convert_all_images()
    print("Image conversion complete!")
