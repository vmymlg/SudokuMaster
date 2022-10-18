import cv2 as cv
import pyautogui
import tkinter as tk
from tkinter import *
from tkinter import ttk
from pynput import keyboard
from PIL import ImageTk,Image
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
            number_identifier()
            
            
        
def save_screenshot():
   image = pyautogui.screenshot(region=(point_hg_x,point_hg_y,point_bd_x-point_hg_x,point_bd_y-point_hg_y))
   image.save('test.png')
   image = ImageTk.PhotoImage(Image.open('test.png'))
   screen.config(image=image)
   line_identifier()

   

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
        lines_list.append([(x1+point_hg_x,y1+point_hg_y),(x2+point_hg_x,y2+point_hg_y)])
     
    # Save the result image
    cv.imwrite('detectedLines.png',image)

def number_identifier():
    location_1 = pyautogui.locateOnScreen('1.png')
    location_2 = pyautogui.locateOnScreen('2.png')
    location_3 = pyautogui.locateOnScreen('3.png')
    location_4 = pyautogui.locateOnScreen('4.png')
    location_5 = pyautogui.locateOnScreen('5.png')
    location_6 = pyautogui.locateOnScreen('6.png')
    location_7 = pyautogui.locateOnScreen('7.png')
    location_8 = pyautogui.locateOnScreen('8.png')
    location_9 = pyautogui.locateOnScreen('9.png')
    save_screenshot()
    create_grid(location_1,location_2,location_3,location_4,location_5,location_6,location_7,location_8,location_9)

def create_grid(l1,l2,l3,l4,l5,l6,l7,l8,l9):
    for location in l1:
        x,y = location
        for line in lines_list:


        
    
    

    
    



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
