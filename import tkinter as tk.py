import tkinter as tk
from tkinter import PhotoImage

main_window = tk.Tk()
main_window.geometry("1100x600+350+100")
image_path = "C:/Users/akash/OneDrive/Documents/College/deeplearning/FacialRecognitionProject/logo.png"  
image = PhotoImage(file=image_path)

    # Create a label to display the image
image_label = tk.Label(main_window, image=image)
image_label.pack()
image_label.place(x=60, y=55, width=400, height=175)
