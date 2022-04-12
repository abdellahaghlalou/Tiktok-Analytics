import selectors
from typing import Optional,Union
from ..models.user_target import UserTarget
from ..models.video_target import VideoTarget
from ..database.models.scrapeoperation import ScrapeOperation
from playwright.async_api import Playwright, async_playwright
from TikTokApi import TikTokApi
from typing import List
import urllib.request
import random
import time
import json


class Scrape : 

    selectors = json.load(open("Tiktok_Analytics\static\selectors.json"))
    cookies = json.load(open("Tiktok_Analytics\static\cookies.json"))
    api = TikTokApi()
    def __init__(self,scrape_operation : Optional[ScrapeOperation]) -> None:
        self.scrape_operation = scrape_operation

    async def start_playwright():
        global playwright
        playwright = await async_playwright().start()
        global browser
        browser =  await playwright.chromium.launch(headless=False)
        global context
        context = await browser.new_context()
        #context.add_init_script("Tiktok_Analytics/static/js/navigator.plugins.js")
        await context.add_cookies(Scrape.cookies)
        global page
        page = await context.new_page()
        await page.goto("https://www.tiktok.com/")

    async def scrape(self,option:str,targets : List[dict]) -> List[any]:
        if option == 1:
            return self.scrape_users(targets)
        if option == 2:
            return await self.scrape_videos(targets)

    def scrape_users(self,users:List[dict]) -> List[UserTarget]:
        users_list = []
        for user in users:
            users_list.append(self.scrape_user(user["username"]))
        return users_list

    async def scrape_videos(self,videos:List[dict]) -> List[VideoTarget]:
        videos_list = []
        for video in videos:
            videos_list.append(await self.scrape_video(video))
        return videos_list
        
    def scrape_user(self,username:str) -> UserTarget:
        user = Scrape.api.user(username)
        user_info = user.info_full()
        user_data = UserTarget(username=user_info["user"]["uniqueId"],
                                nickname=user_info["user"]["nickname"],
                                signature=user_info["user"]["signature"],
                                img=user_info["user"]["avatarMedium"],
                                privateAccount=user_info["user"]["privateAccount"],
                                isUnderAge18=user_info["user"].get("isUnderAge",None),
                                followingCount=user_info["stats"]["followingCount"],
                                followerCount=user_info["stats"]["followerCount"],
                                videoCount=user_info["stats"]["videoCount"],
                                heartCount=user_info["stats"]["heartCount"],
                                diggCount=user_info["stats"]["diggCount"],
                                )
        return user_data

    async def scrape_video(self,video : dict) -> VideoTarget:
        await Scrape.start_playwright()
        await page.wait_for_timeout((random.random() * 2000 + 3000))

        video_url = "https://www.tiktok.com/@" + video["username"] + "/video/" + video["id"]+"?is_copy_url=1&is_from_webapp=v1&q="+video["username"]+"&t="+str(int(time.time()))
        await page.goto(video_url)
        await page.wait_for_timeout((random.random() * 1000 + 3000))

        buttons = await page.query_selector_all("button.tiktok-1xiuanb-ButtonActionItem.ee8s79f0")
        
        await buttons[1].click()
        await page.wait_for_timeout((random.random() * 1000 + 1000))

        sound = await page.query_selector(Scrape.selectors["sound"])
        sound= await sound.get_attribute("href")
        commentCount = await page.query_selector(Scrape.selectors["commentCount"])
        commentCount = await commentCount.text_content()
        commentCount = Scrape.trasform_nbr(commentCount)
        likeCounts = await page.query_selector(Scrape.selectors["likeCount"])
        likeCounts = await likeCounts.text_content()
        likeCounts = Scrape.trasform_nbr(likeCounts)
        video_link = await page.query_selector(Scrape.selectors["videoLink"])
        video_link = await video_link.get_attribute("src")
        img_link = await page.query_selector(Scrape.selectors["videoImgLink"])
        img_link = await img_link.get_attribute("src")
        video_desc = await page.query_selector(Scrape.selectors["video_desc"])
        video_description = await Scrape.get_video_desc(video_desc)
        video_hashtags = await Scrape.get_video_hashtags(video_desc)
        video_tags = await Scrape.get_video_tags(video_desc)
        #video_bytes = await Scrape.api.video(video["id"]).bytes()
         
        video_filename = "Tiktok_Analytics\static\\videos\\"+self.scrape_operation.user_id+"\\"+video["id"] + ".mp4"
        image_filename  = "Tiktok_Analytics\static\\images\\"+self.scrape_operation.user_id+"\\"+video["id"] + ".jpg"
        try :
            urllib.request.urlretrieve(video_link, video_filename)
        except :
            print("you are trying to download existing video")
        try :
            urllib.request.urlretrieve(img_link, image_filename)
        except :
            print("you are trying to download existing image")

        # int(commentCount)//20
        for i in range(10):
            elt = await page.query_selector(Scrape.selectors["comment_section"])
            await elt.evaluate("elt => elt.scroll(0,elt.scrollHeight)")
            await page.wait_for_timeout((random.random() * 100 + 100))
        await page.wait_for_timeout((random.random() * 1000 + 1000))
        comments = await page.query_selector_all(Scrape.selectors["single_comment"])

        comments = [{"whocomments" :await co.query_selector("a"),
                    "text":await co.query_selector("p[data-e2e='comment-level-1']") } 
                    for co in comments]

        comments = [{"username":await co["whocomments"].get_attribute("href"),
                    "text":await co["text"].text_content()} 
                    for co in comments]

        comments = [{"username":co["username"].split("/")[-1],
                    "text":co["text"]}  
                    for co in comments]
                    
        await browser.close()
        video_data = VideoTarget(username=video["username"],
                                videoId=video["id"],
                                videoLink=video_link,
                                imgLink=img_link,
                                soundId=sound,
                                commentCount=commentCount,
                                likeCount=likeCounts,
                                comments=comments,
                                desc = video_description,
                                tags = video_tags,
                                hashtags = video_hashtags,
                                )
        return video_data
    
    def trasform_nbr(nbr:str) -> int:

        return int(nbr.replace("K","000").replace("M","000000").replace("B","000000000").replace(".",""))
    
    async def get_video_desc(video_desc:str) -> str:
        all_text = await video_desc.query_selector_all("span")
        all_text = [await elt.text_content() for elt in all_text]
        return " ".join(all_text)
    
    async def get_video_hashtags(video_desc:str) -> List[str]:
        all_hashtags = await video_desc.query_selector_all("a")
        hashtags = [await hashtag.text_content() for hashtag in all_hashtags]
        hashtags = [hashtag for hashtag in hashtags if hashtag.startswith("#")]
        return hashtags
    
    async def get_video_tags(video_desc:str) -> List[str]:
        all_tags = await video_desc.query_selector_all("a")
        tags = [await tag.text_content() for tag in all_tags]
        tags = [tag for tag in tags if tag.startswith("@")]
        return tags