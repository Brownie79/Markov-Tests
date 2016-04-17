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

#for use with requests
FACEBOOK_GRAPH_URL = "https://graph.facebook.com/"


def post_info(post):
    postID = post['id']
    likes = graph.get_connections(postID,connection_name="likes") #this way enables summary field to get total count
    
    print(likes)


def main():
    while True:
        try: 
            data = feed['data']
            for post in data:
                post_info(post['id'])
            feed = requests.get(feed['paging']['next']).json()    
    
        except KeyError: 
            #no more pages of posts
            break
            
def main2():
    postID ="177577782278470_995462617156645" #Reno's post sharing the thing, 5 likes
    likes = requests.get("https://graph.facebook.com/v2.5/"+postID+"?fields=likes.summary(true)&access_token="+access_token).json()
    likes2 = graph.get_connections(postID, "likes",summary="true")        
    #path = "%s/%s/%s" % ("v2.5", postID, "likes")
    #likes3 = request2(path,{"summary":"true"})
    
    print(json.dumps(likes,sort_keys=True,indent=4,separators=(',', ': ')))
    print(json.dumps(likes2,sort_keys=True,indent=4,separators=(',', ': ')))        
    #print(json.dumps(likes3,sort_keys=True,indent=4,separators=(',', ': ')))        


def request2(path, args=None, post_args=None, files=None, method=None):
    args = args or {}

    if post_args is not None:
        method = "POST"

    if access_token:
        if post_args is not None:
            post_args["access_token"] = access_token
        else:
            args["access_token"] = access_token

    try:
        response = requests.request(method or "GET",
                                    FACEBOOK_GRAPH_URL + path,
                                    timeout=None,
                                    params=args,
                                    data=post_args,
                                    proxies=None,
                                    files=files)
        print(response.url)
    except requests.HTTPError as e:
        response = json.loads(e.read())
        raise GraphAPIError(response)

    headers = response.headers
    if 'json' in headers['content-type']:
        result = response.json()
    elif 'image/' in headers['content-type']:
        mimetype = headers['content-type']
        result = {"data": response.content,
                    "mime-type": mimetype,
                    "url": response.url}
    elif "access_token" in parse_qs(response.text):
        query_str = parse_qs(response.text)
        if "access_token" in query_str:
            result = {"access_token": query_str["access_token"][0]}
            if "expires" in query_str:
                result["expires"] = query_str["expires"][0]
        else:
            raise GraphAPIError(response.json())
    else:
        raise GraphAPIError('Maintype was not text, image, or querystring')

    if result and isinstance(result, dict) and result.get("error"):
        raise GraphAPIError(result)
    return result

if __name__ == "__main__":
    main2()
    