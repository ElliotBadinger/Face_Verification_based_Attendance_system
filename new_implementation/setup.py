from setuptools import setup, find_packages

setup(
    name="school-attendance-system",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.5",
        "sqlalchemy>=1.4.23",
        "python-dotenv>=0.19.0",
        "pydantic[email]>=1.8.2",
        "face-recognition>=1.3.0",
        "opencv-python>=4.5.3",
        "pillow>=8.3.2",
        "mysqlclient>=2.0.3",
        "cryptography>=3.4.8",
        "alembic>=1.7.1",  # For database migrations
    ],
    python_requires=">=3.7",
    author="School Attendance System Team",
    description="Face recognition-based attendance system with POPIA compliance",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
