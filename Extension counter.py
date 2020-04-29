import csv
import tkinter
from tkinter import filedialog
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

File_With_all_recovered_files = filedialog.askopenfilename(initialdir = r"C:\Users\minus\Documents",title = "Select the txt file with the list of recovered files")
File_extension_list = ['.txt','.jpg','.png','.jpeg','.raw','.tif','.bmp','.dsc','.nef','.mp3','.wma','.wav','.m4a','.doc','.ppt','.odt','.pdf','.docx','.pptx','.xlsx','.xls','.avi','.mov','.mpg','.mp4','.flv','.wmv','.zip','.rar','.py','.stl','.gcode','.opj','.opju','.xcf','.ino','.au','.aup','.mts','.apk','.apkg','.3gp','.opus','.mkv','.pfx','.fzz','.fzb','.html','.ttf','.gif','.cer','.crt','.rtf','.h','.cpp','.mus','.sldprt','.f3d','.stp','.mov','.epub','.7z','.swf']

All_files = Extract(import_txt(File_With_all_recovered_files))
count_list = list()
start_time = time.time()
total_count = 0
estimated_time = 0

for index,extension in enumerate(File_extension_list):

    extension_count = 0;
    for file in All_files:
        if extension.casefold() in file.casefold():
            extension_count+=1
    count_list.append([extension,extension_count])
    total_count = total_count+extension_count
    elapsed_time = time.time() - start_time
    completion_percentage = ((1 + index) / len(File_extension_list)) * 100
    estimated_time = (estimated_time + (elapsed_time / (completion_percentage / 100))) / 2
    print(str(completion_percentage) + '%  Elapsed time = ' + str(round(elapsed_time, 2)) + ' s   Estimated Time = ' + str(round(estimated_time, 2)))


count_list = sorted(count_list, key=lambda x: x[1])


print(*count_list,sep='\n')
print(str(total_count)+' Total Count')


