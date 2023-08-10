import os.path
import datetime
import pickle
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition
import util
import sqlite3
import dlib
import os
from tkinter import messagebox
import numpy as np
import threading
from datetime import datetime



class App:
    def __init__(self):
        self.now = datetime.now()

        self.current_time = self.now.strftime("%H:%M:%S")
        self.main_window = tk.Tk()
        self.main_window.geometry("1100x520+350+100")
        self.main_window.title("FacialRecognition")

        self.login_button_main_window = util.get_button(self.main_window, 'Login', 'green', self.login)
        self.login_button_main_window.place(x=775, y=30)

        self.logout_button_main_window = util.get_button(self.main_window, 'Logout', 'red', self.logout)
        self.logout_button_main_window.place(x=775, y=120)

        

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Admin', 'black', self.checkadmin, fg='white')
        self.register_new_user_button_main_window.place(x=775, y=400)
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)
        self.face_detector = dlib.get_frontal_face_detector()
        self.face_recognizer = dlib.face_recognition_model_v1("C:/Users/akash/OneDrive/Documents/College/deeplearning/FacialRecognitionProject/dlib_face_recognition_resnet_model_v1.dat")
        self.shape_predictor = dlib.shape_predictor("C:/Users/akash/OneDrive/Documents/College/deeplearning/FacialRecognitionProject/shape_predictor_68_face_landmarks.dat")

        self.conn = sqlite3.connect("C:/Users/akash/OneDrive/Documents/College/deeplearning/FacialRecognitionProject/maindatabase")
        self.c = self.conn.cursor()
        # Create a users table if not exists
        self.c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,username TEXT UNIQUE, face_descriptor TEXT)")
        
    def captureface(self,username,empid):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        while True:
            self.gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
            self.dets = self.face_detector(self.gray, 1)
            if len(self.dets) == 1:
                self.shape = self.shape_predictor(self.gray, self.dets[0])
                self.face_descriptor = self.face_recognizer.compute_face_descriptor(frame, self.shape)
                self.face_descriptor_str = ','.join(str(e) for e in self.face_descriptor)

                self.c.execute("INSERT INTO users (id,username, face_descriptor) VALUES (?,?, ?)", (empid,username, self.face_descriptor_str))
            self.conn.commit()
            
            messagebox.showinfo("Success", "Face captured successfully!")
            return
    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def checkadmin(self):
        self.checkadmin_newwindow= tk.Toplevel(self.main_window)
        self.checkadmin_newwindow.geometry("1100x520+350+100")
        self.text_label_register_new_user = util.get_text_label(self.checkadmin_newwindow, 'Admin Username:')
        self.text_label_register_new_user.place(x=410, y=50)
        
        self.adminusername = tk.Entry(self.checkadmin_newwindow,width=20, font=('Times new Roman', 15))
        self.adminusername.place(x=410, y=100)
        

        self.text_label_register_new_user = util.get_text_label(self.checkadmin_newwindow, 'Admin Password:')
        
        self.text_label_register_new_user.place(x=410, y=150)

        self.adminpass = tk.Entry(self.checkadmin_newwindow, show="*",width=20,font=('Times new Roman', 15))
        self.adminpass.place(x=410, y=200)

        self.accept_button_admincheck = util.get_button(self.checkadmin_newwindow, 'Submit', 'green', self.check)
        self.accept_button_admincheck.place(x=385, y=350)
        
        
    def check(self):
        print(type(self.adminusername.get()))
        
        if self.adminusername.get()=="admin" and self.adminpass.get()=="admin":
            self.admin()        
        else:
            util.msg_box('Error', 'Wrong Username or Password')
    def admin(self):
        self.admin_newwindow= tk.Toplevel(self.main_window)
        self.admin_newwindow.geometry("1100x520+350+100")

        self.accept_button_admin_newwindow = util.get_button(self.admin_newwindow, 'Register New User', 'green', self.register_new_user)
        self.accept_button_admin_newwindow.place(x=400, y=100)
        self.logs = util.get_button(self.admin_newwindow, 'Download Logs', 'Grey', self.logs)
        self.logs.place(x=400, y=300)
    
    def login(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        while True:
            self.gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.dets = self.face_detector(self.gray,1)
            while True:
                try:
                    self.shape = self.shape_predictor(self.gray, self.dets[0])
                    break
                except IndexError:
                    messagebox.showinfo("Error", "No valid face found")
                    break
                
            self.face_descriptor = self.face_recognizer.compute_face_descriptor(frame, self.shape)
            self.face_descriptor_str = ','.join(str(e) for e in self.face_descriptor)
                
            self.c.execute("SELECT username, face_descriptor FROM users")
            users = self.c.fetchall()
                
            for user in users:
                self.stored_face_descriptor = np.array([float(e) for e in user[1].split(',')])
                self.distance = np.linalg.norm(self.face_descriptor - self.stored_face_descriptor)
                if self.distance < 0.6:  # Adjust this threshold based on your needs
                    messagebox.showinfo("Success", f"Logged in as {user[0]} at {self.current_time}")
                    return
            return



    def logout(self):

        pass


    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1100x520+350+100")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=775, y=330)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=775, y=420)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.name=tk.Entry(self.register_new_user_window,width=30, font=('Times new Roman', 15))
        self.name.place(x=750, y=40)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Input Name:')
        self.text_label_register_new_user.place(x=750, y=0)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Input EmpID:')
        self.text_label_register_new_user.place(x=750, y=90)

        self.empid=tk.Entry(self.register_new_user_window,width=30, font=('Times new Roman', 15))
        self.empid.place(x=750, y=130)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        self.captureface(self.name.get(),self.empid.get())
    def logs(self):
        pass
if __name__ == "__main__":
    app = App()
    app.start()