from multiprocessing import Value
from tkinter.messagebox import showinfo
from tokenize import ContStr
from turtle import window_height, window_width
import tabula
import cv2 as cv
import pyautogui
import tkinter as tk
from tkinter import ttk
from pynput import keyboard

button1 = False
button2 = False
point_hg_x = 0
point_hg_y = 0
point_bd_x = 0
point_bd_y = 0
window_height = 600
window_width = 400
root = tk.Tk()
root.title('Sudoku Destroyer')
root.geometry(str(window_height)+'x'+str(window_height)+'+50+50')
root.resizable(False,False)
root.iconbitmap('sudoku_icon.ico')


root.columnconfigure(0,weight=1)
root.columnconfigure(1,weight=3)


def mouse_pointer_1():
    global button1
    button1 = True
    
def mouse_pointer_2():
    global button2
    button2 = True  

mouse_button_1 = ttk.Button(root,command=mouse_pointer_1,text="Haut-Gauche")
mouse_button_2 = ttk.Button(root,command=mouse_pointer_2,text="Bas-Droit")
label_pointer1 = ttk.Label(root,text="Pointeur haut-gauche tableau")
label_pointer2 = ttk.Label(root,text="Pointeur bas-droit tableau")

label_pointer1.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
label_pointer2.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
mouse_button_1.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
mouse_button_2.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)

def on_press(key):
   global button1
   global button2
   if button1:
       mouse_position = pyautogui.position()
       point_hg_x = mouse_position[0]
       point_hg_y = mouse_position[1]
       label_pointer1.config(text=( "Coordonnées:"+str(point_hg_x)+","+str(point_hg_y)))
       button1 = False
    
   elif button2:
       mouse_position = pyautogui.position()
       point_bd_x = mouse_position[0]
       point_bd_y = mouse_position[1]
       label_pointer2.config(text = "Coordonnées:"+str(point_bd_x)+","+str(point_bd_y))
       button2 = False
       



listener = keyboard.Listener(on_press=on_press)
listener.start()

root.mainloop()
