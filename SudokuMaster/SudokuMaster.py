from multiprocessing import Value
import tabula
import cv2 as cv
import pyautogui
import tkinter as tk
from tkinter import *
from tkinter import ttk
from pynput import keyboard
from PIL import ImageTk,Image
from pytesseract import pytesseract
import numpy

lines_list =[]
button1 = False
button2 = False
start_haut = False
start_bas = False
point_hg_x = 0
point_hg_y = 0
point_bd_x = 0
point_bd_y = 0
window_heights = 1000
window_widths = 500
root = tk.Tk()
root.title('Sudoku Destroyer')
root.geometry(str(window_heights)+'x'+str(window_heights)+'+50+50')
root.resizable(False,False)
root.iconbitmap('sudoku_icon.ico')


root.columnconfigure(0,weight=1)
root.columnconfigure(1,weight=3)
root.columnconfigure(2,weight=3)


def mouse_pointer_1():
    global button1
    global start_haut
    start_haut = True
    button1 = True
    
def mouse_pointer_2():
    global button2
    global start_bas
    start_bas = True
    button2 = True  

def start_screenshot():
    global line_list
    lines_list.clear()
    if start_haut and start_bas:
        if point_hg_x<point_bd_x and point_hg_y<point_bd_y:
            create_screenshot()
        
def create_screenshot():
   print("Create_screenshot")
   image = pyautogui.screenshot(region=(point_hg_x,point_hg_y,point_bd_x-point_hg_x,point_bd_y-point_hg_y))
   image.save('test.png')
   image = ImageTk.PhotoImage(Image.open('test.png'))
   screen.config(image=image)
   line_identifier()

   
def extractdatafrompdf():
    ext = tabula.read_pdf('test.pdf',pages ='1')
    ext[0].to_csv("sudoku.csv")

#Attention
#Vol complet de la fonction
#https://www.geeksforgeeks.org/line-detection-python-opencv-houghline-method/
def line_identifier():
    print("Line_identifier")
    image = cv.imread('test.png')
 
    # Convert image to grayscale
    gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
 
    # Use canny edge detection
    edges = cv.Canny(gray,50,150,apertureSize=3)
 
    # Apply HoughLinesP method to
    # to directly obtain line end points
    global lines_list
    lines = cv.HoughLinesP(
            edges, # Input edge image
            1, # Distance resolution in pixels
            numpy.pi/180, # Angle resolution in radians
            threshold=100, # Min number of votes for valid line
            minLineLength=5, # Min allowed length of line
            maxLineGap=10 # Max allowed gap between line for joining them
            )
 
    # Iterate over points
    for points in lines:
      # Extracted points nested in the list
        x1,y1,x2,y2=points[0]
    # Draw the lines joing the points
    # On the original image
        cv.line(image,(x1,y1),(x2,y2),(0,255,0),2)
    # Maintain a simples lookup list for points
        lines_list.append([(x1,y1),(x2,y2)])
     
    # Save the result image
    cv.imwrite('detectedLines.png',image)

screen = ttk.Label()
start_screen = ttk.Button(root,command=start_screenshot,text="Start Screenshot")
mouse_button_1 = ttk.Button(root,command=mouse_pointer_1,text="Haut-Gauche")
mouse_button_2 = ttk.Button(root,command=mouse_pointer_2,text="Bas-Droit")
label_pointer1 = ttk.Label(root,text="Pointeur haut-gauche tableau")
label_pointer2 = ttk.Label(root,text="Pointeur bas-droit tableau")


label_pointer1.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
label_pointer2.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
mouse_button_1.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
mouse_button_2.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)
start_screen.grid(column=2, row=0, sticky=tk.W, padx=5, pady=5)
screen.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5,columnspan = 3)
path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#Define path to image
path_to_image = 'test.png'
#Point tessaract_cmd to tessaract.exe
pytesseract.tesseract_cmd = path_to_tesseract
#Open image with PIL
img = Image.open(path_to_image)
#Extract text from image
text = pytesseract.image_to_string('test.png')
print(text)
def on_press(key):
   global button1
   global button2
   global point_hg_x
   global point_hg_y
   global point_bd_x
   global point_bd_y
   if key == keyboard.Key.esc:
       listener.stop()
       root.destroy()
   if button1:
       mouse_position = pyautogui.position()
       point_hg_x = mouse_position[0]
       point_hg_y = mouse_position[1]
       label_pointer1.config(text=( "Coordonnees:"+str(point_hg_x)+","+str(point_hg_y)))
       button1 = False
    
   elif button2:
       mouse_position = pyautogui.position()
       point_bd_x = mouse_position[0]
       point_bd_y = mouse_position[1]
       label_pointer2.config(text = "Coordonnees:"+str(point_bd_x)+","+str(point_bd_y))
       button2 = False
       



listener = keyboard.Listener(on_press=on_press)
listener.start()

root.mainloop()
