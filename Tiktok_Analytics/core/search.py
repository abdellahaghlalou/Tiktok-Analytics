from typing import List,Optional,Union
import json
import urllib.request
from PIL import Image
import imgcompare
from playwright.async_api import Playwright, async_playwright
from ..models.user_target import UserTarget
from ..models.video_target import VideoTarget
import random
from ..services.captcha import Captcha


class Search:
    
    selectors = json.load(open("Tiktok_Analytics\static\selectors.json"))
    cookies = json.load(open("Tiktok_Analytics\static\cookies.json"))

    def __init__(self,option : int,search_word : str,search_result: Optional[List[Union[VideoTarget,UserTarget]]]) -> None:
        self.option = option
        self.search_word = search_word
        self.search_result = search_result

    
    async def search(self) -> None:
        if self.option == 1:
            self.search_result =  await self.search_by_user(self.search_word)
        if self.option == 2:
            self.search_result =  await self.search_by_video(self.search_word)
        if self.option == 3:
            self.search_result =   self.search_by_hashtag(self.search_word)
        if self.option == 4:
            self.search_result =   self.search_by_sound(self.search_word)

    async def start_playwright():
        global playwright
        playwright = await  async_playwright().start()
        global browser
        browser = await playwright.chromium.launch(headless=False)
        global context
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4929.0 Safari/537.36"
        context = await browser.new_context(user_agent = user_agent)
        await context.add_init_script("Tiktok_Analytics/services/js/navigator.plugins.js")
        await context.add_cookies(Search.cookies)
        global page
        page = await context.new_page()
        page.on('response', Search._responseHandler) 
        await page.set_extra_http_headers({
            "referer": "https://www.google.com/",
        })
        await page.goto("https://www.tiktok.com/")


    async def search_bar(search_word : str):
        search_bar = await page.query_selector("input[type='search']")
        await search_bar.type(search_word)
        await page.wait_for_timeout((random.random() * 2000 + 3000))
        await page.press('button.tiktok-3n0ac4-ButtonSearch.ev30f216', 'Enter')

    async def load_more(n : int):
        for i in range(n):
            await page.wait_for_timeout((random.random() * 1000 + 1000))
            see_more_butt = await page.query_selector(Search.selectors["see_more"])
            await see_more_butt.click()

    async def search_by_user(self,search_word : str) -> List[UserTarget]:

        await Search.start_playwright()
        await page.wait_for_timeout((random.random() * 2000 + 3000))
        
        await Search.search_bar(search_word)        
        await page.wait_for_timeout((random.random() * 1000 + 1000))
        account_butt = await page.query_selector(Search.selectors["Account_button"])
        await account_butt.click()

        await Search.load_more(1)
        await page.wait_for_timeout((random.random() * 1000 + 1000))
        users_containers = await page.query_selector_all(Search.selectors["user_container"])
        all_usernames = [await Search.get_user_name(elt) for elt in users_containers]
        all_imgs = [await Search.get_img(elt) for elt in users_containers]
        all_descs = [await Search.get_user_desc(elt) for elt in users_containers]
        all_nicknames_followers = [await Search.get_nicknames_followers(elt) for elt in users_containers]
        #page.pause()
        await browser.close()
        await playwright.stop()
        return [UserTarget(username=all_usernames[i],nickname_followers=all_nicknames_followers[i],img=all_imgs[i],signature=all_descs[i]) for i in range(len(all_usernames))]

    async def search_by_video(self,search_word : str) -> List[VideoTarget]:
        
        Search.start_playwright()
        page.wait_for_timeout((random.random() * 2000 + 10000))
        Search.search_bar(search_word)        
        page.wait_for_timeout((random.random() * 1000 + 1000))
        page.query_selector(Search.selectors["Videos_button"]).click()
        
        Search.load_more(3)

        page.wait_for_timeout((random.random() * 1000 + 1000))
        videos_containers = page.query_selector_all(Search.selectors["video_container"])
        all_usernames = [Search.get_video_name(elt) for elt in videos_containers]
        all_imgs = [Search.get_img(elt) for elt in videos_containers]
        all_descs = [Search.get_video_desc(elt) for elt in  videos_containers]
        all_tags_hashtags = [Search.get_tags_hashtags(elt) for elt in videos_containers]
        all_VideoWatchCount = [Search.get_VideoWatchCount(elt) for elt in videos_containers]
        all_VideoIds = [Search.get_videoIds(elt) for elt in  videos_containers]

        browser.close()
        playwright.stop()
        return [VideoTarget(username=all_usernames[i],imgLink=all_imgs[i],desc=all_descs[i],tags_hashtags=all_tags_hashtags[i],videoCountWatch=all_VideoWatchCount[i],videoId=all_VideoIds[i]) for i in range(len(all_usernames))]
    
    def search_by_hashtag(self,search_word : str) -> List[VideoTarget]:
        pass

    def search_by_sound(self,search_word : str) -> List[VideoTarget]:
        pass
    
    async def get_user_name(elt):
        username = await elt.query_selector(Search.selectors["username"])
        return await username.text_content()

    async def get_video_name(elt):
        username_video = await elt.query_selector(Search.selectors["username_video"])
        return await username_video.text_content()

    async def get_img(elt):

        try : 
            img =  await elt.query_selector("img")
            img = await img.get_attribute("src")
        except :
            img = ""
        return img 

    async def get_nicknames_followers(elt):
       text = await  elt.query_selector_all("a")
       return await text[1].text_content()

    async def get_user_desc(elt):  
        try :
            desc = await elt.query_selector("//a[2]/p[2]")
            return await desc.text_content()
        except:
            return ""

    async def get_VideoWatchCount(elt):
        elt = await elt.query_selector("div[data-e2e='search-card-like-container']")
        return await elt.text_content()

    async def get_tags_hashtags(elt):
        try :
            list_a_tags = await  elt.query_selector("div[data-e2e='search-card-video-caption']")
            list_a_tags = await list_a_tags.query_selector_all("a")
            list_tags_hashtags = [await a.text_content() for a in list_a_tags]
            return list_tags_hashtags
        except :
            return []

    async def get_video_desc(elt):  
        try :
            desc = await elt.query_selector("//div[@data-e2e='search-card-video-caption']")
            desc = await desc.query_selector("span")
            return desc.text_content()
        except :
            return ""

    async def get_videoIds(elt):
        elt = await elt.query_selector("//div[@data-e2e='search_video-item']//a")
        return await elt.get_attribute("href").split("/")[-1]

    def trasform_nbr(nbr:str) -> int:
        return int(nbr.replace("K","000").replace("M","000000").replace("B","000000000").replace(".",""))

    async def _responseHandler(response):

        maxContentLength = -1

        responseUrl =  response.url
        #print(responseUrl)
        if not Captcha.isCaptchaUrl(responseUrl):
            return
        await page.pause()
        contentLength = int(response.headers['content-length'])
        if contentLength > maxContentLength:
            maxContentLength = contentLength
            urllib.request.urlretrieve(responseUrl, "start.PNG")
            await Captcha.resize_img("start.PNG")
        
        await Search.solveCaptcha()
    
    async def solveCaptcha():

        Captcha.options = Captcha.get_defauls()
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

            sliderImage = await page.screenshot(clip =  await sliderContainer.bounding_box(),path = "current.jpeg")
            await Captcha.resize_img("current.jpeg")
            difference = imgcompare.image_diff_percent("current.PNG", "start.jpeg")

            if target["difference"] > difference :

                target["difference"] = difference
                target["position"] = currentPosition
        

            currentPosition += Captcha.options["positionIncrement"]
        

        await page.evaluate(
        Captcha._removeOverlayAndShowPuzzlePiece,
        [Captcha.get_selectors()["puzzlePieceOverlay"],
        Captcha.get_selectors()["puzzlePiece"]]
        )
        #isVerifyPage =  self._isVerifyPage()

        await page.mouse.move(
        handle["x"] + target["position"],
        handle["y"] + handle["height"] / 2
        )
        await page.mouse.up()

        #return self._waitForCaptchaDismiss(isVerifyPage)