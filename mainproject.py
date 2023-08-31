from tkinter import PhotoImage
import datetime
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import util
import sqlite3 
import dlib
from tkinter import messagebox
import numpy as np
import pandas as pd
import customtkinter
import cv2

class App:
    def __init__(self):
        self.flag=False
        self.current_time = datetime.datetime.now()
        self.cascPath ="C:/Users/akash/OneDrive/Documents/College/deeplearning/FacialRecognitionProject/haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(self.cascPath)
        self.font = cv2.QT_FONT_NORMAL
        self.first_window = tk.Tk()
        self.first_window.geometry("1100x600+350+100")
        self.first_window.resizable(width=False,height=False)
        self.first_window.title("FacialRecognition")
        self.face_detector = dlib.get_frontal_face_detector()
        self.face_recognizer = dlib.face_recognition_model_v1("C:/Users/akash/OneDrive/Documents/College/deeplearning/FacialRecognitionProject/dlib_face_recognition_resnet_model_v1.dat")
        self.shape_predictor = dlib.shape_predictor("C:/Users/akash/OneDrive/Documents/College/deeplearning/FacialRecognitionProject/shape_predictor_68_face_landmarks.dat")
        self.conn = sqlite3.connect("C:/Users/akash/OneDrive/Documents/College/deeplearning/FacialRecognitionProject/maindatabase")
        self.c = self.conn.cursor()
        self.d = self.conn.cursor()
        self.e=self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,username TEXT, face_descriptor TEXT)")
        self.d.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER ,logintime_time DATETIME,logouttime_time DATETIME)")
        self.image_pathnew = "C:/Users/akash/OneDrive/Documents/College/deeplearning/FacialRecognitionProject/first.png"  
        self.imagenew = PhotoImage(file=self.image_pathnew)

        self.image_labelnew = tk.Label(self.first_window, image=self.imagenew)
        self.image_labelnew.pack()
        self.image_labelnew.place(x=0, y=0, width=1100, height=600)
        
        self.login_button_first_window=customtkinter.CTkButton(master=self.first_window, text="Proceed", command=self.main,height=80,width=325,font=('Sans-serif', 30),corner_radius=20,hover=True,border_width=1,border_color="black",bg_color="#7BC2FF",fg_color="#109945")
        self.login_button_first_window.place(x=375, y=255)
    def main(self):
        self.main_window= tk.Toplevel(self.first_window)
        self.main_window.geometry("1100x600+350+100")
        self.main_window.resizable(width=False,height=False)
        self.main_window.title("FacialRecognition")
        self.main_window.configure(background="white")
        self.image_path = "C:/Users/akash/OneDrive/Documents/College/deeplearning/FacialRecognitionProject/logo2.png"  
        self.image = PhotoImage(file=self.image_path)

        self.image_label = tk.Label(self.main_window, image=self.image)
        self.image_label.pack()
        self.image_label.place(x=0, y=0, width=1100, height=600)
        
        self.login_button_main_window=customtkinter.CTkButton(master=self.main_window, text="Login", command=self.login,height=50,width=275,font=('Sans-serif', 30),corner_radius=20,hover=True,border_width=1,border_color="black",bg_color="#64AFFF",fg_color="#109945")
        self.login_button_main_window.place(x=760, y=100)
        self.logout_button_main_window = customtkinter.CTkButton(master=self.main_window, text="Logout", command=self.logout,height=50,width=275,font=('Sans-serif', 30),corner_radius=20,hover=True,border_width=1,border_color="black",bg_color="#64AFFF",fg_color="#109945")
        self.logout_button_main_window.place(x=760, y=180)
        self.face_descriptor=0
        

        self.register_new_user_button_main_window = customtkinter.CTkButton(master=self.main_window, text="Admin", command=self.checkadmin,height=50,width=275,font=('Sans-serif', 30),corner_radius=20,hover=True,border_width=1,border_color="black",bg_color="#7BC2FF",fg_color="#2e2e2e")
        self.register_new_user_button_main_window.place(x=760, y=430)
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=30, y=90, width=640, height=400)

        self.add_webcam(self.webcam_label)
    
    def reg(self):
        self.main_window.destroy()
        self.adminmain_window= tk.Toplevel(self.first_window)
        self.adminimage_path = "C:/Users/akash/OneDrive/Documents/College/deeplearning/FacialRecognitionProject/reg.png"
        self.adminmain_window.geometry("1100x600+350+100")
        self.adminmain_window.resizable(width=False,height=False)
        self.adminimage = PhotoImage(file=self.adminimage_path)
        self.adminimage_label = tk.Label(self.adminmain_window, image=self.adminimage)
        self.adminimage_label.pack()
        self.adminimage_label.place(x=0, y=0, width=1100, height=600)
        self.adminwebcam_label = util.get_img_label(self.adminmain_window)
        self.adminwebcam_label.place(x=30, y=90, width=640, height=400)
        self.add_webcam (self.adminwebcam_label)
        self.accept_button_register_new_user_window = customtkinter.CTkButton(master=self.adminmain_window, text="Register", command=self.accept_register_new_user,height=50,width=275,font=('Sans-serif', 30),corner_radius=20,hover=True,border_width=1,border_color="black",bg_color="#64AFFF",fg_color="#109945")
        self.accept_button_register_new_user_window.place(x=775, y=370)
        

        self.name=customtkinter.CTkEntry(self.adminmain_window,width=340, font=('Sans-serif', 18),corner_radius=20,placeholder_text="",bg_color="#7BC2FF",fg_color="#224957")
        self.name.place(x=730, y=190)

        self.empid=customtkinter.CTkEntry(self.adminmain_window,width=340, font=('Sans-serif', 18),corner_radius=20,placeholder_text="",bg_color="#7BC2FF",fg_color="#224957")
        self.empid.place(x=730, y=280)

    def captureface(self,username,empid):
        if self.flag==True:
            self.c.execute("SELECT rowid FROM users WHERE id = ?", (empid,))
            self.db_result=self.c.fetchone()
            if (self.db_result is None): 
                ret, frame = self.cap.read()
                self.current_time = datetime.datetime.now()
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
                    
                    messagebox.showinfo("Success", "Face captured successfully!",parent= self.adminmain_window)

                    self.adminmain_window.destroy()
                    return
            else:
                messagebox.showinfo("Error","EmpID already exists",parent= self.adminmain_window)
                return
        else:
            messagebox.showinfo("Error","Please fix lighting or position of face, till rectangle around face is visible",parent= self.adminmain_window)
    def add_webcam(self, label):

        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()
    
    def process_webcam(self):
        
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        self.flag=False
        faces = self.faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(200, 200),
        flags=cv2.CASCADE_SCALE_IMAGE
        
    )

    # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 128, 0), 3)
            self.roi_gray = gray[y:y+h, x:x+w]
            self.roi_color = frame[y:y+h, x:x+w]
            cv2.putText(frame,'PROCEED',(x, y-6), self.font, 2,(255,0, 0),2)
            img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
            self.most_recent_capture_pil = Image.fromarray(img_)
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
            self._label.imgtk = imgtk
            self._label.configure(image=imgtk)
            self.flag=True
        self._label.after(20, self.process_webcam)

    def checkadmin(self):

        self.checkadmin_newwindow= tk.Toplevel(self.first_window)
        self.checkadmin_newwindow.geometry("1100x600+350+100")
        self.image_path1 = "C:/Users/akash/OneDrive/Documents/College/deeplearning/FacialRecognitionProject/logo3.png"  
        self.image1 = PhotoImage(file=self.image_path1)
        self.image_label1 = tk.Label(self.checkadmin_newwindow, image=self.image1)
        self.image_label1.pack()
        self.image_label1.place(x=0, y=0, width=1100, height=600)
        
        self.adminusername = customtkinter.CTkEntry(self.checkadmin_newwindow,width=380, font=('Sans-serif', 18),corner_radius=20,placeholder_text="",bg_color="#7BC2FF",fg_color="#224957")
        self.adminusername.place(x=368, y=260)
        

        self.adminpass = customtkinter.CTkEntry(self.checkadmin_newwindow,width=380, font=('Sans-serif', 18),corner_radius=20,placeholder_text="",bg_color="#7BC2FF",fg_color="#224957",show="*")
        self.adminpass.place(x=368, y=335)

        self.accept_button_admincheck = customtkinter.CTkButton(master=self.checkadmin_newwindow, text="Login", command=self.check,height=50,width=275,font=('Sans-serif', 30),corner_radius=20,hover=True,border_width=1,border_color="black",bg_color="#7BC2FF",fg_color="#109945")
        self.accept_button_admincheck.place(x=415, y=410)
        
        
    def check(self):
        
        if self.adminusername.get()=="admin" and self.adminpass.get()=="admin":
            self.admin()        
        else:
            util.msg_box('Error', 'Wrong Username or Password')
            

    def admin(self):
        
        self.admin_newwindow= tk.Toplevel(self.first_window)
        self.admin_newwindow.geometry("1100x600+350+100")
        self.image_path2 = "C:/Users/akash/OneDrive/Documents/College/deeplearning/FacialRecognitionProject/logo4.png"  
        self.image2 = PhotoImage(file=self.image_path2)
        self.image_label2 = tk.Label(self.admin_newwindow, image=self.image2)
        self.image_label2.pack()
        self.image_label2.place(x=0, y=0, width=1100, height=600)
        self.accept_button_admin_newwindow = customtkinter.CTkButton(master=self.admin_newwindow, text="Register New User", command=self.reg,height=50,width=275,font=('Sans-serif', 30),corner_radius=20,hover=True,border_width=1,border_color="black",bg_color="#7BC2FF",fg_color="#109945")
        self.accept_button_admin_newwindow.place(x=400, y=105)
        self.logs_window = customtkinter.CTkButton(master=self.admin_newwindow, text="Download Logs", command=self.log_window,height=50,width=285,font=('Sans-serif', 30),corner_radius=20,hover=True,border_width=1,border_color="black",bg_color="#7BC2FF",fg_color="#109945")
        self.logs_window.place(x=400, y=245)
        self.deluser_window=customtkinter.CTkButton(master=self.admin_newwindow, text="Remove Employee", command=self.deluser,height=50,width=285,font=('Sans-serif', 30),corner_radius=20,hover=True,border_width=1,border_color="black",bg_color="#7BC2FF",fg_color="#109945")
        self.deluser_window.place(x=400, y=395)

    def deluser(self):
        self.checkadmin_newwindow.destroy()
        self.deleteuserwindow=tk.Toplevel(self.first_window)
        self.deleteuserwindow.geometry("1100x600+350+100")
        self.image_path3 = "C:/Users/akash/OneDrive/Documents/College/deeplearning/FacialRecognitionProject/del.png"  
        self.image3 = PhotoImage(file=self.image_path3)
        self.image_label3 = tk.Label(self.deleteuserwindow, image=self.image3)
        self.image_label3.pack()
        self.image_label3.place(x=0, y=0, width=1100, height=600)
        self.delusername = customtkinter.CTkEntry(self.deleteuserwindow,width=380, font=('Sans-serif', 18),corner_radius=20,placeholder_text="",bg_color="#7BC2FF",fg_color="#224957")
        self.delusername.place(x=380, y=265)
        self.accept_button_delete = customtkinter.CTkButton(master=self.deleteuserwindow, text="Delete", command=self.delete,height=50,width=275,font=('Sans-serif', 30),corner_radius=20,hover=True,border_width=1,border_color="black",bg_color="#7BC2FF",fg_color="#109945")
        self.accept_button_delete.place(x=415, y=415)
        
    def delete(self):
        self.main_window.destroy()
        self.c.execute("SELECT rowid FROM users WHERE id = ?", (self.delusername.get(),))
        self.del_result=self.c.fetchone()
        if (self.del_result is None): 
            messagebox.showinfo("Error","No such ID exists",parent=self.deleteuserwindow)
            return
        else:
            self.c.execute('DELETE FROM users WHERE id=?',(self.delusername.get(),))
            self.conn.commit()
            messagebox.showinfo("Sucess","Record Deleted")
            self.deleteuserwindow.destroy()
            self.admin_newwindow.destroy()

    def login(self):
        self.c.execute("SELECT username,id,face_descriptor FROM users")
        users = self.c.fetchall()
        if not users:
            messagebox.showinfo("Error","No users registered")
        if self.flag==True:
            ret, frame = self.cap.read()
            self.current_time = datetime.datetime.now()
            self.most_recent_capture_arr = frame
            while True:
                self.gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                self.dets = self.face_detector(self.gray,1)
                
                while True:
                    try:
                        self.shape = self.shape_predictor(self.gray, self.dets[0])
                        self.face_descriptor = self.face_recognizer.compute_face_descriptor(frame, self.shape)
                        self.face_descriptor_str = ','.join(str(e) for e in self.face_descriptor)
                        break
                    except IndexError:
                        break
                    except AttributeError:
                        break
                for user in users:
                    self.stored_face_descriptor = np.array([float(e) for e in user[2].split(',')])
                    self.distance = np.linalg.norm(self.face_descriptor - self.stored_face_descriptor)
                    if self.distance < 0.4:  # Adjust this threshold based on your needs
                        messagebox.showinfo("Success", f"Logged in as {user[0]} at {self.current_time}",parent=self.main_window)
                        
                        formatted_date = self.current_time.strftime('%Y-%m-%d %H:%M:%S')
                        self.d.execute("INSERT INTO logs (id,logintime_time) VALUES (?,?)", (user[1],formatted_date))
                        self.conn.commit()
                        return
                messagebox.showinfo("Error", "No valid face found",parent=self.main_window)  
                return
        else:
            messagebox.showinfo("Error","No valid face found",parent=self.main_window)
        

    def logout(self):
        self.c.execute("SELECT username,id,face_descriptor FROM users")
        users = self.c.fetchall()
        if not users:
            messagebox.showinfo("Error","No users registered",parent=self.main_window)
        if self.flag==True:
            ret, frame = self.cap.read()
            self.current_time = datetime.datetime.now()
            self.most_recent_capture_arr = frame
            while True:
                self.gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                self.dets = self.face_detector(self.gray,1)
                while True:
                    try:
                        self.shape = self.shape_predictor(self.gray, self.dets[0])
                        self.face_descriptor = self.face_recognizer.compute_face_descriptor(frame, self.shape)
                        self.face_descriptor_str = ','.join(str(e) for e in self.face_descriptor)
                        break
                    except IndexError:
                        break
                    except AttributeError:
                            break
                    
                self.c.execute("SELECT username,id,face_descriptor FROM users")
                users = self.c.fetchall()
                    
                for user in users:
                    self.stored_face_descriptor = np.array([float(e) for e in user[2].split(',')])
                    self.distance = np.linalg.norm(self.face_descriptor - self.stored_face_descriptor)
                    if self.distance < 0.4:  # Adjust this threshold based on your needs
                        messagebox.showinfo("Success", f"Logged out as {user[0]} at {self.current_time}",parent=self.main_window)
                        formatted_date = self.current_time.strftime('%Y-%m-%d %H:%M:%S')
                    
                        self.d.execute("INSERT INTO logs (id,logouttime_time) VALUES (?,?)", (user[1],formatted_date))
                        self.conn.commit()
                        return
                return
        else:
            messagebox.showinfo("Error","No valid face found",parent=self.main_window)
    def add_img_to_label(self, label):

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):

        self.first_window.mainloop()

    def accept_register_new_user(self):

        self.captureface(self.name.get(),self.empid.get())
        self.checkadmin_newwindow.destroy()
        self.admin_newwindow.destroy()
    def try_again_register_new_user(self):

        self.adminmain_window.destroy()

    def logs(self):

        query = "SELECT * FROM logs"
        df = pd.read_sql(query, self.conn)
        df.to_excel("C:/Users/akash/Desktop/data/logs.xlsx")
        messagebox.showinfo("Success","Logs exported")
        self.checkadmin_newwindow.destroy()
        self.admin_newwindow.destroy()
        self.main_window.destroy()
    
    def user(self):
        query = "SELECT id,username FROM users"
        df = pd.read_sql(query, self.conn)
        df.to_excel("C:/Users/akash/Desktop/data/users.xlsx")
        messagebox.showinfo("Success","Logs exported")
        self.checkadmin_newwindow.destroy()
        self.admin_newwindow.destroy()
    def log_window(self):
        
        self.log_newwindow= tk.Toplevel(self.first_window)
        self.log_newwindow.geometry("1100x600+350+100")
        self.image_pathl = "C:/Users/akash/OneDrive/Documents/College/deeplearning/FacialRecognitionProject/logs.png"  
        self.imagel = PhotoImage(file=self.image_pathl)
        self.image_labell = tk.Label(self.log_newwindow, image=self.imagel)
        self.image_labell.pack()
        self.image_labell.place(x=0, y=0, width=1100, height=600)
        self.accept_button_log_newwindow = customtkinter.CTkButton(master=self.log_newwindow, text="Download Login/Logout Info", command=self.logs,height=50,width=325,font=('Sans-serif', 30),corner_radius=20,hover=True,border_width=1,border_color="black",bg_color="#7BC2FF",fg_color="#109945")
        self.accept_button_log_newwindow.place(x=330, y=205)
        self.logs_window = customtkinter.CTkButton(master=self.log_newwindow, text="Download Users", command=self.user,height=50,width=325,font=('Sans-serif', 30),corner_radius=20,hover=True,border_width=1,border_color="black",bg_color="#7BC2FF",fg_color="#109945")
        self.logs_window.place(x=380, y=345)
        
if __name__ == "__main__":
    app = App()
    app.start()
    