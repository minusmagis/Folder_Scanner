from PIL import Image,ImageFile
import shutil
import os
import time
import rawpy
import imageio

def Extract(list_to_extract_from,column_to_extract = 0):
    return [item[column_to_extract] for item in list_to_extract_from]

def Check_if_Grayscale(Colors_list):
    color_values = Extract(Colors_list,1)
    for index,value in enumerate(color_values):
        if value[0] != value[1] or value[0] != value[2] or value[2] != value[1]:
            return False
        elif index > 15:
            return True
    return True

def Extract_image_by_size(Image_file,Image_Width,Image_Height):
    img = Image.open(Image_file)
    img_width, img_height = img.size
    img.close()
    if img_width == Image_Width and img_height == Image_Height:  # extract certain size images
        return True, 'Selected image'
    else:
        return False, 'No error found'

def Image_corrupt_check(Image_file,Supposed_file_extension,Acceptance_factor = 0.75,Full_scan = True):
    if Supposed_file_extension.casefold() == '.nef':
        try:
            with rawpy.imread(Image_file) as raw:
                img = raw.postprocess()
        except Exception as e:
            # print(e)
            return True, 'Data Corrupted'
        return False,'No error found'
    else:
        start_time = time.time()
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        img_width = 0
        img_height = 0
        clrs = list()
        Exc = 'No error'
        try:
            img = Image.open(Image_file)
            img.verify()
            img.close()
        except Exception as Exc:
            #print(Exc)
            try:
                img.close()
            except:
                pass
            return True,Exc
        # first_step_time = time.time() - start_time
        if Full_scan:
            try:
                img = Image.open(Image_file)
                Image_file_extension = img.format.casefold()
                #print(Image_file_extension)
                if Image_file_extension.casefold() == 'jpeg':
                    Image_file_extension = 'jpg'
                Image_file_extension = '.'+Image_file_extension
                img.close()
                if Image_file_extension.casefold() != Supposed_file_extension.casefold():
                    if Image_file_extension.casefold() != '.tiff' and Image_file_extension.casefold() != '.jpeg' and Image_file_extension.casefold() != '.jpg' and Image_file_extension.casefold() != '.raw' and Image_file_extension.casefold() != '.dsc' and Image_file_extension.casefold() != '.nef' and Image_file_extension.casefold() != '.tiff':
                        return True,'Different file extension indecates overwritten file. Found extension %s' % Image_file_extension

            except:
                return False, 'Unknown error'
            # second_step_time =  time.time() - start_time
            try:
                img = Image.open(Image_file)
                clrs = img.getcolors()
                # bands = img.getbands()
                # print(len(img.histogram()))
                # print(clrs)
                # print(bands)
                img_width,img_height = img.size
                # print(img_width*img_height)
                img.close()
                # second_and_a_half_step = time.time() - start_time
                if clrs == None:
                    #print('No colors found')
                    pass
                else:
                    if isinstance(clrs,list):
                        if len(clrs) == 1:
                            #print('it is corrupted')
                            return True,'It only has one color'
                    if not Check_if_Grayscale(clrs):
                        if (max(Extract(clrs))/(img_width*img_height)) > Acceptance_factor:
                            return True, 'More than the acceptance factor of the image is the same color'
            except Exception as Exc:
                try:
                    #print(Exc)
                    img.close()
                except:
                    pass
                if 'cannot load this image' in repr(Exc):
                    return True,Exc
                elif '-2' in repr(Exc):
                    return True, Exc
                else:
                    return False,Exc
            # third_step_time = time.time() - start_time
            #print('First step time = '+str(first_step_time)+'  Second step time = '+str(second_step_time)+'   Third step time = '+str(third_step_time))
        return False,'No Error found'

def Move_Image_to_Corrupt_folder(Filename, Folder_for_corrupted_files, Filename_without_path):
    try:
        shutil.move(Filename, os.path.join(Folder_for_corrupted_files,Filename_without_path))
        return True, 'Moved Successfully'
    except Exception as Exc:
        return False, Exc