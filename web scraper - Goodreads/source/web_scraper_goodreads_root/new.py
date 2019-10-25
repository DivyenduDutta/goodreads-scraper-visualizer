"""
.. module:: useful_1
    :synopsis: Main entry file into the Goodreads book review scraping and visualization code

:synopsis: Main entry file into the Goodreads book review scraping and visualization code

Functions:
    
- `generate_book_review_images()` : Scrapes goodreads.com for reviews and visualizes data
"""

def generate_book_review_images(genre):
    """
    Does the following:
        1. Scrapes goodreads.com to get most popular book details for input `genre`
        2. Saves details to pickle file
        3. Loads the latest pickle file data
        4. Loops through the book list to:
            - extract book name from book URL
            - scrape book review details 
            - save details to pickle file
            - load latest pickle file data
            - visualize review likes data
        
        Parameters:
            
        - `genre`: book genre to process
    
    .. note:: asdasdasdsda
    """
    #Run the genre scraper and retrive book details for that genre
    
    print('*'*15)