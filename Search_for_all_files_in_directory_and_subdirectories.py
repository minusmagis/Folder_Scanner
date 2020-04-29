import os
import tkinter
from tkinter import filedialog
import csv
import time


def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        if entry != 'System Volume Information':
            # Create full path
            fullPath = os.path.join(dirName, entry)
            # If entry is a directory then get the list of files in this directory
            if os.path.isdir(fullPath):
                allFiles = allFiles + getListOfFiles(fullPath)
            else:
                entry = entry.replace("'", "")
                entry = entry.replace('"', '')
                allFiles.append(entry)
        if len(allFiles) % 1000 == 0:
            print('Files scanned = '+str(len(allFiles)))

    return allFiles

def import_txt(File_to_import):                                         # Function to import any TXT file and return it in the form of a n dimensional list
    with open(File_to_import,encoding="utf8") as csv_file:                              # Recommended to use with when opening files to prevent corruption in case of sudden close. Open File_to_import as a csv file
        csv_reader = csv.reader(csv_file, delimiter="ß")               # Import the file into a set
        line_count = 0                                                  # Initialize the line_count
        First_sub_item = True
        for row in csv_reader:                                          # For each row in the set :
            if line_count == 0:                                         # We first discard the headers. If needed they can be extracted and returned as well
                #print(f'Column names are: {", ".join(row)}')           # Print For debugging purposes
                line_count += 1                                         # We increase the line count to jump to the next step on the next iteration
            elif line_count == 1:                                       # When we are in the first data row
                for index,item in enumerate(row):
                    if First_sub_item:
                        sub_item = repr(row[index]).replace("'", "")
                        sub_item.replace('"', '')
                        items = [sub_item]
                        First_sub_item = False
                    else:
                        if item != '':
                            sub_item = repr(row[index]).replace("'", "")
                            sub_item.replace('"', '')
                            items.append(sub_item)
                Variable_for_data = list([items])                       # We initialize a item dimensional list with the first items
                line_count += 1                                         # We increase the line count to jump to the next step on the next iteration

            else :                                                      # When we are in the second or later data rows
                First_sub_item = True
                items = []
                for index, item in enumerate(row):
                    if First_sub_item:
                        sub_item = repr(row[index]).replace("'","",99)
                        sub_item.replace('"','',99)
                        items = [sub_item]
                        First_sub_item = False
                    else:
                        if item != '':
                            sub_item = repr(row[index]).replace("'","",99)
                            sub_item.replace('"','',99)
                            items.append(sub_item)
                Variable_for_data.append(items)                         # We append the current items to the already existing item dimensional list to add the values as rows within the list
                ##print(temp_array)                                     # Print For debugging purposes
                line_count += 1                                         # We increase the line count even though it is not really necessary
                #print(*Variable_for_data, sep='\n')
        #print(f'Processed {line_count} lines.')                        # Print For debugging purposes
        #print(temp_array)                                              # Print For debugging purposes
        #print(temp_array.shape)                                        # Print For debugging purposes
        #print(*Variable_for_data, sep='\n')                            # Print For debugging purposes
        return Variable_for_data                                        # When the for loop finishes we return the created list

def Extract(list_to_extract_from,column_to_extract = 0):
    return [item[column_to_extract] for item in list_to_extract_from]

File_With_all_files = filedialog.askopenfilename(initialdir = "/",title = "Select the txt file with the list of files")
Folder_With_all_files = filedialog.askdirectory(initialdir = "/",mustexist = True,title = "Select the directory which you want to check")
File_for_unrecovered_files =  filedialog.askopenfilename(initialdir = r"C:\Users\minus\Documents",title = "Select the txt file to save the recovered files")

print('Extracting values from the txt with all files')
All_files = Extract(import_txt(File_With_all_files))

print('Scanning all files within the selected folder')
# print(*All_files,sep= '\n')
# print(Folder_With_all_files)
list_of_recovered_files = getListOfFiles(Folder_With_all_files)
# print(*list_of_files,sep= '\n')
#
print('Recovered files = '+ str(len(list_of_recovered_files))+'  Files to compare those recovered = '+str(len(All_files)))

start_time = time.time()
estimated_time = 0
completion_percentage = 0
unrecovered_files_list = list()
unrecovered_files = 0
recovered_files = 0

for index,file in enumerate(All_files):
    if file in list_of_recovered_files:
        recovered_files +=1
    else:
        unrecovered_files +=1
        unrecovered_files_list.append(file)
    if index%1000 == 0:
        elapsed_time = time.time() - start_time
        completion_percentage = ((1 + index) / len(All_files)) * 100
        estimated_time = (estimated_time + (elapsed_time / (completion_percentage / 100))) / 2
        print(str(completion_percentage) + '%  Elapsed time = ' + str(round(elapsed_time, 2)) + ' s   Estimated Time = ' + str(round(estimated_time, 2))+'     '+str(recovered_files)+' Recovered files and '+str(unrecovered_files) + ' unrecovered files from ' + str(len(All_files)))

print(unrecovered_files_list)
print(str(recovered_files)+' Recovered files and '+str(unrecovered_files) + ' unrecovered files from ' + str(len(All_files)))

TXT_file2 = open(File_for_unrecovered_files,'a',encoding="utf-8")
for item in unrecovered_files_list:
    TXT_file2.write(str(item)+'\n')
TXT_file2.close()