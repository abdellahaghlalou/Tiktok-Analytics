from ..models.user import User
from ..models.video import Video
from ..models.scrapeoperation import ScrapeOperation
from typing import List


class scrape : 
    def __init__(self,scrape_operation : ScrapeOperation) -> None:
        pass
    def scrape(self,option:str,videos : List[Video],users:List[User]) -> None:
        if option == 1:
            self.scrape_users(users)
        if option == 2:
            self.scrape_videos(videos)
    def scrape_users(self,users:List[User]) -> None:
        for user in users:
            self.scrape_user(User.username)
    def scrape_videos(self,videos:List[Video]) -> None:
        for video in videos:
            self.scrape_video(Video.videoId)
    def scrape_user(self,username:str) -> None:
        pass
    def scrape_video(self,videoId:str) -> None:
        pass
    def scrape_video_comments(elt) -> None:
        pass
