
import requests as rq
from cred_manager import INSTA_TOKEN
from bs4 import BeautifulSoup
import hashlib
user = "john.doe" # put username here

def scrape_instagram(driver,user,n):
	# scrape the last n posts
	user_url = "https://instagram.com/"+user
	driver.get(user_url)
	# Wait 1 second
	driver.implicitly_wait(1000)
	soup = BeautifulSoup(driver.page_source,"html.parser")
	posts = soup.find_all("div",{"class":"kIKUG"})
	data = []
	for post in posts:

		post_url_el = post.find("a")
		post_url =  "http://instagram.com" + post_url_el["href"] 
		
		driver.get(post_url)
		post_soup = BeautifulSoup(driver.page_source,"html.parser")
		likes = post_soup.select_one(".sqdOP span")
		num_comments = len(list(post_soup.find_all("ul",{"class":"Mr508"})))
		caption = post_soup.select_one(".C4VMK span")
		post_caption = ""
		if caption == None:
			post_caption = ""
		else:
			post_caption = caption.text[0:100]
		post_data = {
			"likes": int(likes.text),
			"comments": num_comments,
			"caption": post_caption,
			"shares":0,# For convenience
			"id": gen_id(post_caption)
			}
		print(post_data)
		data.append(post_data)
		
		#print(likes)
		#likes = driver.find_element_by_css_selector(".sqd0P span")
		#print(likes.text)
		#driver.implicitly_wait(2000)
	print(data)
	return data

def gen_id(origin):
	# Generate unique id to use in google sheet to avoid duplicates when updating sheet
	m = hashlib.md5()
	m.update(origin.encode())
	return str(int(m.hexdigest(), 16))[0:12]

		



		


