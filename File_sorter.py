import os
import cv2

import numpy as np
import cv2
import tkinter
from tkinter import filedialog
from PIL import Image,ImageFile
import shutil
import os
import time
import Small_Functions as sf

Folder_to_be_sorted = filedialog.askdirectory(initialdir = r"M:\JPG files\Newly recovered files 13_04_20 JPG\Unknown folder",mustexist = True,title = "Select the directory from which the files you want to sort")
Files_to_sort = os.listdir(Folder_to_be_sorted)

Folders_to_sort_the_files = ['To be Deleted', 'Siscu', 'Minu']
Folders_to_sort_the_files_list = list()

for Folder in Folders_to_sort_the_files:
    Folders_to_sort_the_files_list.append(sf.Full_path_adder(Folder, Folder_to_be_sorted))
    if not os.path.exists(sf.Full_path_adder(Folder,Folder_to_be_sorted)):
        print(sf.Full_path_adder(Folder,Folder_to_be_sorted))
        os.mkdir(sf.Full_path_adder(Folder,Folder_to_be_sorted))


for Filename in Files_to_sort:
    Img_fullpath = sf.Full_path_adder(Filename, Folder_to_be_sorted)
    img = cv2.imread(Img_fullpath,cv2.IMREAD_COLOR)

    while True:
        try:
            cv2.imshow('image',img)
            key = cv2.waitKey(0)
            if key == 100:
                cv2.destroyAllWindows()
                print('To be deleted')
                shutil.move(Img_fullpath,sf.Full_path_adder(Filename, Folders_to_sort_the_files_list[0]))
                break

            elif key == 97:
                cv2.destroyAllWindows()
                print('Siscu')
                shutil.move(Img_fullpath,sf.Full_path_adder(Filename, Folders_to_sort_the_files_list[1]))
                break

            elif key == 109:
                cv2.destroyAllWindows()
                print('Martí')
                shutil.move(Img_fullpath,sf.Full_path_adder(Filename, Folders_to_sort_the_files_list[2]))
                break
        except:
            break