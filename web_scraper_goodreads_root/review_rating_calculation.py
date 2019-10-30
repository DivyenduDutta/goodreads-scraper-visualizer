# -*- coding: utf-8 -*-
"""
.. module:: review_rating_calculation
    :synopsis: Calculates the Bayesian Adjusted Rating for each of the books
    
.. note::
    Reference - https://www.analyticsvidhya.com/blog/2019/07/introduction-online-rating-systems-bayesian-adjusted-rating/

.. moduleauthor:: DivyenduDutta

- `_extract_review_likes_ratings(book_review)`
- `_calculate_simple_avg_review_rating(review_ratings)`
- `_convert_to_bayesian_adj_rating(review_likes, review_ratings)`
- `_calculate_bayesian_adj_rating(bayesian_adj_ratings)`
- `_build_ratings_list(processed_book_review_info)`
- `quicksort(arr_to_be_sorted, start, end)`
- `_process_reviews()`
"""
from __future__ import division
from FileUtil.FilePicking import load_obj, load_latest_obj, save_obj
from YALogger.custom_logger import Logger
from HelperUtils import extract_book_name_from_root_url

Logger.initialize_logger(
    logger_prop_file_path=".\logger.properties", log_file_path="./logs"
)


def _extract_review_likes_ratings(book_review):
    """
    Extracts the likes and ratings from the dict (pkl file)
    
    Args:
        book_review (dict) : details of a book
        
    Returns:
        2 lists : likes and ratings
    """
    review_likes = []
    review_ratings = []
    for review in book_review:
        review_likes.append(book_review[review]["review_likes"])
        review_ratings.append(book_review[review]["review_rating"])
    return review_likes, review_ratings


def _calculate_simple_avg_review_rating(review_ratings):
    """
    Calculates the average rating
    
    Args:
       review_ratings (list) : ratings from the reviews
       
    Returns:
        float : average rating
    """
    total_rating = 0
    for review_rating in review_ratings:
        total_rating += review_rating
    return total_rating / len(review_ratings)


def _convert_to_bayesian_adj_rating(review_likes, review_ratings):
    """
    Calculates the Bayesian Adjusted ratings from the goodreads ratings and likes on the ratings
    
    Args:
        review_likes (list) : likes from the reviews
        review_ratings (list) : ratings from the reviews
        
    Returns:
        list : bayesian adjusted ratings
    """
    bayesian_adj_ratings = []
    sum_of_likes = sum(review_likes)
    sum_of_likes_mul_ratings = sum(
        [
            review_like * review_rating
            for review_like, review_rating in zip(review_likes, review_ratings)
        ]
    )
    for i in range(len(review_likes)):
        bayesian_adj_ratings.append(
            (review_likes[i] * review_ratings[i] + sum_of_likes_mul_ratings)
            / (review_likes[i] + sum_of_likes)
        )
    return bayesian_adj_ratings


def _calculate_bayesian_adj_rating(bayesian_adj_ratings):
    """
    Calculates the average bayesian adjusted rating
    
    Args:
        bayesian_adj_ratings (list) : bayesian adjusted ratings from the reviews
        
    Returns:
        float : average bayesian adjusted rating
    """
    return sum(bayesian_adj_ratings) / len(bayesian_adj_ratings)


def _build_ratings_list(processed_book_review_info):
    """
    Build a list rating details from a python dict
    
    Args:
        processed_book_review_info (dict) : processed review details
        
    Returns:
        list : processed review details but as a list
    """
    processed_ratings_list = []
    for index in processed_book_review_info:
        ratings_list = []
        ratings_list.append(
            processed_book_review_info[index]["bayesianAdj_rating_goodreads"]
        )
        ratings_list.append(processed_book_review_info[index]["avg_rating_goodreads"])
        ratings_list.append(processed_book_review_info[index]["avg_rating_simple"])
        ratings_list.append(processed_book_review_info[index]["book_name"])
        processed_ratings_list.append(ratings_list)
    return processed_ratings_list


def quicksort(arr_to_be_sorted, start, end):
    """
    Quicksort implementation to sort a list in ascending order
    Complexity - n * logn
    
    Args:
        arr_to_be_sorted (list) : the input list to be sorted
        start (int) : the start index
        end (int) : the end index
    """
    p = start + 1
    q = end
    partition_pos = start
    if (end - start) <= 0:  # one element/no element
        return
    elif (end - start) == 1:  # 2 elements
        if arr_to_be_sorted[start][0] > arr_to_be_sorted[end][0]:
            arr_to_be_sorted[start], arr_to_be_sorted[end] = (
                arr_to_be_sorted[end],
                arr_to_be_sorted[start],
            )
        return

    while p < q:
        while arr_to_be_sorted[p][0] < arr_to_be_sorted[start][0] and p < end:
            p += 1
        while (
            arr_to_be_sorted[q][0] > arr_to_be_sorted[start][0]
        ):  # and p < end similar condition ie q>=start because at the beginning we take "start" as the start
            q -= 1
        if p < q:
            arr_to_be_sorted[p], arr_to_be_sorted[q] = (
                arr_to_be_sorted[q],
                arr_to_be_sorted[p],
            )

    arr_to_be_sorted[start], arr_to_be_sorted[q] = (
        arr_to_be_sorted[q],
        arr_to_be_sorted[start],
    )
    partition_pos = q
    quicksort(arr_to_be_sorted, start, partition_pos - 1)
    quicksort(arr_to_be_sorted, partition_pos + 1, end)


