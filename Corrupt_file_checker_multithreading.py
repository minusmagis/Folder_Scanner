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
import concurrent.futures

Image.MAX_IMAGE_PIXELS = 2000000000

def Image_process(filename):
    extension = '.jpg'
    global Files_with_extension
    global Corrupted_files
    global Moved_files
    global Scanned_files
    global Full_path_file_list
    global completion_percentage
    if filename.casefold().endswith(extension):
        Files_with_extension += 1
        # print(filename)
        File_Corrupt, Error = IcC.Image_corrupt_check(filename, extension)
        if File_Corrupt:
            Corrupted_files += 1
            # print('Bad file:', filename)  # print out the names of corrupt files
            Moved_successfully, Error = IcC.Move_Image_to_Corrupt_folder(filename, Folder_for_corrupted_files, File_list[index])
            if Moved_successfully:
                Moved_files += 1
    Scanned_files +=1
    if Scanned_files % 1000 == 0:
        elapsed_time = time.time() - start_time
        completion_percentage = ((1 + Scanned_files) / len(Full_path_file_list)) * 100
        estimated_time = elapsed_time / (completion_percentage / 100)
        print(str(completion_percentage) + '% ' + str(len(File_extension_list)) + ' Elapsed time = ' + str(round(elapsed_time, 2)) + ' s   Estimated Time = ' + str(round(estimated_time * len(File_extension_list), 2)) + '     ' + str(Corrupted_files) + ' Corrupted files of which ' + str(
                        Moved_files) + '  moved succesfully from ' + str(Files_with_extension) + ' Extension Files from a total of ' + str(len(Full_path_file_list))+ ' Semicorrupted images = '+str(Semi_corrupted_images))


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

# Folder_With_all_files = filedialog.askdirectory(initialdir = r"C:\Users\minus\Desktop\Newly recovered files",mustexist = True,title = "Select the directory which you want to check")
# Folder_for_corrupted_files = filedialog.askdirectory(initialdir = r"C:\Users\minus\Desktop\Newly recovered files",mustexist = True,title = "Select the directory in which the corrupted files will be allocated")

Folder_With_all_files = r'E:\Newly recovered files'
Folder_for_corrupted_files = r'E:\Corrupt Files'

File_list, Full_path_file_list = getListOfFilesFullPath(Folder_With_all_files)

#print(*Full_path_file_list,sep='\n')
Corrupted_files = 0
Moved_files = 0
Files_with_extension = 0
Scanned_files = 0
Semi_corrupted_images = 0

start_time = time.time()
elapsed_time= 0
real_elapsed_time =0
estimated_time = 0
completion_percentage = 0

File_extension_list = ['.jpg']#,'.png','.gif','.jpeg','.bmp','.tif']

if __name__ == '__main__':
    for extension in File_extension_list:
        args = (Full_path_file_list,extension)
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(Image_process, Full_path_file_list)
        print(str(completion_percentage) + '% ' + str(len(File_extension_list)) + ' Elapsed time = ' + str(round(time.time()-start_time, 2)) + ' s   Estimated Time = ' + str(round(estimated_time * len(File_extension_list), 2)) + '     ' + str(Corrupted_files) + ' Corrupted files of which ' + str(
            Moved_files) + '  moved succesfully from ' + str(Files_with_extension) + ' Extension Files from a total of ' + str(len(Full_path_file_list)) + ' Semicorrupted images = ' + str(Semi_corrupted_images))



