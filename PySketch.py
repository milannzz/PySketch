import cv2 as cv
import tkinter as tk
import numpy as np
from tkinter import filedialog
from PIL import ImageTk,  Image
from datetime import datetime

# Clearer Ui using ctypes
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

class pySketchApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.fileypes = [("Image File", ('.jpg', ".png", '.jpeg', '.bmp', '.tiff', 'tif', '.pbm'))]
        self.font = " helvectica 10"
        self.image_canvas = tk.Label(self)
        self.draw_ui()

    def draw_ui(self):
        self.title("PySketch")
        self.minsize(1366, 868)
        self.resizable(width = True, height = True)
        self.grid_columnconfigure(0, weight = 1)

        container = tk.Frame(self)
        container.grid(row=0, column=0, padx=10, pady=5)
        container.grid_columnconfigure(0, weight = 1)

        open_button = tk.Button(container, text="Open Image", command=self.open_images, width=15, font=self.font)
        open_button.grid(row=0, column=0, padx=10, pady=5, ipady=3)

        convert_button = tk.Button(container, text="Convert", command=self.convert_images, width=15, font=self.font, fg="GREEN")
        convert_button.grid(row=0, column=1, padx=10, pady=5, ipady=3)

        save_button = tk.Button(container, text="Save Image", command=self.saveImage, width=15, font=self.font)
        save_button.grid(row=0, column=2, padx=10, pady=5, ipady=3)
        
        quality_label = tk.Label(container, text="Quality:", font=self.font)
        quality_label.grid(row=1, column=0, padx=(0, 10), pady=(5, 5), sticky=tk.SW)

        self.quality_scale = tk.Scale(container, from_=1, to= 100, orient=tk.HORIZONTAL, length=200)
        self.quality_scale.set(100)
        self.quality_scale.grid(row=1, column=0, padx=(80, 10), pady=(5, 5), sticky=tk.W)

        gamma_label = tk.Label(container, text="Gamma:", font=self.font)
        gamma_label.grid(row=1, column=1, padx=(0, 10), pady=(5, 5), sticky=tk.SW)

        self.gamma_scale = tk.Scale(container, from_=-50, to=50, resolution=0.01,  orient=tk.HORIZONTAL, length=200)
        self.gamma_scale.set(1)
        self.gamma_scale.grid(row=1, column=1, padx=(80, 10), pady=(5, 5), sticky=tk.W)

        smoothening_label = tk.Label(container, text="Smoothening:", font=self.font)
        smoothening_label.grid(row=1, column=2, padx=(0, 10), pady=(5, 5), sticky=tk.SW)

        self.smoothening_scale = tk.Scale(container, from_=1, to= 100,resolution=1,  orient=tk.HORIZONTAL, length=200)
        self.smoothening_scale.set(27)
        self.smoothening_scale.grid(row=1, column=2, padx=(120, 10), pady=(5, 5), sticky=tk.W)


    def open_images(self):
        self.path=filedialog.askopenfilename(filetypes=self.fileypes)
        try:
            orignal_image = cv.imread(self.path)
            image = cv.resize(orignal_image, (0, 0), fx=(720/ orignal_image.shape[0]), fy=(720/ orignal_image.shape[0]), interpolation=cv.INTER_AREA)
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image = Image.fromarray(image))
            self.image_canvas.config(image='')
            self.image_canvas.config(image=photo)
            self.image_canvas.image = photo
            self.image_canvas.grid(row=1, column=0)
        except:
            pass
    
    def convert_to_drawing(self, image):
        self.update()
        grey_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        inverted_image = cv.bitwise_not(grey_image)
        smoothening = int(self.smoothening_scale.get())
        if smoothening % int(2) == int(0):
            smoothening = smoothening - 1
        blurred_image = cv.GaussianBlur(inverted_image, (smoothening, smoothening), 0)
        inverted_blurred_image = cv.bitwise_not(blurred_image)
        image = cv.divide(grey_image, inverted_blurred_image, scale=256.0)
        gamma = self.gamma_scale.get()
        image = 255 * (image/255) ** gamma
        image = np.array(image, dtype=np.uint8)
        white = [255, 255, 255]
        dark = [25, 25, 25]
        image = cv.copyMakeBorder(image, 5, 5, 5, 5, cv.BORDER_CONSTANT, value=dark)
        return image

    def convert_images(self):
        self.update()
        orignal_image = cv.imread(self.path)
        fx = self.quality_scale.get() / 100
        self.orignal_converted_image = cv.resize(orignal_image, (0, 0), fx=fx, fy=fx, interpolation=cv.INTER_AREA)
        self.orignal_converted_image = self.convert_to_drawing(orignal_image)
        compressed_fx = (720 / orignal_image.shape[0])
        if compressed_fx >= fx:
            compressed_fx = fx
        compress_converted_image = cv.resize(self.orignal_converted_image, (0, 0), fx=compressed_fx, fy=compressed_fx, interpolation=cv.INTER_AREA)
        compress_converted_image = Image.fromarray(compress_converted_image)
        compress_converted_image = ImageTk.PhotoImage(compress_converted_image)
        self.image_canvas.config(image=compress_converted_image, padx=10, pady=5)
        self.image_canvas.image = compress_converted_image
        self.image_canvas.grid(row=1, column=0, padx=10, pady=5)
        self.update()
    
    def saveImage(self):
        filename = 'IMG-' + str(datetime.now().strftime("%Y%m%d%H%M%S")) + '.jpg'
        self.path = filedialog.asksaveasfilename(initialfile = filename, filetypes=self.fileypes)
        cv.imwrite(self.path, self.orignal_converted_image)

if __name__ == "__main__":
    app = pySketchApp()
    app.mainloop()