import requests as rq 
from bs4 import BeautifulSoup
from cred_manager import LI_TOKEN, LI_ID
import pdb
import urllib.parse as urp


def scrape_linkedin():
	# Scrape linkedin using api
	token = LI_TOKEN
	headers = {"Authorization": "Bearer "+token}
	encoded_urn = urp.quote_plus('urn:li:organization'+LI_ID)
	print(encoded_urn)
	url = "https://api.linkedin.com/v2/ugcPosts?q=authors&authors=List("+encoded_urn+")"
	resp = rq.get(url,headers=headers)
	pdb.set_trace()
	print(resp.text)
	return 0

scrape_linkedin()











"""
import pdb

user = "industrial-engineers-club-iec"

def scrape_linkedin(driver,user,n):
	page_url = "https://www.linkedin.com/company/" + user
	driver.get(page_url)
	pdb.set_trace()
	#driver.implicitly_wait(3000)
	soup = BeautifulSoup(driver.page_source,'html.parser')
	posts = list(soup.select("div.share-update-card"))
	pdb.set_trace()
	print(len(posts))
	data = []
	for post in posts:
		likes = post.select_one("a[data-tracking-control-name='organization-update_share-update_likes-text']")
		comments = post.select_one("a[data-tracking-control-name='organization-update_share-update_comments-text']")
		num_likes = [int(s) for s in likes.text.split() if s.isdigit()][0]
		num_comments = [int(s) for s in comments.text.split() if s.isdigit()][0]
		post_caption = post.select_one("p.share-update-card__update-text").text[0:100]
		print(num_likes,num_comments)
		post_data = {
			"likes": num_likes,
			"comments": num_comments,
			"platform": "linkedin",
			"caption": post_caption,
			"id": gen_id(post_caption)
		}
		data.append(post_data)

	print(data)
	return data

def gen_id(origin):
	# Generate unique id to use in google sheet to avoid duplicates when updating sheet
	m = hashlib.md5()

	m.update(origin.encode())
	return str(int(m.hexdigest(), 16))[0:12]
"""