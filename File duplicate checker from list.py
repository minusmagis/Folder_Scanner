import csv
import tkinter
from tkinter import filedialog
import Search_for_all_files_in_directory_and_subdirectories as SfaF
import time

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
                        sub_item = repr(row[index]).replace("'","")
                        sub_item.replace('"','')
                        items = [sub_item]
                        First_sub_item = False
                    else:
                        if item != '':
                            sub_item = repr(row[index]).replace("'", "")
                            sub_item.replace('"', '')
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
All_picture_files = Extract(import_txt(File_With_all_files))

All_picture_filenames_recovered = SfaF.getListOfFiles(Folder_With_all_files)

#print(*All_picture_files,sep='\n')
#print(*All_picture_files,sep='\n')
#print(*All_picture_filenames_recovered,sep= '\n')

print('Starting Scanning procedure')

recovered_files = 0
Unrecovered_files = 0

recovered_files_list = list()
Unrecovered_files_list = list()
All_picture_files_length = len(All_picture_files)

start_time = time.time()
estimated_time = 0

for index,file in enumerate(All_picture_files):
    if file in All_picture_filenames_recovered:
        recovered_files +=1
        recovered_files_list.append(file)
    else:
        Unrecovered_files +=1
        Unrecovered_files_list.append(file)
    elapsed_time = time.time() - start_time
    completion_percentage = (1+index) / All_picture_files_length
    estimated_time = (estimated_time + (elapsed_time/ (completion_percentage / 100))) / 2
    #print(str(index)+'/'+str(All_picture_files_length))
    #print(str(completion_percentage) + '%  Elapsed time = ' + str(round(elapsed_time, 2)) + ' s   Estimated Time = ' + str(round(estimated_time, 2)))
    print(str(recovered_files)+' Recovered files and '+str(Unrecovered_files) + ' unrecovered files from ' + str(All_picture_files_length))
    if index >= 100:
        break

print(*Unrecovered_files_list,sep='\n')
print(str(Unrecovered_files)+' Unrecovered Files')
