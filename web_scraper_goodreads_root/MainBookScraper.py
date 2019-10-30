# -*- coding: utf-8 -*-
"""
.. module:: MainBookScraper
    :synopsis: Main entry file into the Goodreads book review scraping and visualization code

.. moduleauthor:: DivyenduDutta

Functions:
    
- `generate_book_review_images()` : Scrapes goodreads.com for reviews and visualizes data
"""
from GenreScraper import retriveSciFiBookList
from FileUtil.FilePicking import save_obj, load_latest_obj
from BookReviews import retrieve_book_review_details
from HelperUtils import extract_book_name_from_root_url
from book_review_visualization import visualize_and_save_review_information
from HelperUtils import data_for_book_exists_current_date
from selenium.common.exceptions import TimeoutException
from CommonConstants.Constants import FAILURE_THRESHOLD
from YALogger.custom_logger import Logger

# initailize the YALogger
Logger.initialize_logger(
    logger_prop_file_path=".\logger.properties", log_file_path="./logs"
)


def generate_book_review_images(genre):
    """
    Does the following:
        
        1. Scrapes goodreads.com to get list of most popular book & details for input `genre`
        2. Saves details to pickle file
        3. Loads the latest pickle file data
        4. Loops through the book list to:
            - extract book name from book URL
            - scrape book review details 
            - save details to pickle file
            - load latest pickle file data
            - visualize review likes data
        
        Args:
            genre (str): book genre to process
        
    .. note:: When there is a timeout exception during scraping, `generate_book_review_images` 
              function will retry upto `FAILURE_THRESHOLD` from :mod:`web_scraper_goodreads_root.CommonConstants.Constants` times before skipping the book
    """
    # Run the genre scraper and retrive book details for that genre
    sci_fi_book_details = retriveSciFiBookList(genre)
    # print('*'*15)
    # Save the details to pkl file
    save_obj(sci_fi_book_details, "sci-fi-books-list", "Data", True)
    # Read the latest pickle file
    sci_fi_list = load_latest_obj("sci-fi-books-list", "Data")
    book_index = 0
    failure_threshold_index = 0
    while True:
        try:
            while book_index < len(sci_fi_list):
                book_url = sci_fi_list[book_index]["book_URL"]
                # get the review details for the book
                book_name = extract_book_name_from_root_url(book_url)
                # print('*'*15)
                Logger.log(
                    "info",
                    "MainBookScraper",
                    "generate_book_review_images",
                    "Processing " + book_name + " book",
                )
                if not data_for_book_exists_current_date("Data/" + book_name):
                    # Iterate through each book in the genre
                    book_review_details = retrieve_book_review_details(
                        book_url, new_book=True
                    )

                    # save the book details
                    save_obj(
                        book_review_details,
                        "book_review_details",
                        "Data/" + book_name,
                        True,
                    )
                    # load the latest pkl file having review details
                    book_review = load_latest_obj(
                        "book_review_details", "Data/" + book_name
                    )

                    # Visualize the info and save it in system
                    visualize_and_save_review_information(book_review, book_name)
                else:
                    Logger.log(
                        "error",
                        "MainBookScraper",
                        "generate_book_review_images",
                        "Book details "
                        + book_name
                        + " already present in current date...skipping",
                    )
                # print('*'*15)
                book_index += 1
            if book_index >= len(sci_fi_list):
                Logger.log(
                    "info",
                    "MainBookScraper",
                    "generate_book_review_images",
                    "All books processed...",
                )
                break
        except TimeoutException as e:
            book_name = extract_book_name_from_root_url(
                sci_fi_list[book_index]["book_URL"]
            )
            failure_threshold_index += 1
            if failure_threshold_index > FAILURE_THRESHOLD:
                Logger.log(
                    "error",
                    "MainBookScraper",
                    "generate_book_review_images",
                    "Skipping "
                    + book_name
                    + " since it hit exception more than threshold limit",
                )
                failure_threshold_index = 0
                book_index += 1
            else:
                Logger.log(
                    "error",
                    "MainBookScraper",
                    "generate_book_review_images",
                    "********Timeout Exception while processing book -->"
                    + repr(e)
                    + "***********",
                )
                Logger.log(
                    "error",
                    "MainBookScraper",
                    "generate_book_review_images",
                    "Retrying to process book again..." + book_name,
                )


if __name__ == "__main__":
    genre = "science-fiction"
    Logger.perform_method_entry_logging(
        "MainBookScraper", "generate_book_review_images"
    )
    generate_book_review_images(genre)
    Logger.perform_method_exit_logging("MainBookScraper", "generate_book_review_images")
