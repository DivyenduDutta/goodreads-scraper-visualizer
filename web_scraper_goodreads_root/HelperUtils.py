# -*- coding: utf-8 -*-
"""
.. module:: HelperUtils
    :synopsis: Various helper utility functions

.. moduleauthor:: DivyenduDutta

- `extract_book_name_from_root_url(root_url)`
- `check_if_file_exists_otherwise_handle(file_path)`
- `data_for_book_exists_current_date(book_data_folder)`
"""
import re
import os
from os import path
import datetime
from datetime import date
from YALogger.custom_logger import Logger


def extract_book_name_from_root_url(root_url):

    book_name = re.split(r"/", root_url)[5]  # 5 so it'll only work with goodreads URLs
    book_name = book_name.replace(".", "_")
    return book_name


def check_if_file_exists_otherwise_handle(file_path):
    """
    This function checks if the path file exists in the path
    If it doesnt then returns false and if it exists then deletes it and returns true
    
    Args:
        file_path (str) : path of the file to check
        
    Returns:
        bool flag indicating whether file exists or not
    """
    full_file_path = os.getcwd() + "/" + file_path
    if path.exists(full_file_path):
        file_exists = True
        Logger.log(
            "info",
            "HelperUtils",
            "check_if_file_exists_otherwise_handle",
            "Deleting previously existing file -->" + full_file_path,
        )
        os.remove(full_file_path)
    else:
        file_exists = False

    return file_exists


def data_for_book_exists_current_date(book_data_folder):
    """
    Checks whether a folder exists and if its creation is the current date or not
    
    Args:
       book_data_folder (str) : folder name/partial path
       
    Returns:
        bool flag indicating whether folder exists or not
    """
    full_folder_path = os.getcwd() + "/" + book_data_folder
    current_date = datetime.date.today()
    if (
        not path.exists(full_folder_path)
        or date.fromtimestamp(os.stat(full_folder_path).st_ctime) != current_date
    ):
        return False
    else:
        return True
    
