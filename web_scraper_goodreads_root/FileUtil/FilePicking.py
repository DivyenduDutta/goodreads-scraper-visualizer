# -*- coding: utf-8 -*-
"""
.. module:: FilePicking
    :synopsis: Functions for pickling and unpickling python objects

.. moduleauthor:: DivyenduDutta

- `save_obj(obj, name, directory )`
- `load_obj(name, directory )`
- `load_latest_obj(name, directory)`
"""
import pickle
import os
import glob
from os import path
from datetime import datetime
import shutil
from HelperUtils import data_for_book_exists_current_date
from YALogger.custom_logger import Logger


def save_obj(obj, name, directory):
    """
    Functions checks if the individual book directory exists as of current date
    If it does'nt exist then it creates it otherwise it deletes the older directory and recreates it
    Pickles and saves the `obj` with the name `name` in dir `directory`
    
    Args:
        obj (python object) : this is being pickled
        name (str) : name with which to save the .pkl file
        directory (str) : name of the directory where the .pkl file is saved
    """
    directory_path = os.getcwd() + "/" + directory + "/"
    if directory != "Data":
        if not data_for_book_exists_current_date(directory_path):
            if not path.exists(directory_path):
                os.mkdir(directory_path)
            else:
                while os.path.isdir(directory_path):
                    shutil.rmtree(directory_path, ignore_errors=True)
                os.mkdir(directory_path)
    else:
        if not path.exists(directory_path):
            os.mkdir(directory_path)

    timestamp = datetime.now().strftime("%Y-%m-%d")
    full_data_file_path = directory_path + name + "_" + timestamp + ".pkl"
    if path.exists(full_data_file_path) == False:
        with open(full_data_file_path, "wb") as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    else:
        Logger.log(
            "error", "FilePickling", "save_obj", full_data_file_path + " already exists"
        )


def load_obj(name, directory):
    """
    Loads the .pkl file named `name` from `directory`
    
    Args:
        name (str) : name with which to load the .pkl file
        directory (str) : name of the directory where the .pkl file is saved 
    """
    directory_path = os.getcwd() + "/" + directory + "/"
    timestamp = datetime.now().strftime("%Y-%m-%d")
    full_data_file_path = directory_path + name + "_" + timestamp + ".pkl"
    if path.exists(full_data_file_path) == True:
        with open(full_data_file_path, "rb") as f:
            return pickle.load(f)
    else:
        raise IOError(full_data_file_path + " doesnt exist")


def load_latest_obj(name, directory):
    """
    Loads the latest .pkl file from a book directory
    
    Args:
        name (str) : name with which to save the .pkl file
        directory (str) : name of the directory where the .pkl file is saved
    """
    directory_path = os.getcwd() + "/" + directory + "/*.pkl"  # all pickle files
    list_of_files = glob.glob(directory_path)
    latest_file = max(list_of_files, key=os.path.getctime)
    with open(latest_file, "rb") as f:
        return pickle.load(f)
