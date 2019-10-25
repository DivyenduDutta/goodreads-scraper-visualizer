# -*- coding: utf-8 -*-
"""
.. module:: book_review_visualization
    :synopsis: Visualizes Goodreads review details for a book

.. moduleauthor:: DivyenduDutta

- `_build_color_scatter_plot_array(book_review)`
- `visualize_and_save_review_information(book_review, book_name)`
"""
from __future__ import division
import matplotlib.pyplot as plt
from HelperUtils import extract_book_name_from_root_url, check_if_file_exists_otherwise_handle
import numpy as np
from matplotlib.lines import Line2D 

#book_review = {
#        0: {'review_rating': 1, 'review_likes':5},
#        1: {'review_rating': 5, 'review_likes':500},
#        2: {'review_rating': 3, 'review_likes':45},
#        }


def _build_color_scatter_plot_array(book_review):
    """
    Creates the review color list based on the review rating
    
    Args:
        book_review (dict) : details of the book review
        
    Returns:
        list of colors based on the review
    """
    colors = []
    for review in book_review:
        if book_review[review]['review_rating'] == 1:
            colors.append('red')
        elif book_review[review]['review_rating'] == 2:
            colors.append('blue')
        elif book_review[review]['review_rating'] == 3:
            colors.append('yellow')
        elif book_review[review]['review_rating'] == 4:
            colors.append('black')
        else:
            colors.append('green')
            
    return colors
    
def visualize_and_save_review_information(book_review, book_name):
    """
    Main function which visualizes the review likes. 
    Each review is represented as a circle, the more likes a review has the larger the circle is
    The color of the circle is based on how positive the review is
    Also saves a high res PNG image of the review visualization
    Normalizes the review likes via min max normalization
    
    Args:
       book_review (dict) : details of the book review
       book_name (str) : the name of the book whose review details are to be visualized
    """
    min_value = min([book_review[review_detail]['review_likes'] for review_detail in book_review])
    max_value = max([book_review[review_detail]['review_likes'] for review_detail in book_review])
    RANGE_DIFF = max_value - min_value
    
    #min max normalization: start
    min_value_new = 100
    max_value_new = 1000
    NEW_RANGE_DIFF = max_value_new - min_value_new
    
    a = NEW_RANGE_DIFF/RANGE_DIFF
    b = max_value_new - a * max_value
    number_of_reviews = len(book_review)

    normalized_likes = [a * book_review[review_detail]['review_likes'] + b for review_detail in book_review]
    #min max normalization: end
    # Fixing random state
    np.random.seed(19680801)
    N = number_of_reviews
    x = np.random.rand(N)
    y = np.random.rand(N)
    colors = _build_color_scatter_plot_array(book_review)
    color_meaning = ['did not like it', 'it was ok', 'liked it', 'really liked it', 'it was amazing']
    plt.scatter(x, y, s=normalized_likes, c=colors, alpha=0.5)
    plt.axis('off')
    legend_colors = ['red', 'blue', 'yellow','black', 'green']
    circles = []
    for color in legend_colors:
        circle = Line2D(range(1), range(1), color="white", marker='o', markerfacecolor=color)
        circles.append(circle)
    
    plt.text(1, 1, book_name, ha='center', va='center')
    plt.legend(circles, color_meaning, prop={'size': 4})
    plt.grid(True)
    check_if_file_exists_otherwise_handle('Data/'+book_name+'/'+book_name+'.png')
    plt.savefig('Data/'+book_name+'/'+book_name+'.png', bbox_inches='tight', dpi=1200) #save image
    plt.show()
    
if __name__ == '__main__':
    pass
    #visualize_and_save_review_information()
