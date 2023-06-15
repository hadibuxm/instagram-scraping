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

# # get instagram account credentials
# username = input('Enter Your User Name ')
# password = input('Enter Your Password ')

# # assign URL
# url = 'https://instagram.com/' + \
# 	input('Enter User Name Of User For Downloading Posts ')

# # Get URL path
# def path():
# 	global chrome
# 	# starts a new chrome session
# 	# add path if required
# 	chrome = webdriver.Chrome()
	
# # Extract URL
# def url_name(url):
# 	# the web page opens up
# 	chrome.get(url)
	
# 	# webdriver will wait for 4 sec before throwing a
# 	# NoSuchElement exception so that the element
# 	# is detected and not skipped.
# 	time.sleep(4)
	
# # Login to access post
# def login(username, your_password):
# 	log_div = chrome.find_element(By.CLASS_NAME, "x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1xmf6yo x1e56ztr x540dpk x1m39q7l x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1")
# 	log_but = log_div.find_element(By.CLASS_NAME, "_acan _acap _acas _aj1-")
# 	time.sleep(2)
# 	print(log_but.is_enabled())
# 	log_but.click()
# 	time.sleep(4)
# 	# finds the username box
# 	usern = chrome.find_element_by_name("username")
# 	# sends the entered username
# 	usern.send_keys(username)

# 	# finds the password box
# 	passw = chrome.find_element_by_name("password")

# 	# sends the entered password
# 	passw.send_keys(your_password)

# 	# sends the enter key
# 	passw.send_keys(Keys.RETURN)

# 	time.sleep(5.5)

# 	# Find Not Now Button
# 	notn = chrome.find_element_by_class_name("yWX7d")

# 	notn.click()
# 	time.sleep(3)
	
# # Function to get content of first post
# def first_post():
# 	pic = chrome.find_element_by_class_name("kIKUG").click()
# 	time.sleep(2)
	
# # Function to get next post
# def next_post():
# 	try:
# 		nex = chrome.find_element_by_class_name(
# 			"coreSpriteRightPaginationArrow")
# 		return nex
# 	except selenium.common.exceptions.NoSuchElementException:
# 		return 0
	
# # Download content of all posts
# def download_allposts():

# 	# open First Post
# 	first_post()

# 	user_name = url.split('/')[-1]

# 	# check if folder corresponding to user name exist or not
# 	if(os.path.isdir(user_name) == False):

# 		# Create folder
# 		os.mkdir(user_name)

# 	# Check if Posts contains multiple images or videos
# 	multiple_images = nested_check()

# 	if multiple_images:
# 		nescheck = multiple_images
# 		count_img = 0
		
# 		while nescheck:
# 			elem_img = chrome.find_element_by_class_name('rQDP3')

# 			# Function to save nested images
# 			save_multiple(user_name+'/'+'content1.'+str(count_img), elem_img)
# 			count_img += 1
# 			nescheck.click()
# 			nescheck = nested_check()

# 		# pass last_img_flag True
# 		save_multiple(user_name+'/'+'content1.' +
# 					str(count_img), elem_img, last_img_flag=1)
# 	else:
# 		save_content('_97aPb', user_name+'/'+'content1')
# 	c = 2
	
# 	while(True):
# 		next_el = next_post()
		
# 		if next_el != False:
# 			next_el.click()
# 			time.sleep(1.3)
			
# 			try:
# 				multiple_images = nested_check()
				
# 				if multiple_images:
# 					nescheck = multiple_images
# 					count_img = 0
					
# 					while nescheck:
# 						elem_img = chrome.find_element_by_class_name('rQDP3')
# 						save_multiple(user_name+'/'+'content' +
# 									str(c)+'.'+str(count_img), elem_img)
# 						count_img += 1
# 						nescheck.click()
# 						nescheck = nested_check()
# 					save_multiple(user_name+'/'+'content'+str(c) +
# 								'.'+str(count_img), elem_img, 1)
# 				else:
# 					save_content('_97aPb', user_name+'/'+'content'+str(c))
			
# 			except selenium.common.exceptions.NoSuchElementException:
# 				print("finished")
# 				return
		
# 		else:
# 			break
		
# 		c += 1

# # Function to save content of the current post
# def save_content(class_name, img_name):
# 	time.sleep(0.5)
	
# 	try:
# 		pic = chrome.find_element_by_class_name(class_name)
	
# 	except selenium.common.exceptions.NoSuchElementException:
# 		print("Either This user has no images or you haven't followed this user or something went wrong")
# 		return
	
# 	html = pic.get_attribute('innerHTML')
# 	soup = bs(html, 'html.parser')
# 	link = soup.find('video')
	
# 	if link:
# 		link = link['src']
	
# 	else:
# 		link = soup.find('img')['src']
# 	response = requests.get(link)
	
# 	with open(img_name, 'wb') as f:
# 		f.write(response.content)
# 	time.sleep(0.9)
	
# # Function to save multiple posts
# def save_multiple(img_name, elem, last_img_flag=False):
# 	time.sleep(1)
# 	l = elem.get_attribute('innerHTML')
# 	html = bs(l, 'html.parser')
# 	biglist = html.find_all('ul')
# 	biglist = biglist[0]
# 	list_images = biglist.find_all('li')
	
# 	if last_img_flag:
# 		user_image = list_images[-1]
	
# 	else:
# 		user_image = list_images[(len(list_images)//2)]
# 	video = user_image.find('video')
	
# 	if video:
# 		link = video['src']
	
# 	else:
# 		link = user_image.find('img')['src']
# 	response = requests.get(link)
	
# 	with open(img_name, 'wb') as f:
# 		f.write(response.content)

# # Function to check if the post is nested
# def nested_check():
	
# 	try:
# 		time.sleep(1)
# 		nes_nex = chrome.find_element_by_class_name('coreSpriteRightChevron ')
# 		return nes_nex
	
# 	except selenium.common.exceptions.NoSuchElementException:
# 		return 0

# # Driver Code
# path()
# time.sleep(1)

# url_name(url)

# login(username, password)

# download_allposts()

# chrome.close()
from instapy import InstaPy
import os
import instaloader
# working for user posts
"""
insta_username = 'heisenberg'
insta_password = 'panoakil.'
user_to_download = 'hadibux_mahessar'  # Replace with the username of the user whose posts you want to download
target_folder = user_to_download+'_posts'

loader = instaloader.Instaloader()
loader.login(insta_username, insta_password)

profile = instaloader.Profile.from_username(loader.context, user_to_download)
for post in profile.get_posts():
    loader.download_post(post, target=target_folder)

loader.close()

"""
import random

def insta_post_downloader(anime):
    insta_username = 'Krun.ai'
    insta_password = 'learn2earn'
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
anime_list = ['queenberyl']
for anime in anime_list:
    insta_post_downloader(anime)
    sleep(30)






