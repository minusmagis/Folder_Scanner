import csv
import tkinter
from tkinter import filedialog
import Search_for_all_files_in_directory_and_subdirectories as SfaF
import time
from numba import jit
import numpy as np

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


def fileextchecher(All_files_list,File_extension_list_temp, index_to_check = []):
    recovered_files = 0
    Unrecovered_files = 0
    start_time = time.time()
    estimated_time = 0
    recovered_files_list = list()
    Unrecovered_files_list = list()
    Unrecovered_files_index = list()
    All_picture_files_length = len(All_files_list)
    if len(index_to_check)==0:
        for index,file in enumerate(All_files_list):
            file_with_space = file+' '
            if any(word.casefold() in file_with_space.casefold() for word in File_extension_list_temp):
                recovered_files +=1
                recovered_files_list.append(file)
            else:
                Unrecovered_files +=1
                Unrecovered_files_list.append(file)
                Unrecovered_files_index.append(index)
            elapsed_time = time.time() - start_time
            completion_percentage = ((1+index) / All_picture_files_length)*100
            estimated_time = (estimated_time + (elapsed_time/ (completion_percentage / 100))) / 2
            #print(str(index)+'/'+str(All_picture_files_length))
            if index % 100000 == 0:
                print(str(completion_percentage) + '%  Elapsed time = ' + str(round(elapsed_time, 2)) + ' s   Estimated Time = ' + str(round(estimated_time, 2))+'     '+str(recovered_files)+' Recovered files and '+str(Unrecovered_files) + ' unrecovered files from ' + str(All_picture_files_length))
        # print(*Unrecovered_files_list, sep='\n')
        # print(str(Unrecovered_files) + ' Unrecovered Files')
    else:
        for index in index_to_check:
            file_with_space = All_files_list[index] + ' '
            if any(word.casefold() in file_with_space.casefold() for word in File_extension_list_temp):
                recovered_files +=1
                recovered_files_list.append(All_files_list[index])
            else:
                Unrecovered_files +=1
                Unrecovered_files_list.append(All_files_list[index])
                Unrecovered_files_index.append(index)
            elapsed_time = time.time() - start_time
            completion_percentage = ((1+index) / All_picture_files_length)*100
            estimated_time = (estimated_time + (elapsed_time/ (completion_percentage / 100))) / 2
            #print(str(index)+'/'+str(All_picture_files_length))
            if index % 100000 == 0:
                pass
                #print(str(completion_percentage) + '%  Elapsed time = ' + str(round(elapsed_time, 2)) + ' s   Estimated Time = ' + str(round(estimated_time, 2))+'     '+str(recovered_files)+' Recovered files and '+str(Unrecovered_files) + ' unrecovered files from ' + str(All_picture_files_length))
        # print(*Unrecovered_files_list, sep='\n')
        # print(str(Unrecovered_files) + ' Unrecovered Files')
    return Unrecovered_files_index,Unrecovered_files_list,recovered_files_list



def search_for_extension_and_correct(All_files_raw_list,All_files_list,unrecovered_index_list):
    for index in unrecovered_index_list:
        #print(All_files_raw_list[index])
        if type(All_files_raw_list[index]) == list:
            temp = str(All_files_raw_list[index][0]+' ___'+All_files_raw_list[index][1]).replace('"','')
            All_files_raw_list[index].pop(1)
            All_files_raw_list[index][0] = temp
            All_files_list[index] = temp
    return All_files_list,All_files_raw_list

