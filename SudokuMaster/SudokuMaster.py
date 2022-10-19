from gc import callbacks
from glob import glob
from multiprocessing import Value
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
import threading
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

pro_nombre = False
pro_point = False
pro_ligne = False
pro_grid_create = False
pro_grid_remplir = False
pro_bot = False
button1 = False
button2 = False
cell_range = 0
lines_list =[]
point_hg_x = 0
point_hg_y = 0
point_bd_x = 0
point_bd_y = 0
old_hg_x = 0
old_hg_y = 0
old_bd_x = 0
old_bd_y = 0
window_heights = 400
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
    button1 = True
    
def mouse_pointer_2():
    global button2
    button2 = True  

def start_screenshot():
        if point_hg_x<point_bd_x and point_hg_y<point_bd_y:
            restart.config(state='enabled')
            tache.config(text=("Recherche des points"))
            number_identifier()
            
            
            
        
def save_screenshot():
   image = pyautogui.screenshot(region=(point_hg_x,point_hg_y,point_bd_x-point_hg_x,point_bd_y-point_hg_y))
   image.save('test.png')
   image = ImageTk.PhotoImage(Image.open('test.png'))
   line_identifier()

   

#Attention
#Inspiration:
#https://www.geeksforgeeks.org/line-detection-python-opencv-houghline-method/
def line_identifier():
    global lines_list
    global pro_ligne
    image = cv.imread('test.png')
    bordure = cv.Canny(image,100,200,apertureSize=3)
    lignes = cv.HoughLinesP(bordure, 1, numpy.pi/180, threshold=100, minLineLength=50, maxLineGap=100)

    for points in lignes:
        x1,y1,x2,y2=points[0]
        #Rajout des point x,y de haut-gauche parce que les chiffres sont detecter a partir de l'ecran
        lines_list.append([(x1+point_hg_x,y1+point_hg_y),(x2+point_hg_x,y2+point_hg_y)])
    pro_ligne = True
    progression()


def number_identifier():
    global pro_nombre
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
    location_len = len(list(location_1))+len(list(location_2))+len(list(location_3))+len(list(location_4))+len(list(location_5))+len(list(location_6))+len(list(location_7))+len(list(location_8))+len(list(location_9))
    pro_nombre = True
    print(location_len)
    if location_len != 0:
        progression()
        save_screenshot()
        find_point_info()
        create_grid(location)
        Thread(target = solve()).start()
    else:
        tache.config(text="Le sudoku nas pas ete reperer veuillez vous assurer des coordonnees")

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
    global old_bd_x
    global old_bd_y
    global old_hg_x
    global old_hg_y
    global pro_point
    old_bd_x = point_hg_x
    old_bd_y = point_hg_y
    old_hg_x = point_bd_x
    old_hg_y = point_bd_y
    point_hg_x = point_x_min
    point_hg_y = point_y_min
    point_bd_x = point_x_max
    point_bd_y = point_y_max
    cell_range = (point_x_max-point_x_min)/9
    pro_point = True
    progression()



def create_grid(location):
    global grid_sudoku
    global pro_grid_create
    i=0
    for loc in location:
        i+=1
        inserer_nombre_grid(loc,i)
        
    
    print(numpy.matrix(grid_sudoku))
    pro_grid_create = True
    progression()

def inserer_nombre_grid(location,i):
    global sudoku
    for loc in location :
        column = ((loc.left-point_hg_x)/cell_range)
        row = ((loc.top-point_hg_y)/cell_range)
        column = int(column)
        row = int(row)
        grid_sudoku[row][column] = i
#Attention
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
    global pro_grid_remplir
    pro_grid_remplir = True
    progression()
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
            time.sleep(0.1)
            keyboard.press(Key.right)
            keyboard.release(Key.right)
            time.sleep(0.1)
    pro_bot = True
    progression()

def refresh():
    global grid_sudoku
    global cell_range
    global lines_list
    global point_hg_x
    global point_hg_y
    global point_bd_x
    global point_bd_y
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
    point_hg_x = old_hg_x
    point_hg_y = old_hg_y
    point_bd_x = old_bd_x
    point_bd_y = old_bd_y
    progress['value'] = 0
    restart.config(state='disabled')

tache = ttk.Label(root,text="Veuillez entrer les coordonnees")
progress = ttk.Progressbar(root,orient=HORIZONTAL,length=500,mode = 'determinate')
start_screen = ttk.Button(root,command=start_screenshot,text="Start Botting",state = 'disabled')
mouse_button_1 = ttk.Button(root,command=mouse_pointer_1,text="Haut-Gauche")
mouse_button_2 = ttk.Button(root,command=mouse_pointer_2,text="Bas-Droit",state='disabled')
restart = ttk.Button(root,command=refresh,text="Redo",state='disabled')
label_pointer1 = ttk.Label(root,text="Pointeur haut-gauche tableau")
label_pointer2 = ttk.Label(root,text="Pointeur bas-droit tableau")

tache.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5,columnspan = 3)
label_pointer1.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
label_pointer2.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
mouse_button_1.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
mouse_button_2.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)
restart.grid(column=2, row=1, sticky=tk.W, padx=5, pady=5)
start_screen.grid(column=2, row=0, sticky=tk.W, padx=5, pady=5)
progress.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5,columnspan = 3)

def progression():
    timer = threading.Timer(0.2,callbacks)
    timer.start
    if pro_bot:
        progress['value'] = 100
        tache.config(text=("Done"))
        progress.update_idletasks()
    elif pro_grid_remplir:
        progress['value'] = 76
        tache.config(text=("Bot en action Toucher a rien!"))
        progress.update_idletasks()
    elif pro_grid_create:
        progress['value'] = 62
        tache.config(text=("Solving"))
        progress.update_idletasks()
    elif pro_ligne:
        progress['value'] = 52
        tache.config(text=("Creation du grid"))
        progress.update_idletasks()
    elif pro_point:
        progress['value'] = 32
        tache.config(text=("Recherche des lignes"))
        progress.update_idletasks()
    elif pro_nombre:
        progress['value'] = 12
        tache.config(text=("Recherche des points du tableau"))
        progress.update_idletasks()
    




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
       mouse_button_2.config(state='enabled')
    
   elif button2:
       mouse_position = pyautogui.position()
       point_bd_x = mouse_position[0]
       point_bd_y = mouse_position[1]
       label_pointer2.config(text = "Coordonnees:"+str(point_bd_x)+","+str(point_bd_y))
       button2 = False
       start_screen.config(state='enabled')
       tache.config(text=("Pret a lancer!"))
       



listener = keyboard.Listener(on_press=on_press)
listener.start()

root.mainloop()
