import selectors
from typing import List,Optional,Union
import json
from playwright.sync_api import Playwright, sync_playwright
from ..database.models.user_target import UserTarget
from ..database.models.video_target import VideoTarget
import random


class Search:
    
    selectors = json.load(open("Tiktok_Analytics\services\selectors.json"))
    cookies = json.load(open("Tiktok_Analytics\services\cookies.json"))

    def __init__(self,option : int,search_word : str,search_result: Optional[List[Union[VideoTarget,UserTarget]]]) -> None:
        self.option = option
        self.search_word = search_word
        self.search_result = search_result

    
    def search(self) -> None:
        if self.option == 1:
            self.search_result =  self.search_by_user(self.search_word)
        if self.option == 2:
            self.search_result =  self.search_by_video(self.search_word)
        if self.option == 3:
            self.search_result =  self.search_by_hashtag(self.search_word)
        if self.option == 4:
            self.search_result =  self.search_by_sound(self.search_word)

    def start_playwright():
        global playwright
        playwright = sync_playwright().start()
        global browser
        browser = playwright.chromium.launch(headless=False)
        global context
        context = browser.new_context()
        #context.add_cookies()
        global page
        page = context.new_page()
        page.goto("https://www.tiktok.com/")

    def search_bar(search_word : str):
        page.query_selector("input[type='search']").type(search_word)
        page.wait_for_timeout((random.random() * 2000 + 3000))
        page.press('button.tiktok-3n0ac4-ButtonSearch.ev30f216', 'Enter')

    def load_more(n : int):
        for i in range(n):
            page.wait_for_timeout((random.random() * 1000 + 1000))
            page.query_selector(Search.selectors["see_more"]).click()

    def search_by_user(self,search_word : str) -> List[UserTarget]:

        Search.start_playwright()
        page.wait_for_timeout((random.random() * 2000 + 10000))
        Search.search_bar(search_word)        
        page.wait_for_timeout((random.random() * 1000 + 1000))
        page.query_selector(Search.selectors["Account_button"]).click()

        Search.load_more(10)
        page.pause()
        page.wait_for_timeout((random.random() * 1000 + 1000))
        users_containers = page.query_selector_all(Search.selectors["user_container"])
        all_usernames = list(map(Search.get_user_name, users_containers))
        all_imgs = list(map(Search.get_img, users_containers))
        #all_nicknames = list(map(get_nickname, users_containers))
        all_descs = list(map(Search.get_user_desc, users_containers))
        #all_followers = list(map(get_followers, users_containers))
        #page.pause()
        print(all_usernames)
        browser.close()
        playwright.stop()
        return [UserTarget(username=all_usernames[i],img=all_imgs[i],desc=all_descs[i]) for i in range(len(all_usernames))]

    def search_by_video(self,search_word : str) -> List[VideoTarget]:
        
        Search.start_playwright()
        page.wait_for_timeout((random.random() * 2000 + 10000))
        Search.search_bar(search_word)        
        page.wait_for_timeout((random.random() * 1000 + 1000))
        page.query_selector(Search.selectors["Videos_button"]).click()
        
        Search.load_more(3)

        page.wait_for_timeout((random.random() * 1000 + 1000))
        videos_containers = page.query_selector_all(Search.selectors["video_container"])
        all_usernames = list(map(Search.get_video_name, videos_containers))
        all_imgs = list(map(Search.get_img, videos_containers))
        all_descs = list(map(Search.get_video_desc, videos_containers))
        all_tags_hashtags = list(map(Search.get_tags_hashtags, videos_containers))
        all_VideoWatchCount = list(map(Search.get_VideoWatchCount, videos_containers))
        all_VideoIds = list(map(Search.get_videoIds, videos_containers))
        print(all_VideoIds)

        browser.close()
        playwright.stop()
        return [VideoTarget(username=all_usernames[i],img=all_imgs[i],desc=all_descs[i],tags_hashtags=all_tags_hashtags[i],videoCountWatch=all_VideoWatchCount[i],videoId=all_VideoIds[i]) for i in range(len(all_usernames))]
    
    def search_by_hashtag(self,search_word : str) -> List[VideoTarget]:
        pass

    def search_by_sound(self,search_word : str) -> List[VideoTarget]:
        pass
    
    def get_user_name(elt):
        return elt.query_selector(Search.selectors["username"]).text_content()

    def get_video_name(elt):
        return elt.query_selector(Search.selectors["username_video"]).text_content()

    def get_img(elt):

        try : 
            img =  elt.query_selector("img").get_attribute("src")
        except :
            img = ""
        return img 

    def get_nickname(elt):
        return elt.query_selector("h2.tiktok-1n69p9f-H2SubTitle.e12ixqxa6").text_content()

    def get_user_desc(elt):  
        try :
            return elt.query_selector("p.tiktok-1jq7d8a-PDesc.e12ixqxa7").text_content()
        except:
            return ""

    def get_followers(elt):
        return elt.query_selector("div.tiktok-1av3vif-DivSubTitleWrapper.e12ixqxa5").query_selector("span").text_content()
    
    def get_VideoWatchCount(elt):
        return elt.query_selector("div[data-e2e='search-card-like-container']").text_content()

    def get_tags_hashtags(elt):
        try :
            list_a_tags = elt.query_selector("div[data-e2e='search-card-video-caption']").query_selector_all("a")
            list_tags_hashtags = [a.text_content() for a in list_a_tags]
            return list_tags_hashtags
        except :
            return []

    def get_video_desc(elt):  
        try :
            return elt.query_selector("div[data-e2e='search-card-video-caption']").query_selector("span").text_content()
        except :
            return ""

    def get_videoIds(elt):
        return elt.query_selector("//div[@data-e2e='search_video-item']//a").get_attribute("href").split("/")[-1]