# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 14:27:49 2022

@author: shiva
"""
import time
import pyautogui
from tkinter import Tk, filedialog
import datetime
root =Tk()
root.withdraw()
root.attributes('-topmost',True)
open_file = filedialog.askdirectory()
print(open_file)

n =int(input("Enter base: "))
b = n
for i in range(n):
    print(" "*b,end="")
    b = b-1
    print("*"*(2*i+1))
    time.sleep(3)
    f = datetime.datetime.now().strftime("%y_%m_%d_%H_%M_%S")
    pyautogui.screenshot((open_file+"/img_"+f+'.png'))
    
