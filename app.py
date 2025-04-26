import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime
import Add_faces
import tempCodeRunnerFile
from PIL import Image


st.set_page_config(
    page_title="Smart Attendance System",
    page_icon="📊",
    layout="wide"
)

for folder in ['Data', 'Attendance']:
    if not os.path.exists(folder):
        os.makedirs(folder)

def main():
    st.sidebar.title("Smart Attendance System")
    st.sidebar.image("https://img.icons8.com/color/96/000000/face-id.png", width=100)
    
    page = st.sidebar.radio("Navigation", ["Home", "Register Face", "Take Attendance", "View Records"])
    
    if page == "Home":
        st.title("Welcome to Smart Attendance System")
        st.subheader("A vision-based project that automates attendance tracking")
        
        st.markdown("""
        This system uses computer vision and machine learning to recognize faces and mark attendance automatically.
        
        ### Key Features:
        - Face recognition for attendance tracking
        - Real-time attendance recording
        - Detailed attendance reports
        - User-friendly interface
        
        ### How to Get Started:
        1. Register faces in the system
        2. Take attendance using the webcam
        3. View attendance records anytime
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("Register Face")
            st.image("https://img.icons8.com/color/96/000000/add-user-male.png", width=100)
        with col2:
            st.info("Take Attendance")
            st.image("https://img.icons8.com/color/96/000000/attendance-mark.png", width=100)
        with col3:
            st.info("View Records")
            st.image("https://img.icons8.com/color/96/000000/report-card.png", width=100)
            
    elif page == "Register Face":
        Add_faces.record_faces()
        
    elif page == "Take Attendance":
        tempCodeRunnerFile.take_attendance()
        
    elif page == "View Records":
        view_attendance()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info("Smart Attendance System v1.0")
    st.sidebar.text("© 2025 | All Rights Reserved")

def view_attendance():
    st.header("Attendance Records")
    
    if not os.path.exists('Attendance'):
        st.error("No attendance records found.")
        return
    
    attendance_files = [f for f in os.listdir('Attendance') if f.startswith('Attendance_') and f.endswith('.csv')]
    
    if not attendance_files:
        st.warning("No attendance records found.")
        return
    
    attendance_files.sort(reverse=True)
    
    selected_date = st.selectbox("Select Date", attendance_files, 
                                format_func=lambda x: x.replace('Attendance_', '').replace('.csv', ''))
    
    if selected_date:
        file_path = os.path.join('Attendance', selected_date)
        
        try:
            df = pd.read_csv(file_path)
            
            st.subheader("Attendance Statistics")
            total_attendees = len(df)
            st.metric("Total Attendees", total_attendees)
            
            st.subheader("Attendance Details")
            st.dataframe(df, use_container_width=True)
            
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=selected_date,
                mime='text/csv',
            )
            
        except Exception as e:
            st.error(f"Error reading attendance file: {e}")

if __name__ == "__main__":
    main()
