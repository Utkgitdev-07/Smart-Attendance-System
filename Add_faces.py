import streamlit as st
import cv2
import pickle
import numpy as np
import os
import time
from PIL import Image

def record_faces():
    """
    Function to register new faces through the webcam interface
    This is based on the original add_faces.py file
    """
    st.header("Record New Face")
    
    
    name = st.text_input("Enter your name:")
    
    if name:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            
            frame_placeholder = st.empty()
            
            
            cap = cv2.VideoCapture(0)
            
            
            if not cap.isOpened():
                st.error("Error: Could not open webcam")
                return
            
            
            try:
                facedetect = cv2.CascadeClassifier('Data/haarcascade_frontalface_default.xml')
                if facedetect.empty():
                    st.error("Error: Face detection model not found or invalid")
                    st.info("Please make sure 'haarcascade_frontalface_default.xml' is in the Data folder")
                    cap.release()
                    return
            except Exception as e:
                st.error(f"Error loading face detection model: {e}")
                cap.release()
                return
            
            
            faces_data = []
            i = 0
            status_text = st.empty()
            
            start_recording = st.button("Start Recording")
            stop_placeholder = st.empty()
            stop_recording = stop_placeholder.button("Stop Recording", key="stop")
            
            if start_recording and not stop_recording:
                status_text.text("Recording started. Please look at the camera.")
                
                while len(faces_data) < 5 and not stop_recording:
                    ret, frame = cap.read()
                    if not ret:
                        st.error("Error: Could not read from webcam")
                        break
                    
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    
                    faces = facedetect.detectMultiScale(gray, 1.3, 5)
                    
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame_rgb, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        
                        crop_img = frame[y:y+h, x:x+w, :]
                        resized_img = cv2.resize(crop_img, (50, 50))
                        
                        if i % 5 == 0 and len(faces_data) < 5:
                            faces_data.append(resized_img)
                        
                        i += 1
                        
                        cv2.putText(frame_rgb, f"Captures: {len(faces_data)}/5", 
                                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                                    1, (0, 255, 0), 2)
                    
                    frame_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)
                    
                    status_text.text(f"Captured {len(faces_data)}/5 images")
                    
                    stop_recording = stop_placeholder.button("Stop Recording", key=f"stop_{i}")
                    
                    time.sleep(0.2)
                
                cap.release()
                
                if len(faces_data) > 0:
                    faces_data = np.asarray(faces_data)
                    faces_data = faces_data.reshape(len(faces_data), -1)
                    
                    if 'names.pkl' not in os.listdir('Data/'):
                        names = [name] * len(faces_data)
                        with open('Data/names.pkl', 'wb') as f:
                            pickle.dump(names, f)
                    else:
                        with open('Data/names.pkl', 'rb') as f:
                            names = pickle.load(f)
                        names = names + [name] * len(faces_data)
                        with open('Data/names.pkl', 'wb') as f:
                            pickle.dump(names, f)
                    
                    if 'faces_data.pkl' not in os.listdir('Data/'):
                        with open('Data/faces_data.pkl', 'wb') as f:
                            pickle.dump(faces_data, f)
                    else:
                        with open('Data/faces_data.pkl', 'rb') as f:
                            faces = pickle.load(f)
                        faces = np.append(faces, faces_data, axis=0)
                        with open('Data/faces_data.pkl', 'wb') as f:
                            pickle.dump(faces, f)
                    
                    st.success(f"Successfully registered {name} with {len(faces_data)} face captures!")
                else:
                    st.warning("No faces were captured. Please try again.")
            
            elif not start_recording:
                st.info("Click 'Start Recording' to begin face registration")
        
        with col2:
            st.subheader("Instructions")
            st.info(
                """
                1. Look directly at the camera
                2. Make sure your face is well-lit
                3. Keep your face centered in the frame
                4. Avoid rapid movements
                5. The system will capture 5 images of your face
                """
            )
            
            st.subheader("Example")
            st.image("https://img.icons8.com/color/96/000000/face-id.png", width=150)
