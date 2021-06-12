import cv2
from numpy import *
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

# Clearer Ui using ctypes
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

mainWindow = Tk()
mainWindow.title("PySketch")
mainWindow.geometry("1366x768")
mainWindow.resizable(width = True, height = True)
mainWindow.grid_columnconfigure(0, weight = 1)


def open():
    global path
    global image

    path=filedialog.askopenfilename(filetypes=[("Image File",('.jpg',".png"))])
    if path == None:
        return
    imageOrg = cv2.imread(path)
    image = cv2.resize(imageOrg,(0,0),fx=(670/imageOrg.shape[0]),fy=(670/imageOrg.shape[0]))

    imggrey = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    image = cv2.bitwise_not(imggrey)
    image = cv2.GaussianBlur(image,(21,21),0)

    invertedblur = cv2.bitwise_not(image)

    image = cv2.divide(imggrey,invertedblur,scale=250)

    maxIntensity = 255.0 # depends on dtype of image data
    x = arange(maxIntensity) 

    # Parameters for manipulating image data
    phi = 1
    theta = 1

    # Increase intensity such that
    # dark pixels become much brighter, 
    # bright pixels become slightly bright
    #newImage0 = (maxIntensity/phi)*(image/(maxIntensity/theta))**0.5
    #newImage0 = array(newImage0,dtype=uint8)

    #cv2.imshow('newImage0',newImage0)
    #cv2.imwrite('newImage0.jpg',newImage0)

    y = (maxIntensity/phi)*(x/(maxIntensity/theta))**0.5

    # Decrease intensity such that
    # dark pixels become much darker, 
    # bright pixels become slightly dark 
    image = (maxIntensity/phi)*(image/(maxIntensity/theta))**1.5
    image = array(image,dtype=uint8)

    white = [255,255,255]
    dark = [25,25,25]
    image = cv2.copyMakeBorder(image,5,5,5,5,cv2.BORDER_CONSTANT,value=dark)

    image4tk = Image.fromarray(image)
    image4tk = ImageTk.PhotoImage(image4tk)

    label = Label(mainWindow ,image=image4tk,padx=10,pady=5)
    label.image = None
    label.image = image4tk
    label.grid(row=1,column=0,padx=10,pady=5)

def saveImage():
    global image
    path = filedialog.asksaveasfilename(initialfile = 'Untitled.jpg',filetypes=[("Image File",('.jpg',".png"))])
    if path == None:
        return
    cv2.imwrite(path,image)

frame = Frame(mainWindow)
frame.grid(row=0,column=0,padx=10,pady=5)
frame.grid_columnconfigure(0, weight = 1)

buttonOpen = Button(frame,text="Open Image",command=open,width=20,font="bold")
buttonOpen.grid(row=0,column=0,padx=10,pady=5)

buttonSave = Button(frame,text="Save Image",command=saveImage,width=20,font="bold")
buttonSave.grid(row=0,column=1,padx=10,pady=5)

# Start the GUI
mainWindow.mainloop()
