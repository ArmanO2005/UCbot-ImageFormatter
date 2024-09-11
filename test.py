import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C://Users//arman//UCbot-ImageFormatter//Tesseract-OCR//tesseract.exe"
print(pytesseract.image_to_string("C://Users//arman//Dropbox//UC_Botanical_Garden//Quercus_agrifolia_71.0163//IMG_5126.jpg", config='--psm 11'))