#!python
import facebook
import requests
import json

itsc = "177577782278470"
access_token = 'CAACEdEose0cBAFSIPpeijW5T4D5mZBGtexkZCCqJ1ZCZBUjWpx2Tgr1jhPMcBUMQPYK2dS930vu2q9XZC1Q8vXSoZAt9EnxvmA5sdA2ihi0AcZCJZCCd1IYSdBQJgC13QSDJZAIWZCtU3Qtu0r9SlZBQMgQAX6uhX9wLgs9jFNWSEgEFAITdnZCtnvGWMpmSykYnEU7mzfGptOIkLw3kXcSIX21b'

#facebook-sdk
graph = facebook.GraphAPI(access_token,version='2.5')
group = graph.get_object(itsc)
feed = graph.get_connections(itsc,'feed')


def post_info(postID):
    #get_connections(id,connection_name,**kwargs)
    # **kwargs is dictionary of parameters, entered as such function(keyword1="val",keyword2="val")
    # interpreted as {"keyword1":"val, "keyword1":"val"}    
    likes = graph.get_connections(postID, "likes",summary="true")          
    
def append_json():
    """
    import json
    with open('data.txt', 'w') as f:
        json.dump(data, f, ensure_ascii=False)
    """
def main():
    flag = True
    while flag:
        try: 
            data = feed['data']
            for post in data:
                post_info(post['id'])
            #feed = requests.get(posts['paging']['next']).json()    
            flag = False
        except KeyError: 
            break             #no more pages of posts

