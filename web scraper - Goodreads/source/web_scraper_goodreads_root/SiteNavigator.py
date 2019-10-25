# -*- coding: utf-8 -*-
"""
.. module:: SiteNavigator
    :synopsis: Initializes the selenium object to trraverse goodreads.com

.. moduleauthor:: DivyenduDutta

Functions:

- `_init(root_url)`
- `get_html_code_for_first_page(root_url, new_book)`
- `get_html_code_for_other_pages(root_url)`
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, JavascriptException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

#global object - selenium driver
driver = None

def _init(root_url):
    """
    Creates and initializes selenium object for traversal.
    Running via chromedriver.exe. For this code to work ensure chromedriver.exe
    is on the path. Download from `here <https://chromedriver.chromium.org/downloads>`_
    Making this a headless selenium object via chrome_options
    
    Args:
        root_url (str) : used to initialize selenium object
        
    Returns:
        selenium instance
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
   
    driver = webdriver.Chrome(chrome_options = options)
    driver.get(root_url)
    #print(driver.page_source)
    return driver

def get_html_code_for_first_page(root_url, new_book):
    """
    Visits the first page in a book and returns the HTML code for the book review part
    The `new_book` indicator helps to ensure we recreate the selenium driver instance for every book
    
    Args:
        root_url (str) : used to initialize selenium object
        new_book (bool) : indicates whether its a new book or not
        
    Returns:
        html code of the book reviews
    """
    global driver
    if new_book:
        driver = None
        
    if driver == None:
        print('Creating headless selenium object for first page')
        driver = _init(root_url)
    try:
        first_page = driver.find_element_by_id("bookReviews")
        return first_page.get_attribute('innerHTML')
    except NoSuchElementException:
        print("WARNING: There is no next page!")
        return None  

def get_html_code_for_other_pages(root_url):
    """
    Visits the other review pages and returns the html code
    Cliking on the a review page at the bottom performs an Ajax call which returns
    a Element.update() which in turn updates the "reviews" id with HTML code
    
    The way we check whether the review data has loaded is by adding a dummy id in the HTML
    and waiting till its not present anymore after the Ajax call
    
    Args:
        root_url (str) : used to initialize selenium object
        
    Returns:
        html code of the book reviews
    """
    global driver
    if driver == None:
        print('Creating headless selenium object for other pages') #should never print
        driver = _init(root_url)
    try:
        next_page = driver.find_element_by_class_name("next_page")
#        driver.execute_script(
#                'document.getElementById("reviews").'
#                'insertAdjacentHTML("beforeend", \'<p id="load_reviews">loading</p>\');'
#            )
        if next_page.tag_name == "a":
            # Click the next page button
            #scroll to 20 avoid pointing issues - specific to chrome
            driver.execute_script("window.scrollTo(0, 20)")
            webdriver.ActionChains(driver).move_to_element(next_page).click(next_page).perform()
            #next_page.click()
            driver.execute_script(
                'document.getElementById("reviews").'
                'insertAdjacentHTML("beforeend", \'<p id="load_reviews">loading</p>\');'
                )
#            time.sleep(10)
            WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.ID, "load_reviews")))
#            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "current")))
            current_page = driver.find_element_by_class_name("current")
            #print("Currently parsing review page - "+current_page.text.encode('utf-8'))
            
            return True, driver.page_source, current_page.text.encode('utf-8')
        driver.close()
        return False, None, None
    except JavascriptException:
        print("WARNING: There is no next page!")
        return False, None, None
    

if __name__ == "__main__":
    pass