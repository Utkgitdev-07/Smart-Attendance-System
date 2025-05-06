# 📊 Smart Attendance System

## Overview

The **Smart Attendance System** is a vision-based project that automates attendance tracking using computer vision and machine learning techniques. It leverages face recognition to register attendance in real-time, making the traditional manual attendance system more efficient and accurate. The application is built with Streamlit, providing an intuitive web interface for all attendance management operations.

## Features

- **Real-time Face Recognition**: Automatically identifies registered individuals using webcam input
- **User Registration**: Simple interface to register new faces with the system
- **Automated Attendance**: Marks attendance with timestamps when registered faces are detected
- **Flexible Attendance Modes**:
  - Auto-stop after detecting all registered users
  - Auto-stop after detecting a specific number of users
  - Auto-stop after a time limit
- **Audio Feedback**: Voice confirmation when attendance is marked
- **Attendance Records**: View and download attendance reports by date
- **User-friendly Interface**: Clean Streamlit UI for easy navigation and use

## Technologies Used

- **Python**: Core programming language
- **Streamlit**: Web application framework for the user interface
- **OpenCV**: Computer vision for face detection and image processing
- **scikit-learn**: KNN classifier for face recognition
- **Pandas**: Data manipulation and CSV handling
- **Threading**: Concurrent processing for audio feedback
- **win32com**: Text-to-speech capabilities (Windows)

## Project Structure

```
Smart-Attendance-System/
│
├── app.py                  # Main application entry point with Streamlit interface
├── Add_faces.py            # Module for registering new faces
├── tempCodeRunnerFile.py   # Module for attendance tracking functionality
├── utils.py                # Utility functions for the system
├── requirements.txt        # List of dependencies
├── Data/                   # Directory for storing face data and models
│   ├── faces_data.pkl      # Pickle file containing face embeddings
│   ├── names.pkl           # Pickle file containing corresponding names
│   └── haarcascade_frontalface_default.xml  # Face detection model
├── Attendance/             # Directory for storing attendance records
│   └── Attendance_DD-MM-YYYY.csv  # Daily attendance records
└── README.md               # Project documentation (this file)
```

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.7+ 
- pip (Python package manager)
- Webcam (built-in or external)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Utkgitdev-07/Smart-Attendance-System.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Smart-Attendance-System
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage Guide

### Starting the Application

Run the application using Streamlit:
```bash
streamlit run app.py
```

### Navigation

The application has four main sections accessible from the sidebar:

1. **Home**: Introduction to the system features
2. **Register Face**: Add new faces to the system
3. **Take Attendance**: Start attendance tracking session
4. **View Records**: Check and download attendance records

### Registering New Faces

1. Navigate to the "Register Face" section
2. Enter the person's name
3. Click "Start Recording"
4. The system will capture 5 images of the face
5. Click "Stop Recording" when finished

### Taking Attendance

1. Navigate to the "Take Attendance" section
2. Select an auto-stop mode:
   - After detecting all registered users
   - After detecting a specific number of users
   - After a time limit
3. Click "Start Attendance Taking"
4. Registered faces will be recognized and attendance will be marked automatically
5. Audio confirmation will announce each successful attendance entry
6. The system will stop automatically based on your selected mode or you can stop manually

### Viewing Attendance Records

1. Navigate to the "View Records" section
2. Select a date from the dropdown menu
3. View attendance statistics and detailed records
4. Download the attendance as a CSV file

## Technical Details

### Face Recognition Process

1. **Face Detection**: Uses Haar Cascade classifier to detect faces in webcam feed
2. **Face Processing**: Detected faces are cropped, resized to 50x50 pixels, and flattened
3. **Classification**: KNN (K-Nearest Neighbors) algorithm identifies the person
4. **Attendance Marking**: When a person is recognized, their name and timestamp are recorded

### Data Storage

- **Face Data**: Stored as pickle files (faces_data.pkl, names.pkl)
- **Attendance Records**: Stored as CSV files with date-based naming

## Troubleshooting

- **Webcam Not Detected**: Ensure your webcam is properly connected and not in use by another application
- **Face Not Recognized**: Try registering again with better lighting and multiple angles
- **Missing Cascade File**: The system should automatically download it, but you can manually place it in the Data directory

## Future Enhancements

- Multiple face detection for group attendance
- Integration with databases for more robust data storage
- Mobile application support
- API for integration with other systems
- Automated reporting and analytics

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-name`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature-name`)
6. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
