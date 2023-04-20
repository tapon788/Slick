import os
import time
import shutil
import platform

""" Setting up linux/windows platform variants """
def get_path_seperator():
    if platform.system() == "Windows":
        return '\\'
    return '/'

""" Cleans a directory. If not exists, creates it. Otherwise, removes it's contents """
def clean_dir(path):
    # Checking if backup folder already exists or not. If not exists will create it.
    print ("Cleaning "+path)
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        for f in os.listdir(path):
            os.remove(path+get_path_seperator()+f)


