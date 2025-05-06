import streamlit as st
import cv2
import pickle
import numpy as np
import os
import time
from datetime import datetime
import csv
import threading

def play_audio_message(message):
    """Play an audio message using text-to-speech"""
    try:
        from win32com.client import Dispatch
        speaker = Dispatch("SAPI.SpVoice")
        speaker.Speak(message)
    except Exception as e:
        st.warning(f"Audio feedback couldn't be played: {e}")

def take_attendance():
    """
    Function to take attendance through the webcam interface
    This is based on the original tempCodeRunnerFile.py file
    Now with auto-stop and audio feedback
    """
    st.header("Take Attendance")
    
    if not os.path.exists('Data/faces_data.pkl') or not os.path.exists('Data/names.pkl'):
        st.error("No face data found. Please register faces first.")
        return
    
    try:
        with open('Data/names.pkl', 'rb') as w:
            LABELS = pickle.load(w)
        with open('Data/faces_data.pkl', 'rb') as f:
            FACES = pickle.load(f)
            
        from sklearn.neighbors import KNeighborsClassifier
        
        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(FACES, LABELS)
        
        st.success("Face recognition model loaded successfully!")
    except Exception as e:
        st.error(f"Error loading face data: {e}")
        return
    
    unique_users = set(LABELS)
    total_registered_users = len(unique_users)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        frame_placeholder = st.empty()
        
        st.subheader("Attendance Settings")
        col_a, col_b = st.columns(2)
        with col_a:
            auto_stop_mode = st.radio("Auto-Stop Mode", 
                                     ["After all registered users", 
                                      "After specific users", 
                                      "After time limit"])
        
        with col_b:
            if auto_stop_mode == "After specific users":
                min_users = st.number_input("Minimum users to detect", 
                                           min_value=1, 
                                           max_value=total_registered_users,
                                           value=min(3, total_registered_users))
            elif auto_stop_mode == "After time limit":
                time_limit = st.number_input("Time limit (seconds)", 
                                            min_value=10, 
                                            max_value=300, 
                                            value=60)
    
        start_attendance = st.button("Start Attendance Taking")
        
        if start_attendance:
            try:
                facedetect = cv2.CascadeClassifier('Data/haarcascade_frontalface_default.xml')
                if facedetect.empty():
                    st.error("Error: Face detection model not found or invalid")
                    st.info("Please make sure 'haarcascade_frontalface_default.xml' is in the Data folder")
                    return
            except Exception as e:
                st.error(f"Error loading face detection model: {e}")
                return
            
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("Error: Could not open webcam")
                return
            
            ts = time.time()
            date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
            timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
            
            attendance_file = f"Attendance/Attendance_{date}.csv"
            file_exists = os.path.isfile(attendance_file)
            
            attendance_taken = {}  
            status_text = st.empty()
            progress_bar = st.progress(0)
            
            attendance_list = st.empty()
            today_attendance = []
            
            stop_placeholder = st.empty()
            stop_button = stop_placeholder.button("Stop Attendance Taking", key="stop_main")
            
            start_time = time.time()
            
            while not stop_button:
                current_time = time.time()
                elapsed_time = current_time - start_time
                
                auto_stop = False
                
                if auto_stop_mode == "After all registered users" and len(attendance_taken) >= total_registered_users:
                    auto_stop = True
                    status_message = "All registered users detected!"
                elif auto_stop_mode == "After specific users" and len(attendance_taken) >= min_users:
                    auto_stop = True
                    status_message = f"Detected {len(attendance_taken)} users as requested!"
                elif auto_stop_mode == "After time limit" and elapsed_time >= time_limit:
                    auto_stop = True
                    status_message = f"Time limit of {time_limit} seconds reached!"
                
                if auto_stop:
                    status_text.info(status_message)
                    break
                
                if auto_stop_mode == "After all registered users":
                    progress = min(len(attendance_taken) / total_registered_users, 1.0)
                    progress_text = f"Detected {len(attendance_taken)}/{total_registered_users} registered users"
                elif auto_stop_mode == "After specific users":
                    progress = min(len(attendance_taken) / min_users, 1.0)
                    progress_text = f"Detected {len(attendance_taken)}/{min_users} users"
                elif auto_stop_mode == "After time limit":
                    progress = min(elapsed_time / time_limit, 1.0)
                    progress_text = f"Time: {int(elapsed_time)}/{time_limit} seconds"
                
                progress_bar.progress(progress)
                status_text.text(progress_text)
                
                ret, frame = cap.read()
                if not ret:
                    st.error("Error: Could not read from webcam")
                    break
                
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = facedetect.detectMultiScale(gray, 1.3, 5)
                
                for (x, y, w, h) in faces:
                    crop_img = frame[y:y+h, x:x+w, :]
                    resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
                    
                    output = knn.predict(resized_img)
                    person_name = str(output[0])
                    
                    cv2.rectangle(frame_rgb, (x, y), (x+w, y+h), (50, 50, 255), 2)
                    cv2.rectangle(frame_rgb, (x, y-40), (x+w, y), (50, 50, 255), -1)
                    cv2.putText(frame_rgb, person_name, (x, y-15), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                    
                    if person_name not in attendance_taken:
                        current_time = datetime.now().strftime("%H:%M:%S")
                        attendance_data = [person_name, current_time]
                        
                        with open(attendance_file, "a", newline="") as csvfile:
                            writer = csv.writer(csvfile)
                            if not file_exists and csvfile.tell() == 0:
                                writer.writerow(['NAME', 'TIME'])
                                file_exists = True
                            writer.writerow(attendance_data)
                        
                        attendance_taken[person_name] = current_time
                        today_attendance.append(f"{person_name} - {current_time}")
                        
                        feedback_thread = threading.Thread(
                            target=play_audio_message, 
                            args=(f"Attendance marked for {person_name}",)
                        )
                        feedback_thread.start()
                        
                        status_text.success(f"Attendance marked for {person_name}")
                
                frame_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)
                
                if today_attendance:
                    attendance_list.markdown("### Today's Attendance:")
                    for entry in today_attendance:
                        attendance_list.markdown(f"- {entry}")
                else:
                    attendance_list.info("No attendance records yet")
                
                stop_button = stop_placeholder.button("Stop Attendance Taking", key=f"stop_{int(time.time()*10)}")
                
                time.sleep(0.05)
            
            cap.release()
            progress_bar.progress(1.0)
            
            if attendance_taken:
                success_message = f"Attendance completed! Recorded {len(attendance_taken)} students."
                st.success(success_message)
                
                completion_thread = threading.Thread(
                    target=play_audio_message, 
                    args=(success_message,)
                )
                completion_thread.start()
            else:
                st.warning("No attendance was recorded.")
    
    with col2:
        st.subheader("Instructions")
        st.info(
            """
            1. Select auto-stop mode
            2. Click "Start Attendance Taking"
            3. Look directly at the camera
            4. The system will recognize registered faces
            5. Audio feedback will confirm each attendance
            6. System will stop automatically based on your settings
            """
        )
        
        st.subheader("Auto-Stop Modes")
        st.write("""
        - **After all registered users**: Stops when all registered faces are detected
        - **After specific users**: Stops after detecting the minimum number of faces
        - **After time limit**: Stops after the specified time in seconds
        """)
        
        st.subheader("Current Session")
        current_date = datetime.now().strftime("%d-%m-%Y")
        current_time = datetime.now().strftime("%H:%M:%S")
        st.write(f"Date: {current_date}")
        st.write(f"Time: {current_time}")
