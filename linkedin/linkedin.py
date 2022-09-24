from sys import path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from time import sleep
import time
from datetime import datetime
from parsel import Selector
import json
import os
import re
import datetime
import requests # request img from web
import shutil # save img locally
from decouple import config

service = Service(executable_path=ChromeDriverManager().install())
options = ChromeOptions()
options.headless = True  # hide GUI
options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
options.add_argument("start-maximized")
options.binary_location = os.getenv("BROWSER_PATH")
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.linkedin.com/login")
username = driver.find_element_by_id("username")
username.send_keys(config('USERNAME'))
password = driver.find_element_by_id("password")
password.send_keys(config('PASSWORD'))
sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
sign_in_button.click()

linkedin_urls = [
    "https://www.linkedin.com/company/amazon",
    "https://www.linkedin.com/company/google",
    "https://www.linkedin.com/company/ibm",
]
sleep(0.5)

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def getNo(s):
    num = re.findall(r"\d+", s)
    return int(num[0])
    

def getDate(date):
    init_date = date.split("•")[0].strip()
    num = getNo(init_date)
    today = datetime.date.today()
    if(init_date.find("d") != -1):
        post_date = today - datetime.timedelta(days=num)
        # if(num>7): 
        #     return 'skip'
        return post_date

    elif(init_date.find("w") != -1):
        post_date = today - datetime.timedelta(weeks=num)
        # if(num>5): 
        #     return 'skip'
        return post_date
        # return 'skip'

    elif(init_date.find("mo") != -1):
        post_date = today - datetime.timedelta(weeks=num*4)
        # if(num>4): 
        #     return 'skip'
        return post_date   
        # return 'skip' 

    elif(init_date.find("yr") != -1):
        post_date = today - datetime.timedelta(weeks=num*52)
        return post_date
        # return 'skip'

    post_date = today - datetime.timedelta(hours=num)
    return post_date

def selectCompany(company):
    switcher = {
        "the-clorox-company": "Clorox",
        "scjohnson": "SC Johnson",
        "unilever": "Unilever",
        "church-&-dwight-co-inc": "Church & Dwight Co., Inc.",
        "gojo-industries": "GoJo (Purell)",
        "procter-and-gamble": "Procter & Gamble",
        "reckitt":"RB",
        "ab-inbev":"AB Inbev",
        "the-coca-cola-company":"The Coca-Cola Company",
        "suntory-holdings-limited":"Suntory",
        "nestle-s-a-":"Nestle",
        "asahi":"Asahi Group",
        "jpmorganchase":"JPMorgan Chase",
        "bank-of-america": "Bank of America",
        "citi": "Citigroup",
        "wellsfargo":"Wells Fargo",
        "rbc": "Royal Bank of Canada",
        "td": "Toronto-Dominion Bank",
        "goldman-sachs": "Goldman Sachs",
        "morgan-stanley": "Morgan Stanley",
        "bank-of-montreal": "Bank of Montreal",
       
    }
    return switcher.get(company, company)
    
posts = []
str = " "

# For loop to iterate over each URL in the list
for linkedin_url in linkedin_urls:
    if linkedin_url:
        linkedin_company = linkedin_url.split("company/")[1]
        # make dir with company
        path_company = f"Linkedin-Posts/{selectCompany(linkedin_company)}"
        if os.path.exists(path_company):
            shutil.rmtree(path_company)
        os.mkdir(path_company)
        posts_url = f"{linkedin_url}/posts?feedView=all"
        driver.get(posts_url)
        sleep(1)
        crawledData = []
        Company = []
        # code for scroll
        SCROLL_PAUSE_TIME = 3
        abc = 0
        #  Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            new_height = new_height + 150
            print(new_height,"height")
            if new_height == last_height:
                break
            # if new_height > 15000:
            #     break
            last_height = new_height

        sleep(5)
        sel = Selector(text=driver.page_source)
        crawledData = sel.xpath(
            '//*[starts-with(@class, "ember-view  occludable-update")]'
        ).getall()
        print("No. of posts ", len(crawledData))

        if crawledData:
            for element in crawledData:
                post = {}
                ext1 = Selector(text=element)
                caption = ext1.xpath(
                    '//*[starts-with(@class, "feed-shared-text relative feed-shared-update-v2__commentary")]/span/span/span'
                ).get()
                if not caption:
                    caption = ext1.xpath(
                        '//*[starts-with(@class, "feed-shared-text relative feed-shared-update-v2__commentary")]/span/span'
                    ).get()
                if caption:    
                    caption = remove_html_tags(caption)
                image = ext1.css("img").xpath("@src").getall()
                video = ext1.css("video").xpath("@src").getall()
                id = ext1.css("div").xpath("@data-urn").get()
                print(id)
                date = ext1.xpath(
                        '//*[starts-with(@class, "feed-shared-actor__sub-description t-12 t-normal")]/span/span/text()'
                    ).get()
                external_link = ext1.xpath(
                        '//*[starts-with(@class, "app-aware-link feed-shared-article__image-link tap-target")]/@href'
                    ).get() 
                if id:
                    id = id.rsplit(":",1)[1]
                post["caption"] = caption
                post["id"] = id
                linkedin_company = selectCompany(linkedin_company)
                post["company"]= linkedin_company
                if date:    
                    posted_at = getDate(date)  
                    if(posted_at == 'skip'): 
                        continue
                    post["posted_at"] = posted_at.isoformat()
                if external_link:
                    post["external_link"] = external_link    

                posts.append(post)

                path = f"Linkedin-Posts/{linkedin_company}/{id}"

                # make dir with id names
                if os.path.exists(path):
                    shutil.rmtree(path)
                os.mkdir(path)

                with open(f"{path}/data.json", "w", encoding="utf-8") as f:
                    json.dump(post, f, ensure_ascii=False, indent=4, default=str) 

                # download images
                for index, img in enumerate(image):
                    if (img.find("static-exp1.licdn.com") == -1):
                        pic_path = f"{path}/image{index}.jpg"
                        res = requests.get(img, stream = True)
                        if res.status_code == 200:
                            with open(pic_path,'wb') as f:
                                shutil.copyfileobj(res.raw, f)
                        else:
                            print('Image Couldn\'t be retrieved')

                # download videos
                if video:
                    for index, vid in enumerate(video):
                        if vid.startswith("http"):
                            sleep(0.5)
                            vid_path = f"{path}/video{index}.mp4"
                            res = requests.get(vid, stream = True)
                            if res.status_code == 200:
                                with open(vid_path,'wb') as f:
                                    shutil.copyfileobj(res.raw, f)
                            else:
                                print('Vid Couldn\'t be retrieved')  
                
                with open("data.json", "w", encoding="utf-8") as f:
                    json.dump(posts, f, ensure_ascii=False, indent=4, default=str)

print("crawling complete !!!!!!!!!!!!!!")
driver.quit()
