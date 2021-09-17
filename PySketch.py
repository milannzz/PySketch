import cv2
from numpy import *
from tkinter import Label, Frame, Tk, Button, IntVar, Scale, HORIZONTAL, messagebox
from tkinter import filedialog
from PIL import ImageTk,  Image
from datetime import date, datetime


# Clearer Ui using ctypes
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

fileypes = [("Image File", ('.jpg', ".png", '.jpeg', '.bmp', '.tiff', '.pbm'))]


def open_images():
    global path
    global image_canvas
    path=filedialog.askopenfilename(filetypes=fileypes)
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

def convert_to_drawing(image):
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

    image = (maxIntensity / phi) * (image / (maxIntensity / theta)) ** 1
    image = array(image, dtype=uint8)

    white = [255, 255, 255]
    dark = [25, 25, 25]
    image = cv2.copyMakeBorder(image, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=dark)

    return image

def convert_images():
    global path
    global image_canvas
    global orignal_converted_image
    try :
        orignal_image = cv2.imread(path)
        orignal_converted_image = convert_to_drawing(orignal_image)

        compress_converted_image = cv2.resize(orignal_converted_image, (0, 0), fx=(640 / orignal_image.shape[0]), fy=(640 / orignal_image.shape[0]), interpolation=cv2.INTER_AREA)
        compress_converted_image = Image.fromarray(compress_converted_image)
        compress_converted_image = ImageTk.PhotoImage(compress_converted_image)

        image_canvas.config(image=compress_converted_image, padx=10, pady=5)
        image_canvas.image = compress_converted_image
        image_canvas.grid(row=1, column=0, padx=10, pady=5)
    except:
        messagebox.showerror("Error", "Please select a image first")

def saveImage():
    orignal_converted_image
    filename = 'IMG-' + str(datetime.now().strftime("%Y%m%d%H%M%S")) + '.jpg'
    path = filedialog.asksaveasfilename(initialfile = filename, filetypes=fileypes)
    
    cv2.imwrite(path, orignal_converted_image)
    



# <--- User Interface --->
main_window = Tk()
main_window.title("PySketch")
main_window.minsize(1366, 868)
main_window.resizable(width = True, height = True)
main_window.grid_columnconfigure(0, weight = 1)

container = Frame(main_window)
container.grid(row=0, column=0, padx=10, pady=5)
container.grid_columnconfigure(0, weight = 1)

open_button = Button(container, text="Open Image", command=open_images, width=15, font="bold 10")
open_button.grid(row=0, column=0, padx=10, pady=5)

convert_button = Button(container, text="Convert", command=convert_images, width=15, font="bold 10", fg="GREEN")
convert_button.grid(row=0, column=1, padx=10, pady=5)

save_button = Button(container, text="Save Image", command=saveImage, width=15, font="bold 10")
save_button.grid(row=0, column=2, padx=10, pady=5)

quality = IntVar()
image_canvas = Label(main_window)

quality_frame = Frame(container)
quality_frame.grid(row=0, column=3)
quality_frame.grid_columnconfigure(0, weight = 1)

quality_scale = Scale(quality_frame, variable=quality, from_=1, to= 100, orient=HORIZONTAL)
quality_scale.set(100)
quality_scale.grid(row=0, column=0, padx=10, pady=5)

quality_label = Label(quality_frame, text="Quality", font="bold 10")
quality_label.grid(row=1, column=0, padx=10, pady=5)

main_window.mainloop()
