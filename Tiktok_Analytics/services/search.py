from typing import List,Optional
from models.user import User
from models.video import Video
import random


class search:

    def __init__(self,option : int,search_word : str,search_result: Optional[List[User | Video]]) -> None:
        self.option = option
        self.searcrh_word = search_word
        self.search_result = search_result
    
    def search(self) -> None:
        if self.option == 1:
            self.search_result = self.search_by_user(self.search_word)
        if self.option == 2:
            self.search_result = self.search_by_video(self.search_word)
        if self.option == 3:
            self.search_result = self.search_by_hashtag(self.search_word)
        if self.option == 4:
            self.search_result = self.search_by_sound(self.search_word)

    def search_by_user(self,search_word : str,browser) -> List[User]:
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.tiktok.com/")
        page.wait_for_timeout((random.random() * 2000 + 10000))
        page.pause()
        #page.goto("https://www.tiktok.com/search?lang=en&q="+user)
        page.query_selector("input[type='search']").type(search_word)
        page.wait_for_timeout((random.random() * 2000 + 3000))
        page.press('button.tiktok-3n0ac4-ButtonSearch.ev30f216', 'Enter')
        # page.query_selector("button.tiktok-3n0ac4-ButtonSearch.ev30f216").click()

        page.wait_for_timeout((random.random() * 1000 + 1000))
        page.query_selector("").click()
        # for i in range(5): 
        #     page.query_selector('Button.tiktok-1mwtjmv-ButtonMore.e1v5onft1').click()
        page.wait_for_timeout((random.random() * 1000 + 1000))
        users_containers = page.query_selector_all("")
        all_usernames = list(map(self.get_user_name, users_containers))
        all_imgs = list(map(self.get_img, users_containers))
        #all_nicknames = list(map(get_nickname, users_containers))
        all_descs = list(map(self.get_user_desc, users_containers))
        #all_followers = list(map(get_followers, users_containers))
        print(all_imgs)
        print(len(all_usernames),len(all_descs),len(all_imgs))
        page.pause()

        context.close()
        return [User(username=all_usernames[i],img=all_imgs[i],desc=all_descs[i]) for i in range(len(all_usernames))]

    def search_by_video(self,search_word : str) -> List[Video]:
        pass
    
    def search_by_hashtag(self,search_word : str) -> List[Video]:
        pass

    def search_by_sound(self,search_word : str) -> List[Video]:
        pass
    
    def get_user_name(elt):
        return elt.query_selector("p.tiktok-1v1eqb4-PTitle.e12ixqxa4").text_content()

    def get_img(elt):
        return elt.query_selector("img").get_attribute("src")

    def get_nickname(elt):
        return elt.query_selector("h2.tiktok-1n69p9f-H2SubTitle.e12ixqxa6").text_content()

    def get_user_desc(elt):  
        try :
            return elt.query_selector("p.tiktok-1jq7d8a-PDesc.e12ixqxa7").text_content()
        except:
            return ""

    def get_followers(elt):
        return elt.query_selector("div.tiktok-1av3vif-DivSubTitleWrapper.e12ixqxa5").query_selector("span").text_content()
    
    def get_video_name(elt):
        return elt.query_selector("a[data-e2e='search-card-user-link']").text_content()

    def get_VideoWatchCount(elt):
        return elt.query_selector("div[data-e2e='search-card-like-container']").text_content()

    def get_tags_hashtags(elt):
        list_a_tags = elt.query_selector("div[data-e2e='search-card-video-caption']").query_selector_all("a")
        list_tags_hashtags = [a.text_content() for a in list_a_tags]
        return list_tags_hashtags

    def get_video_desc(elt):  
        return elt.query_selector("div[data-e2e='search-card-video-caption']").query_selector("span").text_content()