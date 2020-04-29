import os
import tkinter
from tkinter import filedialog
import csv
import time
from PIL import Image
import shutil
import warnings
import psutil
import Is_Image_corrupt as IcC

Image.MAX_IMAGE_PIXELS = 2000000000

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

Folder_With_all_files = filedialog.askdirectory(initialdir = r"M:\\",mustexist = True,title = "Select the directory which you want to check")
Folder_for_corrupted_files = filedialog.askdirectory(initialdir = r"M:\\",mustexist = True,title = "Select the directory in which the corrupted files will be allocated")

File_list, Full_path_file_list = getListOfFilesFullPath(Folder_With_all_files)

# print(*Full_path_file_list,sep='\n')
Corrupted_files = 0
Moved_files = 0
Files_with_extension = 0
Semi_corrupted_images = 0

File_extension_list = ['.nef']#,'.png','.gif','.jpeg','.bmp','.tif']


start_time = time.time()
elapsed_time= 0
estimated_time = 0
local_completion_percentage=0

for superindex,extension in enumerate(File_extension_list):
    for index,filename in enumerate(Full_path_file_list):
        File_Corrupt = False
        Moved_successfully = False
        if filename.casefold().endswith(extension):
            Files_with_extension +=1
            # print('Filemame = ' + str(filename) + ' Extesion = ' + str(extension))
            File_Corrupt,Error = IcC.Image_corrupt_check(filename,extension)                  # Disable full scan when searching for fully corrupted images
            # File_Corrupt, Error = IcC.Extract_image_by_size(filename, 640,480)
            # print(Error)
            if File_Corrupt:
                Corrupted_files +=1
                # print('Bad file:', filename)  # print out the names of corrupt files
                Moved_successfully, Error = IcC.Move_Image_to_Corrupt_folder(filename, Folder_for_corrupted_files, File_list[index])
                if Moved_successfully:
                    Moved_files += 1
            elapsed_time = time.time() - start_time
            local_completion_percentage = ((1 + index) / len(Full_path_file_list)) * 100
            estimated_time = estimated_time * (0.7) + (elapsed_time / (local_completion_percentage / 100)) * (0.3)
            if index % 10 == 0:
                print(
                    str(local_completion_percentage) + '% ' + str(len(File_extension_list)) + ' Elapsed time = ' + str(round(elapsed_time, 2)) + ' s   Estimated Time = ' + str(round(estimated_time * len(File_extension_list), 2)) + '     ' + str(Corrupted_files) + ' Corrupted files of which ' + str(
                        Moved_files) + '  moved succesfully from ' + str(Files_with_extension) + ' Extension Files from a total of ' + str(len(Full_path_file_list))+ ' Semicorrupted images = '+str(Semi_corrupted_images))
        else:
            pass
            #print(filename)

print(str(local_completion_percentage) + '% ' + str(len(File_extension_list)) + ' Elapsed time = ' + str(round(elapsed_time, 2)) + ' s   Estimated Time = ' + str(round(estimated_time * len(File_extension_list), 2)) + '     ' + str(Corrupted_files) + ' Corrupted files of which ' + str(
                        Moved_files) + '  moved succesfully from ' + str(Files_with_extension) + ' Extension Files from a total of ' + str(len(Full_path_file_list))+ ' Semicorrupted images = '+str(Semi_corrupted_images))