def _process_reviews():
    """
    Main code to start processing the review details
    Ensure sci-fi-books-list_YYYY-MM-DD.pkl file is present in current date otherwise run MainBookScraper to get it
    We are making sure to add 1 to review likes which are 0 so as to not ignore those reviews completely
    
    
    """
    try:
        books_details_pickle_file_name = "sci-fi-books-list"
        book_details = load_obj(books_details_pickle_file_name, "Data")
        # Logger.log('info', 'review_rating_calculation','_process_reviews',book_details)
        # Logger.log('info', 'review_rating_calculation','_process_reviews',str(len(book_details)))
        processed_book_review_info = {}

        for book_index in book_details:
            processed_book_review_info[book_index] = {}
            book_name = extract_book_name_from_root_url(
                book_details[book_index]["book_URL"]
            )
            processed_book_review_info[book_index]["book_name"] = book_name
            Logger.log(
                "debug",
                "review_rating_calculation",
                "_process_reviews",
                "Processing " + book_name,
            )
            book_review = load_latest_obj("book_review_details", "Data/" + book_name)
            Logger.log(
                "debug", "review_rating_calculation", "_process_reviews", book_review
            )
            review_likes, review_ratings = _extract_review_likes_ratings(book_review)
            Logger.log(
                "debug",
                "review_rating_calculation",
                "_process_reviews",
                str(len(review_likes)) + "  " + str(len(review_ratings)),
            )
            are_zero_likes_not_present = [
                review_like != 0 for review_like in review_likes
            ]
            if all(are_zero_likes_not_present):
                Logger.log(
                    "debug",
                    "review_rating_calculation",
                    "_process_reviews",
                    "0 likes not present",
                )
            else:
                Logger.log(
                    "debug",
                    "review_rating_calculation",
                    "_process_reviews",
                    "0 likes present",
                )
                review_likes = [review_like + 1 for review_like in review_likes]
                Logger.log(
                    "debug",
                    "review_rating_calculation",
                    "_process_reviews",
                    "Adding 1 to all likes if even one 0 liked review is present",
                )

            avg_book_rating_simple = _calculate_simple_avg_review_rating(review_ratings)
            processed_book_review_info[book_index][
                "avg_rating_simple"
            ] = avg_book_rating_simple
            processed_book_review_info[book_index][
                "avg_rating_goodreads"
            ] = book_details[book_index]["avg_rating"]
            Logger.log(
                "debug",
                "review_rating_calculation",
                "_process_reviews",
                "avg book rating -simple- " + str(avg_book_rating_simple),
            )

            bayesian_adj_ratings = _convert_to_bayesian_adj_rating(
                review_likes, review_ratings
            )
            avg_book_rating_bayesian_adj = _calculate_bayesian_adj_rating(
                bayesian_adj_ratings
            )
            processed_book_review_info[book_index][
                "bayesianAdj_rating_goodreads"
            ] = avg_book_rating_bayesian_adj
            Logger.log(
                "debug",
                "review_rating_calculation",
                "_process_reviews",
                "Bayesian Adjusted rating -BAR- " + str(avg_book_rating_bayesian_adj),
            )

        Logger.log(
            "debug",
            "review_rating_calculation",
            "_process_reviews",
            processed_book_review_info,
        )
        save_obj(
            processed_book_review_info,
            "processed_book_rating_info",
            "Data/processed book rating info",
        )

        aggregated_ratings_list = _build_ratings_list(processed_book_review_info)
        goodreads_top_book = aggregated_ratings_list[0][3]
        quicksort(aggregated_ratings_list, 0, len(aggregated_ratings_list) - 1)
        our_calculated_top_book = aggregated_ratings_list[-1][3]
        Logger.log(
            "info",
            "review_rating_calculation",
            "_process_reviews",
            "Top Book as per Goodreads - "
            + goodreads_top_book
            + " and as per our calculation is - "
            + our_calculated_top_book,
        )
    except IOError:
        Logger.log(
            "error",
            "review_rating_calculation",
            "_process_reviews",
            "sci-fi-books-list_YYYY-MM-DD.pkl not present in current date. Run MainBookScraper to get it",
        )


if __name__ == "__main__":
    _process_reviews()
