"""
.. module:: GenreScraper
    :synopsis: Scrapes details of most popular books in a particular genre

.. moduleauthor:: DivyenduDutta

Functions:
    
- `_create_main_parser(genre)`
- `_build_book_details_map((sci_fi_book_details, book_index, book_details))`
- `_retrieve_book_name(book_block, class_name)`
- `_retrieve_book_URL_and_image_URL(book_block)`
- `_retrieve_author_name(book_block, class_name)`
- `_retrieve_number_of_times_shelved(book_block)`
- `_retrieve_rating_published_details(book_block)`
- `retriveSciFiBookList(genre)`

"""
import requests
from bs4 import BeautifulSoup
import re
import pprint
from FileUtil.FilePicking import save_obj,load_obj


def _create_main_parser(genre):
    """
    Creates the bs4 parser from the goodreads URL. This is to scrape details
    of most popular books in a genre
    
    
    Args:
        genre (str) : Genre to scrape book details
        
    Returns:
        bs4 object : parser
    """
    urlToScrape = 'https://www.goodreads.com/shelf/show/'+genre
    print('Scraping details of '+genre+' genre')
    page = requests.get(urlToScrape)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def _build_book_details_map(sci_fi_book_details, book_index, book_details):
    """
    Build the dictionary containing the details of the book.
    This is then further pickled for persistent storage
    
    
    Args:
        sci_fi_book_details (dict) : dictionary to store book details
        book_index (int) : counter variable for the dictionary `sci_fi_book_details`
        book_details (list) : List containing the different details about the book
        that needs to be stored in the dict `sci_fi_book_details`
    
    Returns:
        dict : book details
    """
    sci_fi_book_details[book_index]['book_name'] =  book_details[0]
    sci_fi_book_details[book_index]['book_URL'] = book_details[1]
    sci_fi_book_details[book_index]['book_img_URL'] = book_details[2]
    sci_fi_book_details[book_index]['author'] = book_details[3]
    sci_fi_book_details[book_index]['shelved'] = book_details[4]
    sci_fi_book_details[book_index]['avg_rating'] = book_details[5]
    sci_fi_book_details[book_index]['number_of_ratings'] = book_details[6]
    sci_fi_book_details[book_index]['published_year'] = book_details[7]
    return sci_fi_book_details

def _retrieve_book_name(book_block, class_name):
    """
    Finds the book name which is in a link <a> tag
    
    Args:
        book_block (bs4) : represents the bs4 for an individual book on the webpage
        class_name (str) : the CSS class name needed to extract the book name
        
    Returns:
        str : name of the book
    """
    book_name_link_tag = book_block.find('a', class_= class_name)
    if book_name_link_tag != None:
        return book_name_link_tag.find(text = True).encode('utf-8')
    
def _retrieve_book_URL_and_image_URL(book_block):
    """
    Finds the book URL (which we use in :mod: `web_scraper_goodreads_root.BookReviews`)
    and book image URL
    
    Args:
        book_block (bs4) : represents the bs4 for an individual book on the webpage
    
    Returns:
        list : book url and book image url
    """
    #leftAlignedImage links to the book URL and image itself
    book_URL_link_tag = book_block.find('a', class_= "leftAlignedImage")
    book_url = 'https://www.goodreads.com'+book_URL_link_tag['href'].encode('utf-8') #can just do this to get value of an attribute
    book_img_url = book_URL_link_tag.find('img')['src'].encode('utf-8')
    return [book_url, book_img_url]

def _retrieve_author_name(book_block, class_name):
    """
    Finds the author details of the book
    Author details are:
    -author name
    -Goodreads author URL
    -is author on goodreads or not
    
    Args:
       book_block (bs4) : represents the bs4 for an individual book on the webpage
       class_name (str) : the CSS class name needed to extract the book name
       
    Returns:
        list : author details
    """
    author_name_div_tag = book_block.find('div', class_= class_name)
    author_name_link_tag = author_name_div_tag.find('a', class_ = 'authorName')
    author_details = {}
    
    author_name = author_name_link_tag.find('span').find(text = True).encode('utf-8')
    author_URL = author_name_link_tag['href'].encode('utf-8')
    
    goodreads_author_tag = author_name_div_tag.find('span', class_ = "greyText")
    if goodreads_author_tag != None:
        is_author_goodreads = True
    else:
        is_author_goodreads = False
    
    author_details['author_name'] = author_name
    author_details['author_URL'] = author_URL
    author_details['goodreads_author'] = is_author_goodreads
    
    return author_details

