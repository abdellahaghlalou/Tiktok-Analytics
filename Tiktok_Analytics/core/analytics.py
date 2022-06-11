


def analyse_data(userid : str):
    all_operations = get_operations_ids(id)
    all_data = get_scraped_data(all_operations)
    videos = filter_videos(all_data)
    accounts = filter_accounts(videos)
    video_analytics = analyse_videos(videos)
    account_analytics = analyse_accounts(accounts)
    return {'account': account_analytics, 'video': video_analytics}

def filter_videos(list):
    pass

def filter_accounts(list):
    pass

def analyse_accounts():
    pass

def analyse_videos(videos):
    
    all_comments = []
    all_mentions = []
    all_hashtags = []
    all_sounds = []
    return {
        'most_watched_videos': most_watched_videos(videos),
        'most_liked_videos': most_liked_videos(videos),
        'most_shared_videos': most_shared_videos(videos),
        'most_commented_videos': most_commented_videos(videos),
        'comments_cloud': comments_cloud(all_comments),
        'mentions_cloud': mentions_cloud(all_mentions),
        'hashtage_cloud': hashtage_cloud(all_hashtags),
        'sound_cloud': sound_cloud(all_sounds)
    }

def preprocess_comments(text):
    pass



def  get_scraped_data():
    pass

def get_operations_ids():
    pass

def hashtage_cloud():
    pass

def sound_cloud():
    pass

def desc_cloud():
    pass

def signature_cloud():
    pass

def mentions_cloud():
    pass

def comments_cloud():
    pass

def most_watched_videos(list):
    return sorted(list, key=lambda k: k['videoCountWatch'], reverse = True)

def most_liked_videos(list):
    return sorted(list, key=lambda k: k['likeCount'], reverse = True)

def most_shared_videos(list):
    return sorted(list, key=lambda k: k['shareCount'], reverse = True)

def most_commented_videos(list):
    return sorted(list, key=lambda k: k['commentCount'], reverse = True)

