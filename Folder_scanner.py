import os
import tkinter
import shutil
from tkinter import filedialog
import textwrap


root = tkinter.Tk()
prompt = '      Press any key      '
label1 = tkinter.Label(root, text=prompt, width=len(prompt), bg='yellow')
label1.pack()

#Folder_With_all_files = filedialog.askdirectory(initialdir = "/",mustexist = True,title = "Select the folder with all the files to scan")
Folder_With_all_files = r'C:\Users\minus\Desktop\Minu Old computers'
#Folder_interesting_files = filedialog.askdirectory(initialdir = "/",mustexist = True,title = "Select the folder where to place the interesting files")
Folder_interesting_files = r'C:\Users\minus\Desktop\Minu old computers interesting folders'
#Folder_Not_interesting_files = filedialog.askdirectory(initialdir = "/",mustexist = True,title = "Select the folder where to dump the files")
Folder_Not_interesting_files = r'C:\Users\minus\Desktop\Minu old computers not interesting folders'

Folders_potentially_interesting = os.listdir(Folder_With_all_files)

print(Folders_potentially_interesting)

letter_count = 0
prev_letter_count = 0

def key(event):
    global letter_count
    letter_count +=1
    if event.char == event.keysym:
        msg = '%r' % event.char
    elif len(event.char) == 1:
        msg = '%r' % (event.keysym, event.char)
    else:
        msg = '%r' % event.keysym
    label1.config(text=msg)
root.bind_all('<Key>', key)



for folder in Folders_potentially_interesting:
    files_asked_for = 0
    print('--------------------------------------------------------------------------New File---------------------------------------------------------------------')
    new_folder_path = Folder_With_all_files+'\\'+folder
    accepted_folder_path = Folder_interesting_files+'\\'+folder
    rejected_folder_path = Folder_Not_interesting_files+'\\'+folder
    print(new_folder_path)
    files_inside_folder = os.listdir(new_folder_path)
    full_path_files_inside_folder = []
    grid_list = [[]]
    minor_list = []
    i = 0
    if len(files_inside_folder) > 11:
        for index,file in enumerate(files_inside_folder):
            full_path_name = new_folder_path + '\\' + file
            full_path_files_inside_folder.append(full_path_name)
            minor_list.append(file)
            if index%10 == 0:
                grid_list.append(minor_list)
                minor_list=[]
        print(*grid_list,sep='\n')
    else:
        for file in files_inside_folder:
            full_path_name = new_folder_path + '\\' + file
            full_path_files_inside_folder.append(full_path_name)
        print(files_inside_folder)
    #print(full_path_files_inside_folder)
    while True:
        if letter_count != prev_letter_count:
            #print(letter_count)
            instruction = label1.cget("text").replace("'","")
            print(instruction)
            prev_letter_count = letter_count
            if instruction == 'a':
                shutil.move(new_folder_path,accepted_folder_path)
                break
            elif instruction == 'r':
                shutil.move(new_folder_path, rejected_folder_path)
                break
            elif instruction == 's':
                break
            elif instruction == 't':
                print(os.listdir(full_path_files_inside_folder[files_asked_for]))
                files_asked_for += 1

        root.update()
        root.update_idletasks()
        #print(label1.cget("text"))

