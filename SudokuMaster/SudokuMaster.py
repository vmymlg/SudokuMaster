import cv2 as cv
import pyautogui
import tkinter as tk
from tkinter import *
from tkinter import ttk
from pynput import keyboard
from pynput.keyboard import Key,Controller
from PIL import ImageTk,Image
import numpy
import time
from threading import Thread

grid_sudoku = [[0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0]]
cell_range = 0
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
            solve()
            
            
        
def save_screenshot():
   image = pyautogui.screenshot(region=(point_hg_x,point_hg_y,point_bd_x-point_hg_x,point_bd_y-point_hg_y))
   image.save('test.png')
   image = ImageTk.PhotoImage(Image.open('test.png'))
   screen.config(image=image)
   line_identifier()

   

#Attention
#Inspiration:
#https://www.geeksforgeeks.org/line-detection-python-opencv-houghline-method/
def line_identifier():
    global lines_list
    image = cv.imread('test.png')
    bordure = cv.Canny(image,100,200,apertureSize=3)
    lignes = cv.HoughLinesP(bordure, 1, numpy.pi/180, threshold=100, minLineLength=50, maxLineGap=100)

    for points in lignes:
        x1,y1,x2,y2=points[0]
        #Rajout des point x,y de haut-gauche parce que les chiffres sont detecter a partir de l'ecran
        lines_list.append([(x1+point_hg_x,y1+point_hg_y),(x2+point_hg_x,y2+point_hg_y)])


def number_identifier():
    location_1 = pyautogui.locateAllOnScreen('1.png')
    location_2 = pyautogui.locateAllOnScreen('2.png')
    location_3 = pyautogui.locateAllOnScreen('3.png')
    location_4 = pyautogui.locateAllOnScreen('4.png')
    location_5 = pyautogui.locateAllOnScreen('5.png')
    location_6 = pyautogui.locateAllOnScreen('6.png')
    location_7 = pyautogui.locateAllOnScreen('7.png')
    location_8 = pyautogui.locateAllOnScreen('8.png')
    location_9 = pyautogui.locateAllOnScreen('9.png')
    location = [location_1,location_2,location_3,location_4,location_5,location_6,location_7,location_8,location_9]
    save_screenshot()
    find_point_info()
    create_grid(location)

def find_point_info():
    point_x_min = 10000
    point_y_min = 10000
    point_x_max = 0
    point_y_max = 0
    for line in lines_list:
        (x1,y1),(x2,y2) = line
        if x1<point_x_min : point_x_min = x1
        if y1<point_y_min : point_y_min = y1
        if x1>point_x_max : point_x_max = x1
        if y1>point_y_max : point_y_max = y1
        if x2<point_x_min : point_x_min = x2
        if y2<point_y_min : point_y_min = y2
        if x2>point_x_max : point_x_max = x2
        if y2>point_y_max : point_y_max = y2
    dimension_cell(point_x_min,point_x_max,point_y_min,point_y_max)

def dimension_cell(point_x_min,point_x_max,point_y_min,point_y_max):
    global point_hg_x
    global point_hg_y
    global point_bd_x
    global point_bd_y
    global cell_range
    point_hg_x = point_x_min
    point_hg_y = point_y_min
    point_bd_x = point_x_max
    point_bd_y = point_y_max
    cell_range = (point_x_max-point_x_min)/9



def create_grid(location):
    global grid_sudoku
    i=0
    for loc in location:
        i+=1
        inserer_nombre_grid(loc,i)
        
    
    print(numpy.matrix(grid_sudoku))

def inserer_nombre_grid(location,i):
    global sudoku
    for loc in location :
        column = ((loc.left-point_hg_x)/cell_range)
        row = ((loc.top-point_hg_y)/cell_range)
        column = int(column)
        row = int(row)
        grid_sudoku[row][column] = i

#Copier entierement https://www.youtube.com/watch?v=PZJ5mjQyxR8
def possible(row, column, number):
    global grid_sudoku
    #Is the number appearing in the given row?
    for i in range(0,9):
        if grid_sudoku[row][i] == number:
            return False

    #Is the number appearing in the given column?
    for i in range(0,9):
        if grid_sudoku[i][column] == number:
            return False
    
    #Is the number appearing in the given square?
    x0 = (column // 3) * 3
    y0 = (row // 3) * 3
    for i in range(0,3):
        for j in range(0,3):
            if grid_sudoku[y0+i][x0+j] == number:return False
                

    return True

def solve():
    global grid_sudoku
    for row in range(0,9):
        for column in range(0,9):
            if grid_sudoku[row][column] == 0:
                for number in range(1,10):
                    if possible(row, column, number):
                        grid_sudoku[row][column] = number
                        solve()
                        grid_sudoku[row][column] = 0

                return
      
    print(numpy.matrix(grid_sudoku))
    Thread(target = bot_remplir()).start()
#Fin copie

def bot_remplir():
    keyboard = Controller()
    for i in range(0,9):
        pyautogui.doubleClick(x=(point_hg_x+((cell_range/2))),y=(point_hg_y+((i*cell_range)+(cell_range/2))))
        for j in range(0,9):
            value = grid_sudoku[i][j]
            keyboard.press(str(value))
            keyboard.release(str(value))
            time.sleep(0.2)
            keyboard.press(Key.right)
            keyboard.release(Key.right)
            time.sleep(0.2)



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