def _retrieve_number_of_times_shelved(book_block):
    """
    Finds the number of times a book has been shlved by people
    Shelving is just a way for users of goodreads to categorize a book
    
    Args:
        book_block (bs4) : represents the bs4 for an individual book on the webpage
        
    Returns:
        int : number of times shelved
    """
    shelf_link_tag = book_block.find('a', class_ = "smallText")
    if shelf_link_tag != None:
        shelf_text = shelf_link_tag.find(text = True)
        shelvedRegex = re.compile(r'\d+')
        number_of_times_shelved = shelvedRegex.search(shelf_text).group().encode('utf-8')
    else:
        number_of_times_shelved = 0
    
    return number_of_times_shelved

def _retrieve_rating_published_details(book_block):
    """
    Finds rating details of the book
    Rating details include:
    -average rating
    -number of ratings
    -year the book was published
        
    Args:
        book_block (bs4) : represents the bs4 for an individual book on the webpage
        
    Returns:
        list : rating details
    """
    rating_published_span_tag = book_block.select('span.greyText.smallText')[0]
    rating_published_text = rating_published_span_tag.find(text = True).encode('utf-8')
    #Avg Rating
    ratingRegex = re.compile(r'avg rating \d+.\d+')
    avg_rating = ratingRegex.search(rating_published_text).group().split(' ')[2]

    #number of ratings
    numberofratingsRegex = re.compile(r'\d+,\d+ ratings')
    number_of_ratings = numberofratingsRegex.search(rating_published_text).group().split(' ')[0]
    
    #published year
    yearPublishedRegex = re.compile(r'published \d\d\d\d')
    published_year = yearPublishedRegex.search(rating_published_text).group().split(' ')[1]
    
    return [avg_rating, number_of_ratings, published_year]
    
def retriveSciFiBookList(genre):
    """
    Main entry into `GenreScraper`
    This function does the following:
        1. Creates the bs4 parser - `_create_main_parser(genre)`
        2. Gets a list of bs4 for each of the books
        3. Loops through each book, retrives the book details and stores in dict
           `sci_fi_book_details`
           
    Args:
        genre (str) : genre to scrape details about
        
    Returns:
        dict : book details from a particular genre
    """
    print('Web scraping started....')
    #root_book_blocks = soup.findAll(attrs={'id' : re.compile("^bookCover")})
    #get the html blocks which lists books
    soup = _create_main_parser(genre)
    root_book_blocks = soup.findAll('div', class_="elementList")
    sci_fi_book_details = {} #main map of book details
    
    #print(type(root_book_blocks))
    book_index = 0
    for book_block in root_book_blocks:
        #get the name of the book
        book_name = _retrieve_book_name(book_block, "bookTitle")
        if book_name != None:
            sci_fi_book_details[book_index] = {}
            book_details = [] #add book details to this list
            book_details.append(book_name)
            
            #get the URL for the book
            book_URL_and_img_URL = _retrieve_book_URL_and_image_URL(book_block)
            book_details.append(book_URL_and_img_URL[0])
            book_details.append(book_URL_and_img_URL[1])
            
            #get the author name
            author_details = _retrieve_author_name(book_block, "authorName__container")
            book_details.append(author_details)
            
            #get number of times shelved
            number_of_times_shelved = _retrieve_number_of_times_shelved(book_block)
            book_details.append(number_of_times_shelved)
            
            #get rating and published date
            rating_published_details = _retrieve_rating_published_details(book_block)
            book_details.append(rating_published_details[0])
            book_details.append(rating_published_details[1])
            book_details.append(rating_published_details[2])
            
            sci_fi_book_details = _build_book_details_map(sci_fi_book_details, book_index, book_details)
            
            book_index += 1
        else:
            print('No book name. No book')
    
    #pp = pprint.PrettyPrinter(indent=4)
    #print(pp.pprint(sci_fi_book_details))
    print('Web scraping stop....')
    return sci_fi_book_details

if __name__ == "__main__":
   #executed when invoked directly
   genre = 'science-fiction'
   sci_fi_book_details = retriveSciFiBookList(genre)
   save_obj(sci_fi_book_details, 'sci-fi-books-list', 'Data')
   
   sci_fi_list = load_obj('sci-fi-books-list', 'Data')
   print(sci_fi_list)
else:
    #executed when imported
    pass