File_extension_list = ['.txt ','.jpg ','.png ','.jpeg ','.raw ','.tif ','.bmp ','.dsc ','.nef ','.mp3 ','.wma ','.wav ','.m4a ','.doc ','.ppt ','.odt ','.pdf ','.docx ','.pptx ','.xlsx ','.xls ','.avi ','.mov ','.mpg ','.mp4 ','.flv ','.wmv ','.zip ','.rar ','.py ','.stl ','.gcode ','.opj ','.opju ','.xcf ','.ino ','.au ','.aup ','.mts ','.apk ','.apkg ','.3gp ','.opus ','.mkv ','.pfx ','.fzz ','.fzb ','.html ','.ttf ','.gif ','.cer ','.crt ','.rtf ','.h ','.cpp ','.mus ','.sldprt ','.f3d ','.stp ','.mov ','.epub ','.7z ','.swf ']
File_With_all_files = filedialog.askopenfilename(initialdir = r"C:\Users\minus\Documents",title = "Select the txt file with the list of files")
File_for_unrecovered_files =  filedialog.askopenfilename(initialdir = r"C:\Users\minus\Documents",title = "Select the txt file to save the unrecovered files")
File_for_recovered_files =  filedialog.askopenfilename(initialdir = r"C:\Users\minus\Documents",title = "Select the txt file to save the recovered files")
All_files_raw = import_txt(File_With_all_files)

All_files = Extract(All_files_raw)

#print(*All_files_raw,sep='\n')
#input('holi')

print('Starting Scanning procedure')

#test = fileextchechersimple(All_files,File_extension_list)
unrecovered_index,unrecovered_files,recovered_files = fileextchecher(All_files,File_extension_list)

# for index in unrecovered_index:
#     print(All_files_raw[index])
#     print(' ')
# #print(*unrecovered_files,sep='\n')
# input('oli')

print('Starting second Scanning procedure')

All_files,All_files_raw_list = search_for_extension_and_correct(All_files_raw,All_files,unrecovered_index)

unrecovered_index,unrecovered_files,recovered_files = fileextchecher(All_files,File_extension_list)

# for index in unrecovered_index:
#     print(All_files_raw[index])
#     print(' ')
# #print(*unrecovered_files,sep='\n')
# input('oli')

#print(*unrecovered_files,sep='\n')

print('Starting third Scanning procedure')

All_files,All_files_raw_list = search_for_extension_and_correct(All_files_raw,All_files,unrecovered_index)

unrecovered_index,unrecovered_files,recovered_files = fileextchecher(All_files,File_extension_list)

# for index in unrecovered_index:
#     print(All_files_raw[index])
#     print(' ')
# #print(*unrecovered_files,sep='\n')

#print(*unrecovered_files,sep='\n')

TXT_file = open(File_for_recovered_files,'a',encoding="utf-8")
for item in recovered_files:
    TXT_file.write(str(item)+'\n')
TXT_file.close()

TXT_file2 = open(File_for_unrecovered_files,'a',encoding="utf-8")
for item in unrecovered_files:
    TXT_file2.write(str(item)+'\n')
TXT_file2.close()


#print(*All_files,sep='\n')
#print(*All_picture_files,sep='\n')
#print(*All_picture_filenames_recovered,sep= '\n')







# @jit # Set "nopython" mode for best performance, equivalent to @njit
# def fileextchechersimple(All_files_list,File_extension_list_temp):
#     recovered_files = 0
#     Unrecovered_files = 0
#     estimated_time = 0
#     recovered_files_list = np.empty(1)
#     Unrecovered_files_list = np.empty(1)
#     All_picture_files_length = len(All_files_list)
#     for index,file in enumerate(All_files_list):
#         for word in File_extension_list_temp:
#             if word in file:
#                 print()
#             else:
#                 print('alo')
#     #         recovered_files +=1
#     #         recovered_files_list.append(file)
#     #     else:
#     #         Unrecovered_files +=1
#     #         Unrecovered_files_list.append(file)
#     #     completion_percentage = (1+index) / All_picture_files_length
#     #     #print(str(index)+'/'+str(All_picture_files_length))
#     #     if index % 1000 == 0:
#     # #         print(str(completion_percentage) + '%     '+str(recovered_files)+' Recovered files and '+str(Unrecovered_files) + ' unrecovered files from ' + str(All_picture_files_length))
#     # # print(*Unrecovered_files_list, sep='\n')
#     # # print(str(Unrecovered_files) + ' Unrecovered Files')
#     return All_picture_files_length





