from typing import List,Optional
from models.user import User
from models.video import Video


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

    def search_by_user(self,search_word : str) -> List[User]:
        pass

    def search_by_video(self,search_word : str) -> List[Video]:
        pass
    
    def search_by_hashtag(self,search_word : str) -> List[Video]:
        pass

    def search_by_sound(self,search_word : str) -> List[Video]:
        pass
