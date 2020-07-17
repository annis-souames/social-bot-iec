from bs4 import BeautifulSoup
import hashlib
import pdb

user = "####" # Put user id here

def scrape_fb(driver,user,n):
	page_url = "https://www.facebook.com/pg/"+ user + "/posts/"
	driver.get(page_url)
	#driver.implicitly_wait(3000)
	soup = BeautifulSoup(driver.page_source,"html.parser")
	posts = soup.select("._1xnd div._4-u2")
	pdb.set_trace()
	data = []
	for post in posts:
		num_likes, num_comments, num_shares = 0,0,0
		caption_txt = ""
		
		likes = post.select_one("span._81hb")
		comments = post.select_one("a._3hg-")
		shares = post.select_one("a._3rwx")
		caption = post.select_one("div[data-testid='post_message'] p")
		post_link = post.select_one("a._5pcq")

		# Check if likes,comments,shares existes
		if likes != None:
			num_likes = int(likes.text)
		if comments != None:
			num_comments = [int(s) for s in comments.text.split() if s.isdigit()][0]
		if shares != None:
			num_shares = [int(s) for s in shares.text.split() if s.isdigit()][0]
		if caption != None:
			caption_txt = caption.text[0:100]
		else:
			continue

		post_data = {
			
			"likes": num_likes,
			"comments": num_comments,
			"shares": num_shares,
			"caption": caption_txt,
			"id": gen_id(caption_txt)
		}
		data.append(post_data)
		print(post_data)
		# remove duplicate entries
	data = [dict(t) for t in {tuple(d.items()) for d in data}]
	print(data)
	return data 

def gen_id(origin):
	# Generate unique id to use in google sheet to avoid duplicates when updating sheet
	m = hashlib.md5()
	m.update(origin.encode())
	return str(int(m.hexdigest(), 16))[0:12]
