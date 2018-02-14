import zipfile

zFile = zipfile.ZipFile('/Users/Johnson/Imagine/Crack_Zip_Pass/test.zip')

zFile.extractall(path='/Users/Johnson/Imagine/Crack_Zip_Pass/test',\
	pwd='123'.encode('utf-8'))