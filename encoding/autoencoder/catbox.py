import requests
import datetime
import os
import re
import sys
from urllib.parse import urlparse
import time
from datetime import timedelta


def upload(folder):
    folderList = []
    folderName = ""
    fileList = []
    uploadedList = []
    deleteFileList = []
    deleteFolderList = []
    file = ''
    fileToFolder = ''
    fileToDelete = ''
    folderToDelete = ''
    
    rootdir = os.getcwd() + '\\' + folder
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            folderList.append(d)
            
    currentFolder = 0
    while currentFolder < len(folderList):
        fileList = os.listdir(folderList[currentFolder])
        currentFile = 0
        while currentFile < len(fileList):
            file = folderList[currentFolder] + '\\' +fileList[currentFile]
            host = "https://catbox.moe/user/api.php"
            origname = file
            if(re.match(r"^.*\.webm$", file)):
                mime_type = "video/webm"
                ext = ".webm"
            elif(re.match(r"^.*\.mp4$", file)):
                mime_type = "video/mp4"
                ext = ".mp4"                   
            elif(re.match(r"^.*\.mp3$", file)):
                mime_type = "audio/mpeg"
                ext = ".mp3"   
            elif(re.match(r"^.*\.jpg$", file)):
                mime_type = "image/jpeg"
                ext = ".jpg"
            elif(re.match(r"^.*\.jpeg$", file)):
                mime_type = "image/jpeg"
                ext = ".jpeg"
            elif(re.match(r"^.*\.png$", file)):
                mime_type = "image/png"
                ext = ".png"
            elif(re.match(r"^.*\.gif$", file)):
                mime_type = "image/gif"
                ext = ".gif"            
            else:
                return None
            if userhash:
                payload = {'reqtype': 'fileupload', 'userhash': userhash}
            else:
                payload = {'reqtype': 'fileupload'}
            timestamp = str(int(datetime.datetime.now().timestamp()))
            file = "temp" + timestamp + ext
            os.rename(origname, file)  # fixes special character errors
            f = open(file, 'rb')
            files = {'fileToUpload': (file, f, mime_type)}
            response = requests.post(host, data=payload, files=files)
            f.close()
            os.rename(file, origname)
            if response.ok:
                print("picture upload success: %s" % response.text)
                a = urlparse(response.text)
                uploadedList.append(os.path.basename(a.path))
                deleteFileList.append(os.path.basename(a.path))
                #print (os.path.basename(a.path))
            else:
                print("upload failed: %s" % response.text)            
            currentFile += 1

        fileToFolder = ' '.join(uploadedList)
        payload = {'reqtype': 'createalbum', 'userhash': userhash, 'title': os.path.basename(folderList[currentFolder]), 'desc': os.path.basename(folderList[currentFolder])+ "'s folder", 'files' : fileToFolder}
        response = requests.post(host, data=payload)
        if response.ok:
            print()
            print("folder creation success: %s" % response.text)
            print()
            a = urlparse(response.text)
            deleteFolderList.append(os.path.basename(a.path))            
            f = open("uploaded.txt", "a")
            f.write(os.path.basename(folderList[currentFolder]) + ' - ' + response.text + '\n')
            f.close()            
        else:
            print("upload failed: %s" % response.text) 
        uploadedList.clear()
        currentFolder += 1  
        
    
    fileToDelete = ' '.join(deleteFileList)
    f = open("deleteFiles.txt", "a")
    f.write(fileToDelete)
    f.close()   
    
    folderToDelete = ' '.join(deleteFolderList)
    f = open("deleteFolders.txt", "a")
    f.write(folderToDelete)
    f.close()       




def deletePics():
    f = open("deleteFiles.txt", "r")
    filesToDelete = f.read()
    f.close()
    
    host = "https://catbox.moe/user/api.php"
    payload = {'reqtype': 'deletefiles', 'userhash': userhash, 'files' : filesToDelete}
    response = requests.post(host, data=payload)
    if response.ok:
        print("deletion was a success: %s" % response.text)         
    else:
        print("delete failed: %s" % response.text)  
        

def deleteAlbum():
    f = open("deleteFolders.txt", "r")
    foldersToDelete = f.read().split(" ")
    f.close()    
    
    host = "https://catbox.moe/user/api.php"
    
    x = 0
    while x < len(foldersToDelete): 
        payload = {'reqtype': 'deletealbum', 'userhash': userhash, 'short' : foldersToDelete[x]}
        response = requests.post(host, data=payload)
        if response.ok:
            print("Album was deleted successfully: %s" % response.text)         
        else:
            print("deletion failed: %s" % response.text)   
        x += 1

def deleteFiles():
    if os.path.exists("deleteFiles.txt"):
        os.remove("deleteFiles.txt")
    else:
        print("The file does not exist") 
        
    if os.path.exists("deleteFolders.txt"):
        os.remove("deleteFolders.txt")
    else:
        print("The file does not exist")
        
    if os.path.exists("uploaded.txt"):
        os.remove("uploaded.txt")
    else:
        print("The file does not exist")      
    


userhash = None
try:
    with open(sys.path[0] + os.sep + "catbox.config") as file:
        match = re.search("userhash" + r"\s?=[ \t\r\f\v]*(.+)$", file.read(), re.I | re.M)
        if match is None:
            print("catbox.py: no userhash present")
        else:
            userhash = match.group(1)
except Exception:
    print("catbox.py: no config file present")




if __name__ == "__main__":
    while True:
        inp = input ("Do you want to: A) Upload Images. B) Delete Images. [A/B]? : ").upper()
        # check if d1a is equal to one of the strings, specified in the list
        if inp in ['A', 'B']:
            # if it was equal - break from the while loop
            break
    # process the input
    if inp == "A": 
        f = input("select the folder to upload ")
        start = time.time()
        upload(f)
        end = time.time()
        sec = end - start
        td = timedelta(seconds=sec)
        print()
        print("Elapsed Time: " + str(td))        
    elif inp == "B": 
        start = time.time()
        deletePics()
        deleteAlbum()
        deleteFiles()
        end = time.time()
        sec = end - start
        td = timedelta(seconds=sec)  
        print()
        print("Elapsed Time: " + str(td))  
