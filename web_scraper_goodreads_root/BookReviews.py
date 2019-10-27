# -*- coding: utf-8 -*-
"""
.. module:: BookReviews
    :synopsis: Scrapes review details for a particular book

.. moduleauthor:: DivyenduDutta

- `_create_book_review_scraper_from_source(html_source)`
- `_retrieve_review_rating(book_review_tag)`
- `_retrieve_review_likes(first_page_book_review_tag)`
- `_retrieve_review_date(first_page_book_review_tag)`
- `_build_review_rating_map(book_review_details, book_review_index, key, value)`
- `_retrieve_book_review_details_per_page(book_review_details, root_book_review_tags, book_review_index)`
- `retrieve_book_review_details(book_url, new_book)`
"""
from bs4 import BeautifulSoup
import sys
from CommonConstants.Constants import (GOODREADS_REVIEW_RATING, ROOT_URL)
from SiteNavigator import get_html_code_for_first_page, get_html_code_for_other_pages
from HelperUtils import extract_book_name_from_root_url
from FileUtil.FilePicking import save_obj
from FileUtil.FilePicking import load_obj
from book_review_visualization import visualize_and_save_review_information
from YALogger.custom_logger import Logger


#Not using this to scrape the first page, using selenium for it now
#def create_book_review_scraper():
#    root_book_url = ROOT_URL
#    book_page = requests.get(root_book_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'})
#    soup = BeautifulSoup(book_page.text, 'html.parser')
#    return soup

def _create_book_review_scraper_from_source(html_source):
    """
    Creates the bs4 parser from the HTML source
    
    Args:
        html_source (str) : html source of the book
        
    Returns:
        bs4 parser
    """
    soup = BeautifulSoup(html_source, 'html.parser')
    return soup

def _retrieve_review_rating(book_review_tag):
    """
    Retrieves the rating given by the review
    Maps to in integer value from `web_scraper_goodreads_root.CommonConstants.Constants`
    
    Args:
       book_review_tag (bs4) : represents the bs4 instance for a particulat review
       
    Returns:
        review rating
    """
    review_rating = ''
    if len(book_review_tag.select('span.staticStars.notranslate')) != 1:
        pass #havent rated it
    else:
        review_rating = book_review_tag.select('span.staticStars.notranslate')[0]['title'].encode('utf-8')
    return GOODREADS_REVIEW_RATING[review_rating]

def _retrieve_review_likes(first_page_book_review_tag):
    """
    Retrieves the number of likes on the review
    
    Args:
        first_page_book_review_tag (bs4) : represents the bs4 instance for a particulat review
    
    Returns:
        review likes
    """
    try:
        likes_text = first_page_book_review_tag.find('span', class_ = 'likesCount').text.encode('utf-8')
        if 'likes' in likes_text:
            likes = int(likes_text[:-len('likes')])
        else:
            likes = int(likes_text[:-len('like')])
    except AttributeError:
        Logger.log('info', 'BookReviews','_retrieve_review_likes','returning 0 likes')
        likes = 0
    return likes
    
def _retrieve_review_date(first_page_book_review_tag):
    """
    Retrieves the review date
    
    Args:
        first_page_book_review_tag (bs4) : represents the bs4 instance for a particulat review
        
    Returns:
        date when the review was posted
    """
    if len(first_page_book_review_tag.select('a.reviewDate.createdAt.right')) > 0:
        return first_page_book_review_tag.select('a.reviewDate.createdAt.right')[0].text
    else:
        first_page_book_review_tag.select('a.reviewDate')[0].text

def _build_review_rating_map(book_review_details, book_review_index, key, value):
    """
    Build the dict `book_review_details`
    
    Args:
        book_review_details (dict) : the book review details
        book_review_index (int) : counter variable for the books
        key (str) : key used in dict `book_review_details`
        value (str) : value used in dict `book_review_details`
        
    Returns:
        details of the reviews for a book
    """
    book_review_details[book_review_index][key] = value
    return book_review_details

