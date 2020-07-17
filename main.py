
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from insta import *
#from linked import *
from facebook import *
import csv 

def save2csv(data):
    #will create 3 csv each time to store scraped data
    header = ["id","caption","likes","comments","shares"]
    for platform in data:
        #keys = data[platform][0].keys()
        csv_file = open("data/" + platform + ".csv","w")
        dict_writer = csv.DictWriter(csv_file, header)
        dict_writer.writeheader()
        dict_writer.writerows(data[platform])
        print("generated csv for " + platform)






options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')

driver = webdriver.Chrome(executable_path="./chromedriver")

data = {}

data["instagram"] = scrape_instagram(driver,'iec.enp',10)
#data["linkedin"] = scrape_linkedin(driver,'industrial-engineers-club-iec',10)

data["facebook"] = scrape_fb(driver,'IEC-103377834618496',10)
save2csv(data)
driver.close()