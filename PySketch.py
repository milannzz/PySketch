import cv2
from numpy import *
from tkinter import Label, Frame, Tk, Button, IntVar, Scale, HORIZONTAL, messagebox
from tkinter import filedialog
from PIL import ImageTk,  Image

# Clearer Ui using ctypes
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

mainWindow = Tk()
mainWindow.title("PySketch")
mainWindow.geometry("1366x768")
mainWindow.resizable(width = True, height = True)
mainWindow.grid_columnconfigure(0, weight = 1)

def open_images():
    global path
    global image_canvas
    path=filedialog.askopenfilename(filetypes=[("Image File", ('.jpg', ".png"))])
    try:
        orignal_image = cv2.imread(path)
        image = cv2.resize(orignal_image, (0, 0), fx=(640 / orignal_image.shape[0]), fy=(640 / orignal_image.shape[0]), interpolation=cv2.INTER_AREA)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        photo = ImageTk.PhotoImage(image = Image.fromarray(image))
        image_canvas.config(image='')
        image_canvas.config(image=photo)
        image_canvas.image = photo
        image_canvas.grid(row=1, column=0)
    except:
        pass

def convert_images():
    global path
    global image
    global image_canvas
    try :
        orignal_image = cv2.imread(path)
        image = cv2.resize(orignal_image, (0, 0), fx=(640 / orignal_image.shape[0]), fy=(640 / orignal_image.shape[0]))

        grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        inverted_image = cv2.bitwise_not(grey_image)
        blurred_image = cv2.GaussianBlur(inverted_image, (21, 21), 0)

        invertedblur = cv2.bitwise_not(blurred_image)

        image = cv2.divide(grey_image, invertedblur, scale=250)

        maxIntensity = 255.0 # depends on dtype of image data
        x = arange(maxIntensity) 

        # Parameters for manipulating image data
        phi = 1
        theta = 1

        y = (maxIntensity / phi) * (x / (maxIntensity / theta)) ** 0.5

        # Decrease intensity such that dark pixels become much darker,  bright pixels become slightly dark 

        image = (maxIntensity / phi)*(image / (maxIntensity / theta)) ** 1.5
        image = array(image, dtype=uint8)

        white = [255, 255, 255]
        dark = [25, 25, 25]
        image = cv2.copyMakeBorder(image, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=dark)

        image4tk = Image.fromarray(image)
        image4tk = ImageTk.PhotoImage(image4tk)

        image_canvas.config(image=image4tk, padx=10, pady=5)
        image_canvas.image = image4tk
        image_canvas.grid(row=1, column=0, padx=10, pady=5)
    except:
        messagebox.showerror("Error", "Please select a image")

def saveImage():
    global image
    path = filedialog.asksaveasfilename(initialfile = 'Untitled.jpg', filetypes=[("Image File", ('.jpg', ".png"))])
    try:
        cv2.imwrite(path, image)
    except:
        messagebox.showerror("Error",  "Save file location not specified.")
        

frame = Frame(mainWindow)
frame.grid(row=0, column=0, padx=10, pady=5)
frame.grid_columnconfigure(0, weight = 1)

open_button = Button(frame, text="Open Image", command=open_images, width=15, font="bold 10")
open_button.grid(row=0, column=0, padx=10, pady=5)

convert_button = Button(frame, text="Convert", command=convert_images, width=15, font="bold 10", fg="GREEN")
convert_button.grid(row=0, column=1, padx=10, pady=5)

buttonSave = Button(frame, text="Save Image", command=saveImage, width=15, font="bold 10")
buttonSave.grid(row=0, column=2, padx=10, pady=5)

quality = IntVar()
image_canvas = Label(mainWindow)

qframe = Frame(frame)
qframe.grid(row=0, column=3)
qframe.grid_columnconfigure(0, weight = 1)

qualityScale = Scale(qframe, variable=quality, from_=1, to= 100, orient=HORIZONTAL)
qualityScale.set(100)
qualityScale.grid(row=0, column=0, padx=10, pady=5)

Label(qframe, text="Quality", font="bold 10").grid(row=1, column=0, padx=10, pady=5)

mainWindow.mainloop()
