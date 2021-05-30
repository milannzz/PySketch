import cv2
from numpy import *
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

mainWindow = Tk()
mainWindow.title("PySketch")
mainWindow.geometry("1366x768")
mainWindow.resizable(width = True, height = True)


def open():
    global path
    path=filedialog.askopenfilename(filetypes=[("Image File",('.jpg',".png"))])
    if path == None:
        return
    imageOrg = cv2.imread(path)
    image = cv2.resize(imageOrg,(0,0),fx=(720/imageOrg.shape[0]),fy=(720/imageOrg.shape[0]))

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
    image = (maxIntensity/phi)*(image/(maxIntensity/theta))**2
    image = array(image,dtype=uint8)

    white = [255,255,255]
    dark = [25,25,25]
    image = cv2.copyMakeBorder(image,5,5,5,5,cv2.BORDER_CONSTANT,value=dark)

    image4tk = Image.fromarray(image)
    image4tk = ImageTk.PhotoImage(image4tk)

    cv2.imwrite("output.jpg",image)

    label = Label(mainWindow ,image=image4tk)
    label.image = image4tk
    label.pack()


buttonOpen = Button(mainWindow,text="Open Images",command=open)
buttonOpen.pack()

mainWindow.mainloop() # Start the GUI
