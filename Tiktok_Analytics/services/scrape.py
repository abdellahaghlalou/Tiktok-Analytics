from typing import Optional,Union
from ..database.models.user_target import UserTarget
from ..database.models.video_target import VideoTarget
from ..database.models.scrapeoperation import ScrapeOperation
from playwright.async_api import Playwright, async_playwright
from TikTokApi import TikTokApi
from typing import List
import random
import time
import json


class Scrape : 

    selectors = json.load(open("Tiktok_Analytics\services\selectors.json"))
    cookies = json.load(open("Tiktok_Analytics\services\cookies.json"))
    api = TikTokApi()
    def __init__(self,scrape_operation : Optional[ScrapeOperation]) -> None:
        pass

    async def start_playwright():
        global playwright
        playwright = await async_playwright().start()
        global browser
        browser =  await playwright.chromium.launch(headless=False)
        global context
        context = await browser.new_context()
        #context.add_init_script("Tiktok_Analytics/services/js/navigator.plugins.js")
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

        buttons = await page.query_selector_all("button.tiktok-1xiuanb-ButtonActionItem.e1bs7gq20")
        await buttons[1].click()
        await page.wait_for_timeout((random.random() * 1000 + 1000))

        sound = await page.query_selector("h4[data-e2e='browse-music'] > a")
        sound= await sound.get_attribute("href")
        commentCount = await page.query_selector("strong[data-e2e='browse-comment-count']")
        commentCount = await commentCount.text_content()
        commentCount = Scrape.trasform_nbr(commentCount)
        likeCounts = await page.query_selector("strong[data-e2e='browse-like-count']")
        likeCounts = await likeCounts.text_content()
        likeCounts = Scrape.trasform_nbr(likeCounts)

        # int(commentCount)//20
        for i in range(3):
            elt = await page.query_selector("div.tiktok-46wese-DivCommentListContainer.ey83cgi0")
            await elt.evaluate("elt => elt.scroll(0,elt.scrollHeight)")
            await page.wait_for_timeout((random.random() * 100 + 100))
        comments = await page.query_selector_all("div.tiktok-16r0vzi-DivCommentItemContainer.e1c8wije0")

        comments = [{"whocomments" :await co.query_selector("a"),
                    "text":await co.query_selector("p[data-e2e='comment-level-1']") } 
                    for co in comments]

        comments = [{"username":await co["whocomments"].get_attribute("href"),
                    "text":await co["text"].text_content()} 
                    for co in comments]
        #print(sound,commentCount,likeCounts,comments,len(comments))
        await browser.close()
        video_data = VideoTarget(username=video["username"],
                                videoId=video["id"],
                                soundId=sound,
                                commentCount=commentCount,
                                likeCount=likeCounts,
                                comments=comments,
                                )
        return video_data
    
    def trasform_nbr(nbr:str) -> int:

        return int(nbr.replace("K","000").replace("M","000000").replace("B","000000000").replace(".",""))