def _retrieve_book_review_details_per_page(book_review_details, root_book_review_tags, book_review_index):
    """
    This functions is the main driver function for all other functions in this file
    Retrieves details of the book which include:
    - rating of the book by the review
    - likes on the review
    - date of the review
        
    Args:
        book_review_details (dict) : the book review details
        root_book_review_tags (bs4) : bs4 instance for a particular review
        book_review_index (int) : counter variable for the books
    
    Returns:
    - details of the reviews
    - which book number was processed
    """
    first_page_book_review_tags = root_book_review_tags.select('div.friendReviews.elementListBrown')
    for first_page_book_review_tag in first_page_book_review_tags:
        book_review_details[book_review_index] = {}
        review_rating = _retrieve_review_rating(first_page_book_review_tag)
        review_likes = _retrieve_review_likes(first_page_book_review_tag)
        review_date = _retrieve_review_date(first_page_book_review_tag)
        if review_rating != 0:
            book_review_details = _build_review_rating_map(book_review_details, book_review_index, 'review_likes', review_likes)
            book_review_details = _build_review_rating_map(book_review_details, book_review_index, 'review_rating', review_rating)
            book_review_details = _build_review_rating_map(book_review_details, book_review_index, 'review_date', review_date)
            book_review_index += 1
            
    return book_review_details, book_review_index
    

def retrieve_book_review_details(book_url, new_book):
    """
    Main entry function into this file's code
    Also handles the progress bar
    Basically this function scrapes review data from the first page and then visits
    each of the review pages and scrapes review data from them
    
    Args:
        book_url (str) : URL of the book
        new_book (bool) : indicates whether its a new book or not
        
    Returns:
        review details of the book
    """
    Logger.log('info', 'BookReviews','retrieve_book_review_details','Book Review Scraping started...')
    book_review_details = {}
    book_review_index = 0
    #first for the first page
    Logger.log('info', 'BookReviews','retrieve_book_review_details','Scraping review data from first page started...')
    root_book_review_html = get_html_code_for_first_page(book_url, new_book)
    new_book = False
    root_book_review_tags = _create_book_review_scraper_from_source(root_book_review_html)
    book_review_details, book_review_index = _retrieve_book_review_details_per_page(book_review_details, root_book_review_tags, book_review_index)
    Logger.log('info', 'BookReviews','retrieve_book_review_details','Scraping review data from first page done...')
    Logger.log('info', 'BookReviews','retrieve_book_review_details','Scraping review data from other pages...')
    is_next_page_there = True
    
    #progress bar code
    # setup toolbar
    sys.stdout.write("[")
    sys.stdout.flush()
    
    while True:
        #print('Scraping review data from page started...')
        is_next_page_there, html_source, current_page = get_html_code_for_other_pages(book_url)
        if is_next_page_there == False:
            break
        else:
            book_review_scraper_per_page = _create_book_review_scraper_from_source(html_source)
            root_book_review_tags = book_review_scraper_per_page.find('div', attrs={"id":"bookReviews"})
            #for other pages
            book_review_details, book_review_index = _retrieve_book_review_details_per_page(book_review_details, root_book_review_tags, book_review_index)
        sys.stdout.write("###")
        sys.stdout.flush()
        #print('Scraping review data from page done...\n')
        
    sys.stdout.write("]\n") # this ends the progress bar
    Logger.log('info', 'BookReviews','retrieve_book_review_details','Book Review Scraping stopped...')
    return book_review_details

if __name__ == "__main__":
     pass
#    uncomment below for dev purposes
#    book_url = ROOT_URL
#    book_review_details = retrieve_book_review_details(book_url, True)
#    book_name = extract_book_name_from_root_url(book_url)
#    save_obj(book_review_details, 'book_review_details', 'Data/'+book_name)
#    book_review = load_obj('book_review_details', 'Data/'+book_name)
#    #Visualize the info and save it in system
#    visualize_and_save_review_information(book_review, book_name)
#    print(book_review)