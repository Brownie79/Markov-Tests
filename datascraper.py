#!python
import requests
import json
import facebook
import requests
from urllib.parse import parse_qs

APP_ID = '460299580843062'
APP_NAME = 'markov'
APP_SECRET = 'a892688755cd673d914e075ca377f824'
FACEBOOK_GRAPH_URL = "https://graph.facebook.com"
ACCESS_TOKEN = '460299580843062|PhtmUW3MEMVh5pI_A44NA_I6mdI'

group_id = '759985267390294' #hackathonhackers
graph = facebook.GraphAPI(ACCESS_TOKEN,version='2.5')
feed = graph.get_connections(group_id,'feed',limit='500')

#constants
POST_LIMIT_GRAB = 200 
LIKE_THRESHOLD = 55

def log_post(postID):
    likes_dict = graph.get_connections(postID,connection_name="likes",summary='true')
    likes = likes_dict['summary']['total_count']

    filename = "" # pop/sod#postid#likes
    pop = "FALSE"
    if(likes>=LIKE_THRESHOLD):
        filename = group_id + "/pop#" + postID + '#' + str(likes) + ".txt"  
        pop = "TRUE"
    else:
        filename = group_id + "/sod#" + postID + '#' + str(likes) + ".txt"
    
    newFile = open(filename, "w")
    message = graph.get_object(postID)['message']
    newFile.write(message)
    
    newFile.close()

def main():
    counter = 0
    global feed
    while(counter<POST_LIMIT_GRAB):
        try:
            data = feed['data']
            for post in data:
                log_post(post['id'])
                counter += 1
                if(counter>POST_LIMIT_GRAB):
                    break
            feed = requests.get(feed['paging']['next']).json()
            
        except KeyError:
            print("No More Posts")
            break
            
            
if __name__ == "__main__":
    main()