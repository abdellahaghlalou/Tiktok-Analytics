from typing import Optional,Union
from ..database.models.user_target import UserTarget
from ..database.models.video_target import VideoTarget
from ..database.models.scrapeoperation import ScrapeOperation
from TikTokApi import TikTokApi
from typing import List


class Scrape : 

    api = TikTokApi()
    def __init__(self,scrape_operation : Optional[ScrapeOperation]) -> None:
        pass
    def scrape(self,option:str,videos : List[str],users:List[str]) -> List[any]:
        if option == 1:
            return self.scrape_users(users)
        if option == 2:
            return self.scrape_videos(videos)

    def scrape_users(self,users:List[str]) -> List[UserTarget]:
        users_list = []
        for user in users:
            users_list.append(self.scrape_user(user))
        return users_list
    def scrape_videos(self,videos:List[str]) -> List[VideoTarget]:
        videos_list = []
        for video in videos:
            videos_list.append(self.scrape_video(video))
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
    def scrape_video(self,videoId:str) -> VideoTarget:
        pass
    def scrape_video_comments(elt) -> None:
        pass
