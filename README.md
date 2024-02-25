# Team: VCC GND
## Project: Automated Attendance System using Facial Recognition 

## Overview

The Automated Attendance System using Facial Recognition is a project aimed at simplifying the process of taking attendance in classrooms. Leveraging the power of facial recognition technology, our system automates the attendance process, eliminating the need for manual roll calls.

## Features

- **Facial Recognition**: The system utilizes facial recognition models to identify and mark the attendance of students present in the classroom.
- **Prototype Version**: We have developed a prototype version capable of recognizing groups of 4 people simultaneously.
- **Hardware Setup**: Raspberry Pi is employed for real-time deployment. The official camera module provided by Raspberry Pi is used for capturing classroom images.
- **Student Data Management**: The system captures details of students via the camera. These details are then updated on a Google Sheet, ensuring efficient data management.
- **Notification System**: A Telegram bot is integrated into the system for notification purposes. It logs messages related to attendance and sends alerts for students with attendance below 75%.

## Technologies Used

- **Tensorflow**: For developing and training CNN-based model.
- **Raspberry Pi**: Hardware platform for deployment.
- **Google Sheet API**: For updating student details.
- **Telegram Bot API**: For notification purposes.

## Usage

1. **Setup Raspberry Pi**: Ensure the Raspberry Pi and camera module are correctly set up in the classroom.
   
2. **Install Dependencies**: Make sure all required dependencies are installed on the Raspberry Pi. This might include libraries for facial recognition, Google Sheet API, and Telegram bot API. Use the following commands to install dependencies:

    ```bash
    pip install tensorflow
    pip install gspread
    pip install opencv-python
    pip install python-telegram-bot
    ```

3. **Clone the Repository**: Clone the project repository onto your Raspberry Pi:

    ```bash
    git clone https://github.com/meeeeet/duhacks_3
    ```

4. **Run the Code**: Navigate to the project directory and run the main script:

    ```bash
    cd automated-attendance-system
    python face_main.py
    ```

      **Note**: Before running the script, ensure to configure confidential information such as API keys and access tokens in the appropriate configuration files.        Certain characters in the configuration files have been changed for security purposes.

5. **Monitor Output**: The system will start capturing image, perform facial recognition, and update attendance data. Monitor the terminal output for any errors or status messages.

6. **Receive Notifications**: Notifications regarding attendance will be sent via the configured Telegram bot. Ensure the bot is set up correctly and authorized to send messages to your Telegram account.

7. **Review Attendance Data**: Attendance data will be updated in real-time on the configured Google Sheet. Access the Google Sheet to review attendance records.

## Demo

- [Project Demo Video](https://www.youtube.com/watch?v=your_video_id) - Watch a demonstration of the Automated Attendance System in action.

## Google Sheet

- [Attendance Google Sheet](https://docs.google.com/spreadsheets/d/your_sheet_id/edit) - View the Google Sheet where attendance data is updated in real-time.

## Contributors
1. Meet Sangani
2. Viraj Tank
3. Gaurang Vasiyar
4. Dhruv Gangadwala
