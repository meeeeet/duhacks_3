import os, shutil
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from telegram import Bot
import asyncio
import nest_asyncio
import time
import cv2
import random
from datetime import datetime
import gspread
import RPi.GPIO as GPIO
from google.oauth2.service_account import Credentials

# DATA
test_img_path="M:/DDU/SEM 6/TP/SEM-VI_Term_Project/Auto-Attendance/face_extract/img/face_55.jpg"
pretrained_model='C:/Users/Administrator/Downloads/face_recognition_model.h5'
extracted_faces='C:/Users/Administrator/OneDrive/Desktop/TEMP'

# TELEGRAM
bot_token = '7146124828:AAGhgu_ZWZ-y7ObNXbgal-mFS1Y-RHObSY8'
user_chat_id = ['1953374962','661067276','868836142'] # Gaurang:1953374962 Meet:661067276 Viraj:868836142
user_sel=1
warn_msg=['[WARNING] Photo isn\'t clear.']
update_msg=['Updating google sheet...']

# GOOGLE SHEET
cred_file="C:/Users/Administrator/Downloads/face-sheet-415304-a148ef94ac7b.json"
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(cred_file, scopes=scopes)
client = gspread.authorize(creds)
sheet_id = "1HDq-JBpx3KvIj_S3YKmnelfzCtf-tUdPdo-RIHmjTmY"


# STUDENT DATA
class_names = ['Dhruv', 'Gaurang', 'Meet', 'Viraj']
student_id=['21ECUOS094','21ECUEG098','21ECUEG073','21ECUBG069']
student_roll_no=['EC053','EC039','EC028','EC035']

# HANDLES
sheet = client.open_by_key(sheet_id)
worksht = sheet.worksheet("Attendace log")
report_worksht=sheet.worksheet("Report")
model = load_model(pretrained_model)

def face_rasp(student_id):
    def extract_faces(image_path, output_folder):

        folder = output_folder
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8, minSize=(30, 30))
        extracted_faces = []
        a=0
        for i, (x, y, w, h) in enumerate(faces):
            face = image[y:y+h, x:x+w]
            extracted_faces.append(face)
            face_filename = os.path.join(output_folder, f'face_{a}.jpg')
            cv2.imwrite(face_filename, face)
            print(f"Face {a} saved to {face_filename}")
            a=a+1

    image_path = test_img_path
    extract_faces(image_path,extracted_faces)

    nest_asyncio.apply()

    mybot = Bot(token=bot_token)
    async def send_telegram_messages(msg_list,user_chat_id):
        for i in range(len(msg_list)):
            await mybot.send_message(chat_id=user_chat_id, text=msg_list[i])
            await asyncio.sleep(1)  # Adjust the sleep duration as needed

    def process_images(image_folder):
        process_msgs = []
        avg_acc=0
        count=0
        for filename in os.listdir(image_folder):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                img_path = os.path.join(image_folder, filename)
                img = image.load_img(img_path, target_size=(256, 256))
                img_array = image.img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize the image data

                predictions = model.predict(img_array)
                predicted_class_index = np.argmax(predictions[0])
                predicted_class_label = class_names[predicted_class_index]

                print(filename)
                print(class_names)
                print(predictions[0])
                print(predicted_class_label)
                if(predictions[0][predicted_class_index]>=0.8):
                    avg_acc=avg_acc+max(predictions[0])
                    count=count+1
                    process_msgs.append(student_id[predicted_class_index]+'--'+
                                        student_roll_no[predicted_class_index]+'--'+
                                        predicted_class_label)
        return process_msgs,(avg_acc/count)

    att_msg,avg_acc=process_images(extracted_faces)

    current_time = datetime.now()
    print(avg_acc)
    print(att_msg)
    att_msg=list(set(att_msg))
    print(att_msg)
    split_list = [item.split('--') for item in att_msg]
    print('---------')
    print(split_list)

    asyncio.run(send_telegram_messages(['-----------Attendance Report-----------',
                                        'Date and time: ' + str(current_time)],
                                    user_chat_id[user_sel]))

    current_time = datetime.now()
    if(avg_acc>=0.94):
        asyncio.run(send_telegram_messages(att_msg,user_chat_id[user_sel]))
        asyncio.run(send_telegram_messages(['Updating google sheet...'],user_chat_id[user_sel]))
        last_row = len(worksht.col_values(1)) + 1
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M:%S')

        sheet_data = split_list

        # Find the last row with data in column A
        last_row = len(worksht.col_values(1)) + 1

        for row in sheet_data:
            # Update date and time values
            worksht.update('A{}'.format(last_row), [[current_date]])
            worksht.update('B{}'.format(last_row), [[current_time]])
            # Update ID, roll no, and name values
            worksht.update('C{}'.format(last_row), [[row[0]]])
            worksht.update('D{}'.format(last_row), [[row[1]]])
            worksht.update('E{}'.format(last_row), [[row[2]]])
            # Move to the next row
            last_row += 1
        asyncio.run(send_telegram_messages(['Done!!!'],user_chat_id[user_sel]))
    else:
        asyncio.run(send_telegram_messages(warn_msg,user_chat_id[user_sel]))

    cell_range = 'D3:D6'
    cell_values = report_worksht.get(cell_range)
    ratt_percentage = [value[0] for value in cell_values]
    cell_range = 'A3:A6'
    cell_values = report_worksht.get(cell_range)
    ratt_id = [value[0] for value in cell_values]

    detained_stdid = []
    for i, percentage in enumerate(ratt_percentage):
        if float(percentage) < 75:
            # If the attendance percentage is less than 75, add the corresponding ID to detained_stdid list
            detained_stdid.append(ratt_id[i])

    # Print the detained student IDs
    print("-----------Likely to be detained-----------")
    detained_email = []
    for student_id in detained_stdid:
        email = student_id + '@ddu.ac.in'
        detained_email.append(email)

    print(detained_email)

    detain_msg=['-----------Overall Attendance Report-----------',
                'Following Student(s) have less than 75% attendance.']
    combined_list = []

    for i in range(len(detained_stdid)):
        combined_element = "{}. {} {{{}}}".format(i+1, detained_stdid[i], detained_email[i])
        combined_list.append(combined_element)

    print(combined_list)

    asyncio.run(send_telegram_messages(detain_msg,user_chat_id[user_sel]))
    asyncio.run(send_telegram_messages(combined_list,user_chat_id[user_sel]))
    gsheet_link='bit.ly/AttendanceReportMS'
    asyncio.run(send_telegram_messages(['Google sheet link: '+gsheet_link],user_chat_id[user_sel]))



############################ MAIN PROGRAM ##################################


# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set the pin numbers
led_pin = 18
button_pin = 17
start_pin = 23
# Set up the LED pin as an output
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(start_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        # Check if the button is pressed
        if GPIO.input(button_pin) == GPIO.HIGH:
            # Turn on the LED
            GPIO.output(led_pin, GPIO.HIGH)
            GPIO.output(start_pin, GPIO.LOW)
            os.system("rpicam-jpeg -o /home/viraj/Desktop/Sem-VI\ Term\ Project/Face/test.jpg -t 10000")
            face_rasp(student_id)
            time.sleep(2)
        else:
            # Turn off the LED
            GPIO.output(led_pin, GPIO.LOW)
            GPIO.output(start_pin, GPIO.HIGH)
            print("WAITING PUSH BUTTON TO BE PRESSED...")
        # Add a small delay to debounce the button
        time.sleep(0.1)
finally:
    # Clean up GPIO pins
    GPIO.cleanup()
