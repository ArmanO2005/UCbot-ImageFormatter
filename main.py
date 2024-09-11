# folder naming format for the program to work properly is 'Genus_species_accession#'.

import os
from PIL import Image
from pillow_heif import register_heif_opener
import pytesseract
import cv2
import numpy as np


pytesseract.pytesseract.tesseract_cmd = r"C://Users//arman//UCbot-ImageFormatter//Tesseract-OCR//tesseract.exe"
register_heif_opener()


print("What are your initials? ([first initial][last initial] i.e. AO if my first name starts with A and last name ")
print("starts with O")
RInitial = str(input("Initials: "))
RInitial = '_'+RInitial+'_'


print("Enter the file path you want to edit below. You should follow the 'Genus_species_accession#' naming format for ")
print("your file. To find the file path of your file, go to the file you want to edit in your file explorer, ")
print("right click, and select 'Copy as path'")
RInput = input("File path: ").replace('"', '') + '\\'


def convertToJPG(directory):
    for filename in os.listdir(directory):
        image = Image.open(os.path.join(directory, filename))
        image.convert('RGB').save(os.path.join(directory, os.path.splitext(filename)[0] + '.jpg'))
        if os.path.splitext(filename)[1] == '.HEIC':
            os.remove(os.path.join(directory, filename))

def readTag(directory):
    for filename in os.listdir(directory):
        # print(pytesseract.image_to_string(Image.open(os.path.join(directory, filename)), config="--psm 11"))
        img = cv2.imread(os.path.join(directory, filename))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(gray,50,255,0)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        img_area = img.shape[0] * img.shape[1]

        for cnt in contours:
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
            if len(approx) == 4:
                area = cv2.contourArea(cnt)
                if area > 0.85 * img_area:
                    print(True)
                    print(filename)


def namePics(directory, initials):
    accession = str(directory.split('\\')[-2]).rpartition('_')[2] + '_'
    name = initials + str(directory.split('\\')[-2]).rpartition('_')[0]

    i = 0
    for filename in os.listdir(directory):
        temp = accession + str(i) + name
        os.rename(os.path.join(directory, filename), (directory + temp + '.jpg'))
        i = i + 1

    for filename in os.listdir(directory):
        if filename.split('_')[1] == '0':
            label_name = filename.replace('_0_', '_Label_')
            os.rename(os.path.join(directory, filename), os.path.join(directory, label_name))
            

def indivFormatter(directory, initials):
    convertToJPG(directory)
    readTag(directory)
    # namePics(directory, initials)


def massFormatter(initial, folder):
    checkr = []
    for item in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, item)):
            checkr.append(True)
        else:
            checkr.append(False)
    if all(checkr):
        for item in os.listdir(folder):
            indivFormatter(initial, (os.path.join(folder, item) + '\\'))
    elif not any(checkr):
        indivFormatter(folder, initial)


massFormatter(RInitial, RInput)