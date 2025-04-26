import os
import cv2
import numpy as np
import pickle
from datetime import datetime
import time

def ensure_directories_exist():
    """
    Ensure that necessary directories exist
    """
    for directory in ['Data', 'Attendance']:
        if not os.path.exists(directory):
            os.makedirs(directory)
            
def download_cascade_if_needed():
    """
    Download the Haar cascade classifier if it doesn't exist
    """
    cascade_path = 'Data/haarcascade_frontalface_default.xml'
    
    if not os.path.exists(cascade_path):
        import urllib.request
        
        
        if not os.path.exists('Data'):
            os.makedirs('Data')
            
    
        cascade_url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
        
        
        try:
            urllib.request.urlretrieve(cascade_url, cascade_path)
            return True
        except Exception as e:
            print(f"Error downloading cascade file: {e}")
            return False
    return True

def get_current_datetime():
    """
    Get the current date and time formatted as strings
    """
    ts = time.time()
    date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
    day = datetime.fromtimestamp(ts).strftime("%A")
    timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
    
    return date, day, timestamp

def save_attendance(name, timestamp, file_path=None):
    """
    Save attendance to a CSV file
    
    Args:
        name (str): Name of the person
        timestamp (str): Time of attendance
        file_path (str, optional): Path to the attendance file. If None, uses the current date.
    """
    if file_path is None:
        date, _, _ = get_current_datetime()
        file_path = f"Attendance/Attendance_{date}.csv"
    
    
    file_exists = os.path.isfile(file_path)
    
 
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    
    
    import csv
    with open(file_path, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['NAME', 'TIME'])
        writer.writerow([name, timestamp])
        
    return True

def load_face_data():
    """
    Load face data and labels from pickle files
    
    Returns:
        tuple: (faces_data, labels) if successful, (None, None) otherwise
    """
    try:
        with open('Data/names.pkl', 'rb') as w:
            labels = pickle.load(w)
        with open('Data/faces_data.pkl', 'rb') as f:
            faces = pickle.load(f)
        return faces, labels
    except Exception as e:
        print(f"Error loading face data: {e}")
        return None, None

def text_to_speech(text):
    """
    Convert text to speech (simplified version)
    
    Args:
        text (str): Text to convert to speech
    """
    try:
        from win32com.client import Dispatch
        speaker = Dispatch("SAPI.SpVoice")
        speaker.Speak(text)
        return True
    except Exception as e:
        print(f"Error with text-to-speech: {e}")
        return False