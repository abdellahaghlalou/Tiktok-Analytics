from typing import Optional
from unittest import result

from requests import request
from ..models.user_target import UserTarget
from ..models.video_target import VideoTarget
from ..database.models.user_target import UserTargetModel
from ..database.models.video_target import VideoTargetModel
from ..database.models.scrapeoperation import ScrapeOperation
from playwright.async_api import Playwright, async_playwright
from TikTokApi import TikTokApi
from typing import List
import urllib.request
import imgcompare
from ..services.captcha import Captcha
from ..database.database import add_new_users, add_new_videos
import random
import time
import json


class Scrape : 

    selectors = json.load(open("Tiktok_Analytics\static\selectors.json"))
    cookies = json.load(open("Tiktok_Analytics\static\cookies.json"))
    api = TikTokApi()
    use_tiktok = True
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
        page.on('response', Scrape._responseHandler)
        await page.goto("https://www.tiktok.com/")

    async def scrape(self,option:str,targets : List[dict],request) -> List[any]:
        if option == 1:
            return await self.scrape_users(targets,request)
        if option == 2:
            return await self.scrape_videos(targets,request)

    async def scrape_users(self,users:List[dict],request) -> List[UserTarget]:
        users_list = []
        if(Scrape.use_tiktok):
            await Scrape.start_playwright()
            for user in users:
                users_list.append(await self.scrape_user_from_tiktok(user["username"],request))
            await browser.close()
            await playwright.stop()     
        else:
            for user in users:
                users_list.append(await self.scrape_user(user["username"],request))
        return users_list

    async def scrape_videos(self,videos:List[dict],request) -> List[VideoTarget]:
        await Scrape.start_playwright()
        videos_list = []
        for video in videos:
            videos_list.append(await self.scrape_video(video,request))
        await browser.close()
        return videos_list
        
    async def scrape_user_from_tiktok(self,username:str,request) -> List[str]:
        await page.goto("https://www.tiktok.com/@"+username)
        await page.wait_for_load_state("networkidle")
        followersC = await page.wait_for_selector(Scrape.selectors["user_page"]["followers"])
        followers = await followersC.text_content()
        followers = Scrape.trasform_nbr(followers)
        followingC = await page.wait_for_selector(Scrape.selectors["user_page"]["following"])
        following = await followingC.text_content()
        following = Scrape.trasform_nbr(following)
        likesC = await page.wait_for_selector(Scrape.selectors["user_page"]["likes"])
        likes = await likesC.text_content()
        likes = Scrape.trasform_nbr(likes)
        desc = await page.wait_for_selector(Scrape.selectors["user_page"]["signature"])
        desc = await desc.text_content()
        nickname = await page.wait_for_selector(Scrape.selectors["user_page"]["user_nickname"])
        nickname = await nickname.text_content()
        imageLink = await page.wait_for_selector(Scrape.selectors["user_page"]["user_profile_image"])
        imageLink = await imageLink.get_attribute("src")

        user_data = UserTarget(username=username,
                                nickname=nickname,
                                signature=desc,
                                img=imageLink,
                                privateAccount=False,
                                isUnderAge18=None,
                                followingCount=following,
                                followerCount=followers,
                                videoCount=None,
                                heartCount= likes,
                                diggCount=None,
                                )
        await add_new_users(request=request,results=[user_data])
        user_target_rel = UserTargetModel(username=user_data.username,scrap_operation_id=self.scrape_operation.id)

        # img_filename = "Tiktok_Analytics\static\images"+"\"+user_data.username+".jpg"
        # Scrape.store_video_img(user_data.img,img_filename)
        await user_target_rel.save()
        return user_data

    async def scrape_user(self,username:str,request) -> UserTarget:
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
        await add_new_users(results= [user_data], request = request)
        user_target_rel = UserTargetModel(username=user_data.username,scrap_operation_id=self.scrape_operation.id)

        # img_filename = "Tiktok_Analytics\static\images"+"\"+user_data.username+".jpg"
        # Scrape.store_video_img(user_data.img,img_filename)
        await user_target_rel.save()
        return user_data

    async def scrape_video(self,video : dict,request) -> VideoTarget:
       
        await page.wait_for_timeout((random.random() * 2000 + 3000))

        video_url = "https://www.tiktok.com/@" + video["username"] + "/video/" + video["id"]+"?is_copy_url=1&is_from_webapp=v1&q="+video["username"]+"&t="+str(int(time.time()))
        await page.goto(video_url)
        await page.wait_for_timeout((random.random() * 1000 + 3000))

        button = await page.query_selector(Scrape.selectors["comment_button"])
        
        await button.click(timeout= 10000000)
        await page.wait_for_timeout((random.random() * 1000 + 1000))

        sound = await page.query_selector(Scrape.selectors["sound"])
        sound= await sound.get_attribute("href")
        commentCount = await page.query_selector(Scrape.selectors["commentCount"])
        commentCount = await commentCount.text_content()
        commentCount = Scrape.trasform_nbr(commentCount)
        shareCount = await page.query_selector(Scrape.selectors["shareCount"])
        shareCount = await shareCount.text_content()
        shareCount = Scrape.trasform_nbr(shareCount)
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
         
        # video_filename = "Tiktok_Analytics\static\videos"+"\\"+video["id"] + ".mp4"
        # image_filename  = "Tiktok_Analytics\static\images"+"\\"+ video["id"] + ".jpg"
        # Scrape.store_video_img(video_link,video_filename)
        # Scrape.store_video_img(img_link,image_filename)

        # int(commentCount)//20
        for i in range(10):
            # window.scroll(0,document.body.scrollHeight)
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
                    
        # await browser.close()
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
        await add_new_videos(results=[video_data],request = request)
        video_target_rel = VideoTargetModel(video_id=video_data.videoId,scrap_operation_id=self.scrape_operation.id)
        await video_target_rel.save()
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

    def store_video_img(link:str,filename:str) -> None:
        try :
            urllib.request.urlretrieve(link, filename)
        except :
            print("you are trying to download existing item")
        
    async def _responseHandler(response):

        maxContentLength = -1

        responseUrl =  response.url
        if not Captcha.isCaptchaUrl(responseUrl):
            return
        contentLength = int(response.headers['content-length'])
        if contentLength > maxContentLength:
            maxContentLength = contentLength
        await page.evaluate(Captcha.disabeleScroll)
        # await page.pause()
        await Scrape.solveCaptcha()
        await page.evaluate(Captcha.enableScroll)

    async def solveCaptcha():

        Captcha.options = Captcha.get_defauls()

        elt =await page.query_selector(".captcha_verify_img_slide")
        style = await elt.get_attribute("style")
        await page.evaluate("document.querySelector('.captcha_verify_img_slide').style = 'hidden'")
        sliderContainer =  await page.query_selector(
          Captcha.get_selectors()["puzzleImageWrapper"]
        )
        await page.screenshot(clip =  await sliderContainer.bounding_box(),path = 'start.PNG')
        await page.evaluate("(stl) => document.querySelector('.captcha_verify_img_slide').style = stl",style)
        await Captcha.resize_img("start.PNG")



        await page.evaluate(Captcha.appendOverlayAndHidePuzzlePiece,
                            [Captcha.get_selectors()["puzzlePiece"],
                            Captcha.get_selectors()["puzzlePieceOverlay"],
                            Captcha.get_selectors()["puzzleImageWrapper"]])

        sliderElement =  await page.query_selector(Captcha.get_selectors()["sliderElement"])
        sliderHandle =  await page.query_selector(Captcha.get_selectors()["sliderHandle"])
        slider =  await sliderElement.bounding_box()
        handle =  await sliderHandle.bounding_box()

        currentPosition = Captcha.options["startPosition"]

        target = {
        "position": 0,
        "difference": 100,
        }
        await page.wait_for_timeout(3000)

        await page.mouse.move(
        handle["x"] + handle["width"] / 2,
        handle["y"] + handle["height"] / 2
        )
        await page.mouse.down()

        while   currentPosition < slider["width"] - handle["width"] / 2 :
            await page.mouse.move(
            handle["x"] + currentPosition,
            handle["y"] + handle["height"] / 2)
        

            await page.evaluate(
            Captcha._syncOverlayPositionWithPuzzlePiece,
            [Captcha.get_selectors()["puzzlePiece"],
            Captcha.get_selectors()["puzzlePieceOverlay"]])
        

            sliderContainer =  await page.query_selector(
            Captcha.get_selectors()["puzzleImageWrapper"]
        )
            

            bbox = await sliderContainer.bounding_box()
            sliderImage = await page.screenshot(clip =  bbox,path = "current.jpeg")
            await Captcha.resize_img("current.jpeg")
            difference = imgcompare.image_diff_percent("current.PNG", "start.PNG")

            if target["difference"] > difference :

                target["difference"] = difference
                target["position"] = currentPosition
        

            currentPosition += Captcha.options["positionIncrement"]
        

        await page.evaluate(
        Captcha._removeOverlayAndShowPuzzlePiece,
        [Captcha.get_selectors()["puzzlePieceOverlay"],
        Captcha.get_selectors()["puzzlePiece"]]
        )
        

        await page.mouse.move(
        handle["x"] + target["position"],
        handle["y"] + handle["height"] / 2
        )
        await page.mouse.up()
