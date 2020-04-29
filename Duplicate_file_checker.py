import os
import tkinter
from tkinter import filedialog
import csv
import time
from PIL import Image
import shutil
import re
import hashlib
import ntpath
import imagehash

Image.MAX_IMAGE_PIXELS = 2000000000

def file_hash_partial(filepath):
    with open(filepath, 'rb') as f:
        read_chunk = min(max(file_size(filepath), 0), 1000)
        return hashlib.md5(f.read(read_chunk)).hexdigest()

def image_d_hash(filepath):
    img = Image.open(filepath)
    try:
        Image_Hash = imagehash.dhash(img)
    except OSError:
        try:
            img.close()
        except:
            pass
        return 'Semi Corrupt image'
    img.close()
    return Image_Hash

def file_hash_full(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def Filename_Extractor(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def file_size(filepath):
    try:
        path_size = os.path.getsize(filepath)
    except (OSError,):
        # not accessible (permissions, etc) - pass on
        return -1
    return path_size

def getListOfFilesFullPath(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    Full_path_list = list()
    # Iterate over all the entries
    for entry in listOfFile:
        if entry != 'System Volume Information':
            # Create full path
            fullPath = os.path.join(dirName, entry)
            # If entry is a directory then get the list of files in this directory
            if os.path.isdir(fullPath):
                sub_files, sub_full_path_files = getListOfFilesFullPath(fullPath)
                allFiles = allFiles + sub_files
                Full_path_list = Full_path_list + sub_full_path_files
            else:
                allFiles.append(entry)
                Full_path_list.append(fullPath)
        if len(allFiles) % 1000 == 0:
            print('Files scanned = '+str(len(allFiles)))

    return allFiles,Full_path_list

Folder_With_all_files = filedialog.askdirectory(initialdir = "M:\\",mustexist = True,title = "Select the directory which you want to check")
Folder_for_duplicate_files = filedialog.askdirectory(initialdir = "M:\\",mustexist = True,title = "Select the directory in which the duplicate files will be allocated")
File_for_duplicate_files = filedialog.askopenfilename(initialdir = "M:\\",title = "Select the file in which the duplicate filenames list will be allocated")

File_list, Full_path_file_list = getListOfFilesFullPath(Folder_With_all_files)
hash_list = list()

# print(*Full_path_file_list,sep='\n')

Fine_Scan = True
Definitive_move = True  ## --------------------------------------------------------------------------------------------------


index = 0
Duplicate_files = 0
estimated_time = 0
start_time = time.time()
hash_by_file_size = {}
for index,filename in enumerate(Full_path_file_list):
    if Fine_Scan:
        current_file_size = file_size(filename)
    else:
        current_file_size = round((file_size(filename))/10000)

    # print(current_file_size)
    # print(os.path.getsize(filename))
    # print('--------')
    duplicate = hash_by_file_size.get(current_file_size)
    # print(duplicate)

    if duplicate is not None:
        hash_by_file_size[current_file_size].append(filename)
    else:
        hash_by_file_size[current_file_size] = []
        hash_by_file_size[current_file_size].append(filename)
    if index %1000 == 0:
        completion_percentage = ((index + 1) / (len(Full_path_file_list) + 1)) * 100
        elapsed_time = time.time()-start_time
        estimated_time = elapsed_time/((index+1)/(len(Full_path_file_list)+1))
        print(str(round(completion_percentage,4))+' %  '+'Scanning same size files; '+str(index)+ ' files scanned from '+ str(len(Full_path_file_list))+ '  Elapsed Time :'+str(elapsed_time) +'  Estimated Time : '+str(estimated_time))

# TXT_file2 = open(File_for_duplicate_files,'a',encoding="utf-8")
# for keys,values in hash_by_file_size.items():
#     TXT_file2.write(str(keys) + '\n')
#     TXT_file2.write(str(values) + '\n')
#     print(keys)
#     print(values)
# TXT_file2.close()


First_1000_hash_list = {}
index = 0
start_time = time.time()
for file_size_bracket,file_size_list in hash_by_file_size.items():
    if len(file_size_list) > 1:
        for file in file_size_list:
            current_hash_name = file_hash_partial(file)
            #print(current_hash_name)
            duplicate = First_1000_hash_list.get(current_hash_name)
            #print(duplicate)

            if duplicate is not None:
                First_1000_hash_list[current_hash_name].append(file)
                #print('Moved Duplicate')
            else:
                First_1000_hash_list[current_hash_name] = []
                First_1000_hash_list[current_hash_name].append(file)

    if index %10 == 0:
        completion_percentage = ((index + 1) / (len(hash_by_file_size) + 1)) * 100
        elapsed_time = time.time()-start_time
        estimated_time = elapsed_time/((index+1)/(len(hash_by_file_size)+1))
        print(str(round(completion_percentage,4))+' %  '+'Scanning same first 1000 hash files; '+str(index)+ ' file sizes scanned from '+ str(len(hash_by_file_size))+ '  Elapsed Time :'+str(elapsed_time) +'  Estimated Time : '+str(estimated_time))
    index +=1

Duplicate_files = 0
index = 0
Full_hash_list = {}
start_time = time.time()
for file_1000_hash, filename_list in First_1000_hash_list.items():
    if len(filename_list) > 1:
        for file in filename_list:
            if Fine_Scan:
                try:
                    current_hash_name = file_hash_full(file)
                except Exception as e:
                    current_hash_name ='Semi Corrupt image'
            else:
                try:
                    current_hash_name = image_d_hash(file)
                except Exception as e:
                    current_hash_name ='Semi Corrupt image'
            # print(current_hash_name)
            duplicate = Full_hash_list.get(current_hash_name)
            # print(duplicate)

            if duplicate is not None:
                Full_hash_list[current_hash_name].append(file)
                # print(current_hash_name)
                # print(file)
                if str(current_hash_name) != 'Semi Corrupt image':
                    Duplicate_files += 1
                    # print('Moved Duplicate')
            else:
                Full_hash_list[current_hash_name] = []
                Full_hash_list[current_hash_name].append(file)
    if index %100 == 0:
        completion_percentage = ((index+1)/(len(First_1000_hash_list)+1)) * 100
        elapsed_time = time.time()-start_time
        estimated_time = elapsed_time/((index+1)/(len(First_1000_hash_list)+1))
        print(str(round(completion_percentage,4))+' %  '+str(Duplicate_files)+' Duplicated files from '+ str(len(Full_path_file_list))+'  Elapsed time: '+str(round(elapsed_time,2))+'  Estimated Time : '+str(round(estimated_time,2)))
    index +=1

print(str(Duplicate_files)+' Duplicated files from '+ str(len(Full_path_file_list))+'  Elapsed time: '+str(round(elapsed_time,2))+'  Estimated Time : '+str(round(estimated_time,2)))

TXT_file2 = open(File_for_duplicate_files,'a',encoding="utf-8")
for current_image_hash,file_duplicate_list in Full_hash_list.items():
    one_file_saved = False
    if len(file_duplicate_list) >1 :
        TXT_file2.write(str(current_image_hash) + '\n')
        TXT_file2.write(str(file_duplicate_list) + '\n')
        # print(current_image_hash)
        # print(file_duplicate_list)
    if len(file_duplicate_list) >1 and str(current_image_hash) != 'Semi Corrupt image':
        File_to_save = [i for i in file_duplicate_list if 'found.000' in i]
        print(File_to_save)
        if isinstance(File_to_save, list):
            if len(File_to_save) > 0:
                File_to_save = File_to_save[0]
            else:
                File_to_save = file_duplicate_list[0]
        for filename in file_duplicate_list:
            if filename != File_to_save:
                if Definitive_move:
                    shutil.move(filename, os.path.join(Folder_for_duplicate_files, Filename_Extractor(filename)))
                else:
                    shutil.copy(filename, os.path.join(Folder_for_duplicate_files, Filename_Extractor(filename)))
TXT_file2.close()

# for keys,values in full_hash_list.items():
#     print(keys)
#     print(values)
#-----------------------------------------------------------first step

# for index,filename in enumerate(Full_path_file_list):
#     hash_name = file_hash(filename)
#     if hash_name in hash_list:
#         Duplicate_files +=1
#         shutil.move(filename, os.path.join(Folder_for_duplicate_files, File_list[index]))
#     else:
#         hash_list.append(hash_name)
#     if index %1000 == 0:
#         elapsed_time = time.time()-start_time
#         estimated_time = elapsed_time/((index+1)/(len(Full_path_file_list)+1))
#         print(str(Duplicate_files)+' Duplicated files of '+str(index)+ 'files scanned from'+ str(len(Full_path_file_list))+'  Estimated Time : '+str(estimated_time))
#
#
# print(str(Duplicate_files)+' Duplicated files of ' +str(len(Full_path_file_list))+' Files')