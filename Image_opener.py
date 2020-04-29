from PIL import Image,ImageFile
from tkinter import filedialog
import Is_Image_corrupt as IcC

ImageFile.LOAD_TRUNCATED_IMAGES = True

Image_file = filedialog.askopenfilename(initialdir = r"C:\Users\minus\Desktop\Newly recovered files\test folder",title = "Select the image file which you want to check")

print(IcC.Image_corrupt_check(Image_file,'.jpg'))




