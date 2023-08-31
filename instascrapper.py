# # import required modules
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By

# import selenium.common.exceptions
# import time
# from bs4 import BeautifulSoup as bs
# import requests
# import os
from time import sleep
from instapy import InstaPy
import os
import instaloader
# working for user posts

import random

def insta_post_downloader(anime):
    insta_username = 'your_insta_username'
    insta_password = 'your_insta_password'
    # user_to_download = 'hadibux_mahessar'  # Replace with the username of the user whose posts you want to download

    post_amount = 200

    loader = instaloader.Instaloader()
    loader.login(insta_username, insta_password)
    # explore_query = input("enter anime name")
    explore_query = anime 
    explore_posts = loader.get_hashtag_posts(explore_query)
    target_folder = explore_query+'_posts'
    count = 0

    for post in explore_posts:
        if count >= post_amount:
            break
        loader.download_post(post, target=target_folder)
        sleep(random.uniform(4, 10))
        count += 1

    loader.close()

# anime_names
post_list = ['pakistan']
for post in post_list:
    insta_post_downloader(post)
    sleep(30)






