# Import necessary libraries
import streamlit as st
import pandas as pd
import os
from datetime import datetime
import time

# Get the current timestamp and format it for date, day, and time
ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")  # Date (day-month-year)
day = datetime.fromtimestamp(ts).strftime("%A")  # Day of the week (e.g., Monday)
timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")  # Time with seconds (Hour:Minute:Second)

# Correct file name concatenation
folder_path = 'Attendance'
filename = os.path.join(folder_path, f"Attendance_{date}.csv")  # Construct file path

# Check if the file exists
if os.path.exists(filename):
    # Read the CSV file
    df = pd.read_csv(filename)
    
    # Display the date and day for attendance
    st.write(f"Attendance for {day}, {date}")
    
    # Loop through each row to show user's name and time
    for index, row in df.iterrows():
        name = row['NAME']  # Assuming 'NAME' column holds the user's name
        time_of_attendance = row['TIME']  # Assuming 'TIME' column holds the timestamp
        st.write(f"User: {name}, Time: {time_of_attendance}")
else:
    st.error(f"File not found: {filename}. Please ensure the attendance file is generated.")
