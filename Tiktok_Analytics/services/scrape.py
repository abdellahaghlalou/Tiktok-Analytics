from typing import Optional,Union
from ..database.models.user_target import UserTarget
from ..database.models.video_target import VideoTarget
from ..database.models.scrapeoperation import ScrapeOperation
from TikTokApi import TikTokApi
from typing import List


class Scrape : 
    def __init__(self,scrape_operation : Optional[ScrapeOperation]) -> None:
        pass
    def scrape(self,option:str,videos : List[str],users:List[str]) -> List[any]:
        if option == 1:
            return self.scrape_users(users)
        if option == 2:
            return self.scrape_videos(videos)

    def scrape_users(self,users:List[str]) -> List:
        users_list = []
        for user in users:
            users_list.append(self.scrape_user(user))
        return users_list
    def scrape_videos(self,videos:List[str]) -> List:
        videos_list = []
        for video in videos:
            videos_list.append(self.scrape_video(video))
        return videos_list
    def scrape_user(self,username:str) -> None:
        api = TikTokApi()
        user = api.user(username)
        return user.info_full()
    def scrape_video(self,videoId:str) -> None:
        pass
    def scrape_video_comments(elt) -> None:
        pass
