from typing import List,Optional,Union
import json
import imgcompare
from playwright.async_api import Playwright, async_playwright
from ..models.user_target import UserTarget
from ..models.video_target import VideoTarget
import random
from ..services.captcha import Captcha
# import glob

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
    
        await context.add_cookies(Search.cookies)
        global page
        page = await context.new_page()
        # for file in glob.glob("Tiktok_Analytics\static\js\*.js"):
        #     print(file)
        #     # await page.add_script_tag(file)
        page.on('response', Search._responseHandler) 
        await page.set_extra_http_headers({
            "referer": "https://www.google.com/",
        })
        # await page.pause()
        await page.goto("https://www.tiktok.com/")



    async def search_bar(search_word : str):
        search_bar = await page.query_selector("input[type='search']")
        await search_bar.type(search_word)
        await page.wait_for_timeout((random.random() * 2000 + 3000))
        await page.press('button.tiktok-3n0ac4-ButtonSearch.ev30f216', 'Enter')

    async def load_more(n : int):
        for i in range(n):
            await page.wait_for_timeout((random.random() * 1000 + 1000))
            see_more_butt = await page.wait_for_selector(Search.selectors["see_more"],timeout=10000000,)
            await see_more_butt.click()

    async def search_by_user(self,search_word : str) -> List[UserTarget]:

        await Search.start_playwright()
        await page.wait_for_timeout((random.random() * 2000 + 3000))
        
        await Search.search_bar(search_word)        
        await page.wait_for_timeout((random.random() * 1000 + 1000))
        account_butt = await page.query_selector(Search.selectors["Account_button"])
        await account_butt.click(timeout= 10000000)

        await Search.load_more(1)
        await page.wait_for_timeout((random.random() * 1000 + 1000))
        users_containers = await page.query_selector_all(Search.selectors["user_container"])
        all_usernames = [await Search.get_user_name(elt) for elt in users_containers]
        all_imgs = [await Search.get_img(elt) for elt in users_containers]
        all_descs = [await Search.get_user_desc(elt) for elt in users_containers]
        all_nicknames_followers = [await Search.get_nicknames_followers(elt) for elt in users_containers]
        hasBadge = [await Search.hasBadge(elt) for elt in users_containers]

        await browser.close()
        await playwright.stop()
        return [UserTarget(username=all_usernames[i],nickname_followers=all_nicknames_followers[i],img=all_imgs[i],hasBadge=hasBadge[i],signature=all_descs[i]) for i in range(len(all_usernames))]

    async def search_by_video(self,search_word : str) -> List[VideoTarget]:
        
        await Search.start_playwright()
        await page.wait_for_timeout((random.random() * 2000 + 10000))
        await Search.search_bar(search_word)        
        await page.wait_for_timeout((random.random() * 1000 + 1000))
        video_butt = await page.wait_for_selector(Search.selectors["Videos_button"])
        await video_butt.click(timeout= 10000000)
        
        await Search.load_more(1)

        await page.wait_for_timeout((random.random() * 1000 + 1000))
        videos_containers =await  page.query_selector_all(Search.selectors["video_container"])
        all_usernames = [await Search.get_video_name(elt) for elt in videos_containers]
        all_imgs = [await Search.get_img(elt) for elt in videos_containers]
        all_descs = [await Search.get_video_desc(elt) for elt in  videos_containers]
        all_tags_hashtags = [await Search.get_tags_hashtags(elt) for elt in videos_containers]
        all_VideoWatchCount = [await Search.get_VideoWatchCount(elt) for elt in videos_containers]
        all_VideoIds = [await Search.get_videoIds(elt) for elt in  videos_containers]
        all_tags = [await Search.get_tags(elt) for elt in  videos_containers]
        all_hashtags = [await Search.get_hashtags(elt) for elt in  videos_containers]
        all_times = [await Search.get_time(elt) for elt in  videos_containers]
        all_usernames_images = [await Search.get_username_image(elt) for elt in  videos_containers]
        await browser.close()
        await playwright.stop()
        return [VideoTarget(username=all_usernames[i],username_img=all_usernames_images[i],time = all_times[i],tags =all_tags[i],hashtags=all_hashtags[i] ,imgLink=all_imgs[i],tags_hashtags=all_tags_hashtags[i],videoCountWatch=all_VideoWatchCount[i],videoId=all_VideoIds[i]) for i in range(len(all_usernames))]
    
    def search_by_hashtag(self,search_word : str) -> List[VideoTarget]:
        pass

    def search_by_sound(self,search_word : str) -> List[VideoTarget]:
        pass
    
    async def hasBadge(elt):
        svg = await elt.query_selector(Search.selectors["badge"])
        if(await elt.query_selector(Search.selectors["badge"])):
            return True
        else:
            return False

    async def get_user_name(elt):
        username = await elt.query_selector(Search.selectors["username"])
        return await username.text_content()

    async def get_username_image(elt):
        username = await elt.query_selector(Search.selectors["username_video_image"])
        img = await username.get_attribute('src')
        # print("img: "+img)
        return img

    async def get_video_name(elt):
        username_video = await elt.query_selector(Search.selectors["username_video"])
        return await username_video.text_content()

    async def get_time(elt):
        time = await elt.query_selector(Search.selectors["video_time"])
        time = await time.text_content()
        # print("time : "+time)
        return time

    async def get_img(elt):

        try : 
            img =  await elt.query_selector("img")
            img = await img.get_attribute("src")
        except :
            img = ""
        return img 

    async def get_nicknames_followers(elt):
        try : 
            desc = await elt.query_selector("//a[2]/p[3]")
            desc = await desc.text_content()
            nick_foll = await elt.query_selector("//a[2]/p[2]")
            return await nick_foll.text_content()
        except :
            nick_foll = await elt.query_selector("//a[2]/div")
            try : 
                return await nick_foll.text_content()
            except :
                nick_foll = await elt.query_selector("//a[2]/p[2]")
                return await nick_foll.text_content()


    async def get_user_desc(elt):  
        try :
            desc = await elt.query_selector("//a[2]/p[3]")
            return await desc.text_content()
        except:
            desc = await elt.query_selector("//a[2]/p[2]")
            try :
                return await desc.text_content()
            except :
                return ""

    async def get_VideoWatchCount(elt):
        elt = await elt.query_selector("div[data-e2e='search-card-like-container']")
        return await elt.text_content()
    async def get_hashtags(elt):
        try :
            list_a_tags = await  elt.query_selector("div[data-e2e='search-card-video-caption']")
            list_a_tags = await list_a_tags.query_selector_all("a")
            list_tags_hashtags = [await a.text_content() for a in list_a_tags]
            return [hashtag for hashtag in list_tags_hashtags if hashtag.startswith("#")]
        except :
            return []
    async def get_tags(elt):
        try :
            list_a_tags = await  elt.query_selector("div[data-e2e='search-card-video-caption']")
            list_a_tags = await list_a_tags.query_selector_all("a")
            list_tags_hashtags = [await a.text_content() for a in list_a_tags]
            return [tag for tag in list_tags_hashtags if tag.startswith("@")]
        except :
            return []
    async def get_tags_hashtags(elt):
        try :
            list_a_tags = await  elt.query_selector("div[data-e2e='search-card-video-caption']")
            list_a_tags = await list_a_tags.query_selector_all("a")
            list_tags_hashtags = [await a.text_content() for a in list_a_tags]
            return "".join(list_tags_hashtags)
        except :
            return ""

    async def get_video_desc(elt):  
        try :
            desc = await elt.query_selector("//div[@data-e2e='search-card-video-caption']")
            desc = await desc.query_selector("span")
            return desc.text_content()
        except :
            return " "

    async def get_videoIds(elt):
        elt = await elt.query_selector("//div[@data-e2e='search_video-item']//a")
        elt = await elt.get_attribute("href")
        return elt.split("/")[-1]

    def trasform_nbr(nbr:str) -> int:
        return int(nbr.replace("K","000").replace("M","000000").replace("B","000000000").replace(".",""))

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
        await Search.solveCaptcha()
    
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
