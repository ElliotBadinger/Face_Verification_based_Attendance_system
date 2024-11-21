import face_recognition
import numpy as np
import cv2
import os
from PIL import Image
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def verify_image(image_path):
    """Verify and convert image to correct format if needed"""
    try:
        # Open the image with PIL
        with Image.open(image_path) as img:
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            # Convert to numpy array
            img_array = np.array(img)
            # Verify the array format
            if img_array.dtype != np.uint8:
                img_array = img_array.astype(np.uint8)
            if len(img_array.shape) != 3 or img_array.shape[2] != 3:
                raise ValueError(f"Invalid image shape: {img_array.shape}")
            return img_array
    except Exception as e:
        logger.error(f"Error processing image {image_path}: {str(e)}")
        return None

def Recognizer(details):
    logger.debug(f"Starting Recognizer with details: {details}")
    video = cv2.VideoCapture(0)

    known_face_encodings = []
    known_face_names = []

    base_dir = os.getcwd()
    image_dir = os.path.join(
        base_dir,
        'static',
        'images',
        'Student_Images',
        details['branch'],
        details['year'],
        details['section']
    )
    logger.debug(f"Looking for images in directory: {image_dir}")
    
    if not os.path.exists(image_dir):
        logger.error(f"Directory does not exist: {image_dir}")
        os.makedirs(image_dir, exist_ok=True)
        logger.debug(f"Created directory: {image_dir}")
    
    names = []

    # First verify all images in directory
    image_files = []
    for root, dirs, files in os.walk(image_dir):
        logger.debug(f"Found files: {files}")
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                path = os.path.join(root, file)
                image_files.append((path, file))

    # Process verified images
    for path, file in image_files:
        logger.debug(f"Processing image: {path}")
        try:
            # Verify and load image
            img = verify_image(path)
            if img is None:
                continue

            # Get face encodings
            face_locations = face_recognition.face_locations(img)
            if not face_locations:
                logger.warning(f"No face found in {path}")
                continue

            img_encoding = face_recognition.face_encodings(img, face_locations)[0]
            label = file[:len(file)-4]
            known_face_names.append(label)
            known_face_encodings.append(img_encoding)
            logger.debug(f"Successfully encoded face for: {label}")
        except Exception as e:
            logger.error(f"Error processing {path}: {str(e)}")
            continue

    logger.debug(f"Found {len(known_face_encodings)} face encodings")

    if not known_face_encodings:
        logger.warning("No valid face encodings found in directory")
        video.release()
        return []

    face_locations = []
    face_encodings = []

    while True:    
        check, frame = video.read()
        if not check:
            logger.error("Failed to grab frame from camera")
            break

        small_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []

        for face_encoding in face_encodings:
            try:
                matches = face_recognition.compare_faces(known_face_encodings, np.array(face_encoding), tolerance=0.6)
                if not any(matches):
                    continue

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    face_names.append(name)
                    if name not in names:
                        names.append(name)
                        logger.debug(f"Recognized face: {name}")
            except Exception as e:
                logger.error(f"Error during face comparison: {str(e)}")
                continue

        if len(face_names) == 0:
            for (top,right,bottom,left) in face_locations:
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2

                cv2.rectangle(frame, (left,top), (right,bottom), (0,0,255), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, 'Unknown', (left, top), font, 0.8, (255,255,255), 1)
        else:
            for (top,right,bottom,left), name in zip(face_locations, face_names):
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2

                cv2.rectangle(frame, (left,top), (right,bottom), (0,255,0), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left, top), font, 0.8, (255,255,255), 1)

        cv2.imshow("Face Recognition Panel", frame)

        if cv2.waitKey(1) == ord('s'):
            break

    video.release()
    cv2.destroyAllWindows()
    logger.debug(f"Recognition complete. Found names: {names}")
    return names
