import os
import pickle
from tkinter import PhotoImage
import tkinter as tk
from tkinter import messagebox
import face_recognition


def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
                        window,
                        text=text,
                        activebackground="black",
                        activeforeground="white",
                        fg=fg,
                        bg=color,
                        command=command,
                        height=1,
                        width=15,
                        font=('Helvetica bold', 20)
                    )

    return button


def get_img_label(window):
    label = tk.Label(window,borderwidth=2, relief="solid")
    label.place(x=30, y=90,width=640, height=475)
    return label


def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("Times new Roman", 21), justify="left")
    return label


def get_entry_text(window):
    inputtxt = tk.Text(window,
                       height=1,
                       width=15, font=("Times new Roman", 15))
    return inputtxt


def msg_box(title, description):
    messagebox.showinfo(title, description)

def image(window):
    image_path = "C:/Users/akash/OneDrive/Documents/College/deeplearning/FacialRecognitionProject/logo.png"  
    image = PhotoImage(file=image_path)

    # Create a label to display the image
    image_label = tk.Label(window, image=image)
    image_label.pack()
    return image_label


